"""
Christopher's AI Coaching Business - Stripe Webhook Handler
Comprehensive webhook processing for real-time billing events and automation
"""

import asyncio
import logging
import hmac
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import json
import stripe
import asyncpg
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import aioredis
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
STRIPE_WEBHOOK_SECRET = "whsec_..."
STRIPE_SECRET_KEY = "sk_live_..."
DATABASE_URL = "postgresql://user:pass@localhost/billing_db"
REDIS_URL = "redis://localhost:6379"

# Initialize Stripe
stripe.api_key = STRIPE_SECRET_KEY

class WebhookEventType(str, Enum):
    # Customer events
    CUSTOMER_CREATED = "customer.created"
    CUSTOMER_UPDATED = "customer.updated"
    CUSTOMER_DELETED = "customer.deleted"
    
    # Subscription events
    SUBSCRIPTION_CREATED = "customer.subscription.created"
    SUBSCRIPTION_UPDATED = "customer.subscription.updated"
    SUBSCRIPTION_DELETED = "customer.subscription.deleted"
    SUBSCRIPTION_TRIAL_WILL_END = "customer.subscription.trial_will_end"
    
    # Invoice events
    INVOICE_CREATED = "invoice.created"
    INVOICE_FINALIZED = "invoice.finalized"
    INVOICE_PAYMENT_SUCCEEDED = "invoice.payment_succeeded"
    INVOICE_PAYMENT_FAILED = "invoice.payment_failed"
    INVOICE_UPCOMING = "invoice.upcoming"
    
    # Payment events
    PAYMENT_INTENT_SUCCEEDED = "payment_intent.succeeded"
    PAYMENT_INTENT_FAILED = "payment_intent.payment_failed"
    PAYMENT_METHOD_ATTACHED = "payment_method.attached"
    
    # Charge events
    CHARGE_SUCCEEDED = "charge.succeeded"
    CHARGE_FAILED = "charge.failed"
    CHARGE_DISPUTE_CREATED = "charge.dispute.created"
    
    # Card events
    SOURCE_EXPIRING = "customer.source.expiring"

@dataclass
class WebhookProcessingResult:
    success: bool
    event_type: str
    processed_at: datetime
    message: str
    data: Optional[Dict] = None
    error: Optional[str] = None

class StripeWebhookHandler:
    """Comprehensive Stripe webhook processing system"""
    
    def __init__(self):
        self.db_pool = None
        self.redis = None
        self.processing_stats = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'duplicate': 0
        }
        
    async def initialize(self):
        """Initialize database connections"""
        self.db_pool = await asyncpg.create_pool(DATABASE_URL)
        self.redis = await aioredis.from_url(REDIS_URL)
        logger.info("Stripe webhook handler initialized")
    
    async def process_webhook(self, payload: bytes, signature: str) -> WebhookProcessingResult:
        """Process incoming Stripe webhook with verification and handling"""
        try:
            # Verify webhook signature
            try:
                event = stripe.Webhook.construct_event(payload, signature, STRIPE_WEBHOOK_SECRET)
            except ValueError as e:
                logger.error(f"Invalid payload: {e}")
                return WebhookProcessingResult(
                    success=False,
                    event_type="unknown",
                    processed_at=datetime.utcnow(),
                    message="Invalid payload",
                    error=str(e)
                )
            except stripe.error.SignatureVerificationError as e:
                logger.error(f"Invalid signature: {e}")
                return WebhookProcessingResult(
                    success=False,
                    event_type="unknown",
                    processed_at=datetime.utcnow(),
                    message="Invalid signature",
                    error=str(e)
                )
            
            # Check for duplicate events
            if await self._is_duplicate_event(event['id']):
                logger.info(f"Duplicate event ignored: {event['id']}")
                self.processing_stats['duplicate'] += 1
                return WebhookProcessingResult(
                    success=True,
                    event_type=event['type'],
                    processed_at=datetime.utcnow(),
                    message="Duplicate event ignored"
                )
            
            # Store webhook event
            await self._store_webhook_event(event)
            
            # Process event based on type
            result = await self._route_webhook_event(event)
            
            # Update processing statistics
            self.processing_stats['total_processed'] += 1
            if result.success:
                self.processing_stats['successful'] += 1
            else:
                self.processing_stats['failed'] += 1
            
            return result
            
        except Exception as e:
            logger.error(f"Webhook processing failed: {str(e)}")
            return WebhookProcessingResult(
                success=False,
                event_type="unknown",
                processed_at=datetime.utcnow(),
                message="Processing error",
                error=str(e)
            )
    
    async def _route_webhook_event(self, event: Dict) -> WebhookProcessingResult:
        """Route webhook event to appropriate handler"""
        event_type = event['type']
        event_data = event['data']['object']
        
        handler_mapping = {
            # Customer events
            WebhookEventType.CUSTOMER_CREATED: self._handle_customer_created,
            WebhookEventType.CUSTOMER_UPDATED: self._handle_customer_updated,
            WebhookEventType.CUSTOMER_DELETED: self._handle_customer_deleted,
            
            # Subscription events
            WebhookEventType.SUBSCRIPTION_CREATED: self._handle_subscription_created,
            WebhookEventType.SUBSCRIPTION_UPDATED: self._handle_subscription_updated,
            WebhookEventType.SUBSCRIPTION_DELETED: self._handle_subscription_deleted,
            WebhookEventType.SUBSCRIPTION_TRIAL_WILL_END: self._handle_trial_ending,
            
            # Invoice events
            WebhookEventType.INVOICE_CREATED: self._handle_invoice_created,
            WebhookEventType.INVOICE_FINALIZED: self._handle_invoice_finalized,
            WebhookEventType.INVOICE_PAYMENT_SUCCEEDED: self._handle_payment_succeeded,
            WebhookEventType.INVOICE_PAYMENT_FAILED: self._handle_payment_failed,
            WebhookEventType.INVOICE_UPCOMING: self._handle_upcoming_invoice,
            
            # Payment events
            WebhookEventType.PAYMENT_INTENT_SUCCEEDED: self._handle_payment_intent_succeeded,
            WebhookEventType.PAYMENT_INTENT_FAILED: self._handle_payment_intent_failed,
            WebhookEventType.PAYMENT_METHOD_ATTACHED: self._handle_payment_method_attached,
            
            # Charge events
            WebhookEventType.CHARGE_SUCCEEDED: self._handle_charge_succeeded,
            WebhookEventType.CHARGE_FAILED: self._handle_charge_failed,
            WebhookEventType.CHARGE_DISPUTE_CREATED: self._handle_dispute_created,
            
            # Card expiry
            WebhookEventType.SOURCE_EXPIRING: self._handle_card_expiring
        }
        
        handler = handler_mapping.get(event_type)
        if not handler:
            logger.warning(f"No handler for event type: {event_type}")
            return WebhookProcessingResult(
                success=True,
                event_type=event_type,
                processed_at=datetime.utcnow(),
                message="No handler configured for this event type"
            )
        
        try:
            result = await handler(event_data)
            await self._mark_webhook_processed(event['id'])
            
            return WebhookProcessingResult(
                success=True,
                event_type=event_type,
                processed_at=datetime.utcnow(),
                message=f"Successfully processed {event_type}",
                data=result
            )
            
        except Exception as e:
            logger.error(f"Handler failed for {event_type}: {str(e)}")
            await self._mark_webhook_failed(event['id'], str(e))
            
            return WebhookProcessingResult(
                success=False,
                event_type=event_type,
                processed_at=datetime.utcnow(),
                message=f"Handler failed for {event_type}",
                error=str(e)
            )
    
    # Event Handlers
    
    async def _handle_customer_created(self, customer_data: Dict) -> Dict:
        """Handle customer.created event"""
        async with self.db_pool.acquire() as conn:
            # Check if customer already exists
            existing = await conn.fetchval(
                "SELECT id FROM customers WHERE stripe_customer_id = $1",
                customer_data['id']
            )
            
            if existing:
                return {'action': 'customer_already_exists', 'customer_id': existing}
            
            # Create new customer
            customer_id = await conn.fetchval("""
                INSERT INTO customers (
                    email, first_name, last_name, stripe_customer_id,
                    billing_address, preferred_currency, lifecycle_stage
                ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING id
            """, 
                customer_data['email'],
                customer_data.get('name', '').split(' ')[0] if customer_data.get('name') else '',
                ' '.join(customer_data.get('name', '').split(' ')[1:]) if customer_data.get('name') else '',
                customer_data['id'],
                json.dumps(customer_data.get('address', {})),
                customer_data.get('currency', 'USD').upper(),
                'prospect'
            )
            
            logger.info(f"Created customer {customer_id} from Stripe customer {customer_data['id']}")
            return {'action': 'customer_created', 'customer_id': customer_id}
    
    async def _handle_customer_updated(self, customer_data: Dict) -> Dict:
        """Handle customer.updated event"""
        async with self.db_pool.acquire() as conn:
            result = await conn.execute("""
                UPDATE customers 
                SET email = $1, billing_address = $2, preferred_currency = $3,
                    updated_at = CURRENT_TIMESTAMP
                WHERE stripe_customer_id = $4
            """, 
                customer_data['email'],
                json.dumps(customer_data.get('address', {})),
                customer_data.get('currency', 'USD').upper(),
                customer_data['id']
            )
            
            return {'action': 'customer_updated', 'rows_affected': int(result.split()[-1])}
    
    async def _handle_subscription_created(self, subscription_data: Dict) -> Dict:
        """Handle customer.subscription.created event"""
        async with self.db_pool.acquire() as conn:
            # Get customer ID
            customer_id = await conn.fetchval(
                "SELECT id FROM customers WHERE stripe_customer_id = $1",
                subscription_data['customer']
            )
            
            if not customer_id:
                raise ValueError(f"Customer not found: {subscription_data['customer']}")
            
            # Get plan information
            price_id = subscription_data['items']['data'][0]['price']['id']
            price = stripe.Price.retrieve(price_id)
            
            # Create subscription
            subscription_id = await conn.fetchval("""
                INSERT INTO subscriptions (
                    customer_id, plan_id, stripe_subscription_id, status,
                    current_period_start, current_period_end, unit_amount,
                    trial_start, trial_end, quantity
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                RETURNING id
            """, 
                customer_id,
                price.metadata.get('plan_id', price_id),
                subscription_data['id'],
                subscription_data['status'],
                datetime.fromtimestamp(subscription_data['current_period_start']),
                datetime.fromtimestamp(subscription_data['current_period_end']),
                price.unit_amount / 100,  # Convert from cents
                datetime.fromtimestamp(subscription_data['trial_start']) if subscription_data.get('trial_start') else None,
                datetime.fromtimestamp(subscription_data['trial_end']) if subscription_data.get('trial_end') else None,
                subscription_data['items']['data'][0]['quantity']
            )
            
            # Update customer lifecycle stage
            lifecycle_stage = 'trial' if subscription_data.get('trial_end') else 'active'
            await conn.execute("""
                UPDATE customers 
                SET lifecycle_stage = $1, last_activity_at = CURRENT_TIMESTAMP
                WHERE id = $2
            """, lifecycle_stage, customer_id)
            
            logger.info(f"Created subscription {subscription_id} for customer {customer_id}")
            return {'action': 'subscription_created', 'subscription_id': subscription_id}
    
    async def _handle_subscription_updated(self, subscription_data: Dict) -> Dict:
        """Handle customer.subscription.updated event"""
        async with self.db_pool.acquire() as conn:
            # Update subscription
            result = await conn.execute("""
                UPDATE subscriptions 
                SET status = $1, current_period_start = $2, current_period_end = $3,
                    cancel_at = $4, canceled_at = $5, ended_at = $6,
                    updated_at = CURRENT_TIMESTAMP
                WHERE stripe_subscription_id = $7
            """, 
                subscription_data['status'],
                datetime.fromtimestamp(subscription_data['current_period_start']),
                datetime.fromtimestamp(subscription_data['current_period_end']),
                datetime.fromtimestamp(subscription_data['cancel_at']) if subscription_data.get('cancel_at') else None,
                datetime.fromtimestamp(subscription_data['canceled_at']) if subscription_data.get('canceled_at') else None,
                datetime.fromtimestamp(subscription_data['ended_at']) if subscription_data.get('ended_at') else None,
                subscription_data['id']
            )
            
            # Update customer lifecycle if subscription canceled
            if subscription_data['status'] in ['canceled', 'unpaid']:
                customer_id = await conn.fetchval(
                    "SELECT customer_id FROM subscriptions WHERE stripe_subscription_id = $1",
                    subscription_data['id']
                )
                if customer_id:
                    await conn.execute("""
                        UPDATE customers 
                        SET lifecycle_stage = 'churned', updated_at = CURRENT_TIMESTAMP
                        WHERE id = $1
                    """, customer_id)
            
            return {'action': 'subscription_updated', 'rows_affected': int(result.split()[-1])}
    
    async def _handle_payment_succeeded(self, invoice_data: Dict) -> Dict:
        """Handle invoice.payment_succeeded event"""
        async with self.db_pool.acquire() as conn:
            # Update invoice status
            await conn.execute("""
                UPDATE invoices 
                SET status = 'paid', amount_paid = $1, paid_at = $2,
                    updated_at = CURRENT_TIMESTAMP
                WHERE stripe_invoice_id = $3
            """, 
                invoice_data['amount_paid'] / 100,  # Convert from cents
                datetime.fromtimestamp(invoice_data['status_transitions']['paid_at']),
                invoice_data['id']
            )
            
            # Record successful payment transaction
            if invoice_data.get('payment_intent'):
                payment_intent = stripe.PaymentIntent.retrieve(invoice_data['payment_intent'])
                
                await conn.execute("""
                    INSERT INTO payment_transactions (
                        customer_id, invoice_id, payment_intent_id, amount, currency,
                        status, payment_method_type, net_amount, processing_fee
                    ) VALUES (
                        (SELECT customer_id FROM invoices WHERE stripe_invoice_id = $1),
                        (SELECT id FROM invoices WHERE stripe_invoice_id = $1),
                        $2, $3, $4, $5, $6, $7, $8
                    )
                """, 
                    invoice_data['id'],
                    payment_intent.id,
                    payment_intent.amount / 100,
                    payment_intent.currency.upper(),
                    'succeeded',
                    payment_intent.payment_method_types[0] if payment_intent.payment_method_types else 'unknown',
                    (payment_intent.amount - (payment_intent.application_fee_amount or 0)) / 100,
                    (payment_intent.application_fee_amount or 0) / 100
                )
            
            # Update customer LTV
            customer_id = await conn.fetchval(
                "SELECT customer_id FROM invoices WHERE stripe_invoice_id = $1",
                invoice_data['id']
            )
            
            if customer_id:
                await conn.execute("""
                    UPDATE customers 
                    SET total_lifetime_value = total_lifetime_value + $1,
                        last_activity_at = CURRENT_TIMESTAMP,
                        lifecycle_stage = CASE 
                            WHEN lifecycle_stage = 'trial' THEN 'active'
                            ELSE lifecycle_stage
                        END
                    WHERE id = $2
                """, invoice_data['amount_paid'] / 100, customer_id)
            
            logger.info(f"Processed successful payment for invoice {invoice_data['id']}")
            return {
                'action': 'payment_succeeded',
                'amount': invoice_data['amount_paid'] / 100,
                'customer_id': customer_id
            }
    
    async def _handle_payment_failed(self, invoice_data: Dict) -> Dict:
        """Handle invoice.payment_failed event with dunning trigger"""
        async with self.db_pool.acquire() as conn:
            # Update invoice status
            await conn.execute("""
                UPDATE invoices 
                SET status = 'open', attempt_count = attempt_count + 1,
                    next_payment_attempt = $1, updated_at = CURRENT_TIMESTAMP
                WHERE stripe_invoice_id = $2
            """, 
                datetime.fromtimestamp(invoice_data['next_payment_attempt']) if invoice_data.get('next_payment_attempt') else None,
                invoice_data['id']
            )
            
            # Get subscription and customer info
            subscription_info = await conn.fetchrow("""
                SELECT s.id as subscription_id, s.customer_id, c.churn_risk_score
                FROM subscriptions s
                JOIN customers c ON s.customer_id = c.id
                WHERE s.stripe_subscription_id = $1
            """, invoice_data.get('subscription'))
            
            if subscription_info:
                # Trigger dunning campaign
                from dunning_manager import dunning_manager
                campaign_id = await dunning_manager.create_dunning_campaign(
                    customer_id=subscription_info['customer_id'],
                    subscription_id=subscription_info['subscription_id'],
                    campaign_type='failed_payment',
                    trigger_data={
                        'invoice_id': invoice_data['id'],
                        'amount': invoice_data['amount_due'] / 100,
                        'attempt_count': invoice_data.get('attempt_count', 1),
                        'failure_code': invoice_data.get('last_finalization_error', {}).get('code'),
                        'failure_message': invoice_data.get('last_finalization_error', {}).get('message')
                    }
                )
                
                logger.info(f"Created dunning campaign {campaign_id} for failed payment {invoice_data['id']}")
                return {
                    'action': 'payment_failed_dunning_triggered',
                    'campaign_id': campaign_id,
                    'invoice_id': invoice_data['id']
                }
            
            return {'action': 'payment_failed_recorded', 'invoice_id': invoice_data['id']}
    
    async def _handle_trial_ending(self, subscription_data: Dict) -> Dict:
        """Handle customer.subscription.trial_will_end event"""
        # Trigger trial ending email campaign
        async with self.db_pool.acquire() as conn:
            customer_info = await conn.fetchrow("""
                SELECT c.id, c.email, c.first_name, s.id as subscription_id
                FROM customers c
                JOIN subscriptions s ON c.id = s.customer_id
                WHERE c.stripe_customer_id = $1
            """, subscription_data['customer'])
            
            if customer_info:
                # Create trial ending campaign
                from dunning_manager import dunning_manager
                campaign_id = await dunning_manager.create_dunning_campaign(
                    customer_id=customer_info['id'],
                    subscription_id=customer_info['subscription_id'],
                    campaign_type='trial_ending',
                    trigger_data={
                        'trial_end_date': subscription_data['trial_end'],
                        'subscription_id': subscription_data['id']
                    }
                )
                
                return {
                    'action': 'trial_ending_campaign_created',
                    'campaign_id': campaign_id
                }
        
        return {'action': 'trial_ending_processed'}
    
    async def _handle_card_expiring(self, source_data: Dict) -> Dict:
        """Handle customer.source.expiring event"""
        async with self.db_pool.acquire() as conn:
            customer_info = await conn.fetchrow("""
                SELECT id FROM customers WHERE stripe_customer_id = $1
            """, source_data['customer'])
            
            if customer_info:
                # Create card expiring campaign
                from dunning_manager import dunning_manager
                campaign_id = await dunning_manager.create_dunning_campaign(
                    customer_id=customer_info['id'],
                    subscription_id=None,
                    campaign_type='card_expiring',
                    trigger_data={
                        'card_exp_month': source_data.get('exp_month'),
                        'card_exp_year': source_data.get('exp_year'),
                        'card_last4': source_data.get('last4')
                    }
                )
                
                return {
                    'action': 'card_expiring_campaign_created',
                    'campaign_id': campaign_id
                }
        
        return {'action': 'card_expiring_processed'}
    
    # Additional handlers (abbreviated for space)
    
    async def _handle_customer_deleted(self, customer_data: Dict) -> Dict:
        """Handle customer.deleted event"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                UPDATE customers 
                SET lifecycle_stage = 'deleted', updated_at = CURRENT_TIMESTAMP
                WHERE stripe_customer_id = $1
            """, customer_data['id'])
        
        return {'action': 'customer_marked_deleted'}
    
    async def _handle_subscription_deleted(self, subscription_data: Dict) -> Dict:
        """Handle customer.subscription.deleted event"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                UPDATE subscriptions 
                SET status = 'canceled', ended_at = $1, updated_at = CURRENT_TIMESTAMP
                WHERE stripe_subscription_id = $2
            """, 
                datetime.fromtimestamp(subscription_data['ended_at']) if subscription_data.get('ended_at') else datetime.utcnow(),
                subscription_data['id']
            )
        
        return {'action': 'subscription_marked_deleted'}
    
    # Utility methods
    
    async def _is_duplicate_event(self, event_id: str) -> bool:
        """Check if webhook event has already been processed"""
        async with self.db_pool.acquire() as conn:
            result = await conn.fetchval(
                "SELECT processed FROM webhook_events WHERE event_id = $1",
                event_id
            )
            return result is True
    
    async def _store_webhook_event(self, event: Dict):
        """Store webhook event in database"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO webhook_events (
                    source, event_id, event_type, api_version, data, processed
                ) VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (event_id) DO NOTHING
            """, 
                'stripe',
                event['id'],
                event['type'],
                event.get('api_version'),
                json.dumps(event),
                False
            )
    
    async def _mark_webhook_processed(self, event_id: str):
        """Mark webhook event as successfully processed"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                UPDATE webhook_events 
                SET processed = TRUE, processed_at = CURRENT_TIMESTAMP
                WHERE event_id = $1
            """, event_id)
    
    async def _mark_webhook_failed(self, event_id: str, error_message: str):
        """Mark webhook event as failed with error message"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                UPDATE webhook_events 
                SET processed = FALSE, error_message = $1, processed_at = CURRENT_TIMESTAMP,
                    retry_count = retry_count + 1
                WHERE event_id = $2
            """, error_message, event_id)

# FastAPI app for webhook endpoints
app = FastAPI(title="Christopher's AI Coaching - Stripe Webhooks")

# Initialize webhook handler
webhook_handler = StripeWebhookHandler()

@app.on_event("startup")
async def startup_event():
    await webhook_handler.initialize()

@app.post("/webhooks/stripe")
async def handle_stripe_webhook(request: Request, background_tasks: BackgroundTasks):
    """Main Stripe webhook endpoint"""
    try:
        payload = await request.body()
        signature = request.headers.get('stripe-signature')
        
        if not signature:
            raise HTTPException(status_code=400, detail="Missing stripe-signature header")
        
        # Process webhook asynchronously
        result = await webhook_handler.process_webhook(payload, signature)
        
        if result.success:
            return JSONResponse(
                status_code=200,
                content={
                    'status': 'success',
                    'event_type': result.event_type,
                    'message': result.message,
                    'processed_at': result.processed_at.isoformat()
                }
            )
        else:
            return JSONResponse(
                status_code=400,
                content={
                    'status': 'error',
                    'event_type': result.event_type,
                    'message': result.message,
                    'error': result.error,
                    'processed_at': result.processed_at.isoformat()
                }
            )
    
    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                'status': 'error',
                'message': 'Internal server error',
                'error': str(e)
            }
        )

@app.get("/webhooks/stats")
async def get_webhook_stats():
    """Get webhook processing statistics"""
    return {
        'processing_stats': webhook_handler.processing_stats,
        'timestamp': datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)