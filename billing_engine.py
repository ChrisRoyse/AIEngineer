"""
Christopher's AI Coaching Business - Billing Engine
Comprehensive automated billing system with Stripe integration and revenue optimization
"""

import asyncio
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import stripe
import paypalrestsdk
import asyncpg
import aioredis
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
import httpx
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
STRIPE_SECRET_KEY = "sk_live_..."  # Set via environment variable
STRIPE_PUBLISHABLE_KEY = "pk_live_..."
PAYPAL_CLIENT_ID = "..."
PAYPAL_CLIENT_SECRET = "..."
DATABASE_URL = "postgresql://user:pass@localhost/billing_db"
REDIS_URL = "redis://localhost:6379"

# Initialize Stripe
stripe.api_key = STRIPE_SECRET_KEY

class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    TRIALING = "trialing"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    UNPAID = "unpaid"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"

@dataclass
class SubscriptionPlan:
    id: str
    name: str
    price: Decimal
    currency: str
    interval: str  # monthly, quarterly, annually
    trial_days: int = 0
    features: Dict[str, Any] = None

# Predefined subscription plans for Christopher's coaching business
COACHING_PLANS = {
    "elite_coaching": SubscriptionPlan(
        id="elite_coaching",
        name="Elite 1:1 Coaching",
        price=Decimal("5000.00"),
        currency="USD",
        interval="monthly",
        trial_days=7,
        features={
            "weekly_sessions": 4,
            "priority_support": True,
            "custom_materials": True,
            "unlimited_messaging": True
        }
    ),
    "group_coaching": SubscriptionPlan(
        id="group_coaching",
        name="Group Coaching Programs",
        price=Decimal("1500.00"),
        currency="USD",
        interval="monthly",
        trial_days=14,
        features={
            "weekly_sessions": 2,
            "group_size": 8,
            "community_access": True,
            "resource_library": True
        }
    ),
    "community_access": SubscriptionPlan(
        id="community_access",
        name="Community Access",
        price=Decimal("97.00"),
        currency="USD",
        interval="monthly",
        trial_days=30,
        features={
            "forum_access": True,
            "monthly_webinars": True,
            "resource_downloads": True
        }
    ),
    "self_paced_course": SubscriptionPlan(
        id="self_paced_course",
        name="Self-Paced Courses",
        price=Decimal("997.00"),
        currency="USD",
        interval="one_time",
        features={
            "lifetime_access": True,
            "all_modules": True,
            "downloadable_content": True,
            "certificate": True
        }
    )
}

class BillingEngine:
    """Core billing engine with automated processing and revenue optimization"""
    
    def __init__(self):
        self.db_pool = None
        self.redis = None
        
    async def initialize(self):
        """Initialize database connections and Redis"""
        self.db_pool = await asyncpg.create_pool(DATABASE_URL)
        self.redis = await aioredis.from_url(REDIS_URL)
        logger.info("Billing engine initialized")
    
    async def create_customer(self, email: str, name: str, payment_method_id: str = None) -> Dict:
        """Create new customer in Stripe and local database"""
        try:
            # Create Stripe customer
            stripe_customer = stripe.Customer.create(
                email=email,
                name=name,
                payment_method=payment_method_id,
                invoice_settings={
                    'default_payment_method': payment_method_id,
                },
                metadata={
                    'created_by': 'billing_engine',
                    'business': 'christopher_ai_coaching'
                }
            )
            
            # Store in database
            async with self.db_pool.acquire() as conn:
                customer_id = await conn.fetchval("""
                    INSERT INTO customers (email, first_name, last_name, stripe_customer_id)
                    VALUES ($1, $2, $3, $4)
                    RETURNING id
                """, email, name.split()[0], name.split()[-1], stripe_customer.id)
            
            logger.info(f"Created customer {customer_id} for {email}")
            return {
                'customer_id': customer_id,
                'stripe_customer_id': stripe_customer.id,
                'email': email
            }
            
        except Exception as e:
            logger.error(f"Failed to create customer {email}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    
    async def create_subscription(self, customer_id: str, plan_id: str, 
                                discount_code: str = None) -> Dict:
        """Create new subscription with intelligent pricing and trial handling"""
        try:
            plan = COACHING_PLANS.get(plan_id)
            if not plan:
                raise HTTPException(status_code=404, detail="Plan not found")
            
            # Get customer from database
            async with self.db_pool.acquire() as conn:
                customer_data = await conn.fetchrow("""
                    SELECT stripe_customer_id, email, lifecycle_stage
                    FROM customers WHERE id = $1
                """, customer_id)
            
            if not customer_data:
                raise HTTPException(status_code=404, detail="Customer not found")
            
            # Create Stripe price if it doesn't exist
            stripe_price = await self._ensure_stripe_price(plan)
            
            # Apply discount if provided
            coupon_id = None
            if discount_code:
                coupon_id = await self._validate_discount_code(discount_code, plan_id)
            
            # Create subscription
            subscription_params = {
                'customer': customer_data['stripe_customer_id'],
                'items': [{'price': stripe_price.id}],
                'payment_behavior': 'default_incomplete',
                'payment_settings': {
                    'save_default_payment_method': 'on_subscription'
                },
                'expand': ['latest_invoice.payment_intent'],
                'metadata': {
                    'plan_id': plan_id,
                    'customer_id': str(customer_id),
                    'created_by': 'billing_engine'
                }
            }
            
            # Add trial period if applicable
            if plan.trial_days > 0:
                subscription_params['trial_period_days'] = plan.trial_days
            
            # Add coupon if validated
            if coupon_id:
                subscription_params['coupon'] = coupon_id
            
            stripe_subscription = stripe.Subscription.create(**subscription_params)
            
            # Store subscription in database
            async with self.db_pool.acquire() as conn:
                subscription_id = await conn.fetchval("""
                    INSERT INTO subscriptions (
                        customer_id, plan_id, stripe_subscription_id, status,
                        current_period_start, current_period_end, unit_amount,
                        trial_start, trial_end
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                    RETURNING id
                """, 
                    customer_id, plan_id, stripe_subscription.id, stripe_subscription.status,
                    datetime.fromtimestamp(stripe_subscription.current_period_start),
                    datetime.fromtimestamp(stripe_subscription.current_period_end),
                    plan.price,
                    datetime.fromtimestamp(stripe_subscription.trial_start) if stripe_subscription.trial_start else None,
                    datetime.fromtimestamp(stripe_subscription.trial_end) if stripe_subscription.trial_end else None
                )
            
            # Update customer lifecycle stage
            await self._update_customer_lifecycle(customer_id, 'trial' if plan.trial_days > 0 else 'active')
            
            logger.info(f"Created subscription {subscription_id} for customer {customer_id}")
            
            return {
                'subscription_id': subscription_id,
                'stripe_subscription_id': stripe_subscription.id,
                'status': stripe_subscription.status,
                'client_secret': stripe_subscription.latest_invoice.payment_intent.client_secret if stripe_subscription.latest_invoice else None
            }
            
        except Exception as e:
            logger.error(f"Failed to create subscription: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    
    async def process_recurring_billing(self) -> Dict:
        """Process all recurring billing automatically with intelligent retry logic"""
        try:
            processed_count = 0
            failed_count = 0
            
            # Get all active subscriptions due for billing
            async with self.db_pool.acquire() as conn:
                subscriptions = await conn.fetch("""
                    SELECT s.*, c.stripe_customer_id, c.email, c.churn_risk_score
                    FROM subscriptions s
                    JOIN customers c ON s.customer_id = c.id
                    WHERE s.status IN ('active', 'trialing')
                    AND s.current_period_end <= CURRENT_TIMESTAMP + INTERVAL '1 day'
                    AND s.stripe_subscription_id IS NOT NULL
                """)
            
            for sub in subscriptions:
                try:
                    # Retrieve latest subscription from Stripe
                    stripe_sub = stripe.Subscription.retrieve(sub['stripe_subscription_id'])
                    
                    if stripe_sub.status == 'active':
                        # Process successful renewal
                        await self._handle_successful_renewal(sub, stripe_sub)
                        processed_count += 1
                    elif stripe_sub.status in ['past_due', 'unpaid']:
                        # Handle failed payment
                        await self._handle_failed_payment(sub, stripe_sub)
                        failed_count += 1
                    
                except Exception as e:
                    logger.error(f"Failed to process subscription {sub['id']}: {str(e)}")
                    failed_count += 1
            
            logger.info(f"Processed {processed_count} renewals, {failed_count} failures")
            
            return {
                'processed_renewals': processed_count,
                'failed_payments': failed_count,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Recurring billing process failed: {str(e)}")
            raise
    
    async def handle_failed_payment(self, subscription_id: str, invoice_id: str) -> Dict:
        """Handle failed payments with intelligent dunning management"""
        try:
            # Get subscription and customer data
            async with self.db_pool.acquire() as conn:
                sub_data = await conn.fetchrow("""
                    SELECT s.*, c.email, c.stripe_customer_id, c.churn_risk_score
                    FROM subscriptions s
                    JOIN customers c ON s.customer_id = c.id
                    WHERE s.id = $1
                """, subscription_id)
            
            if not sub_data:
                raise HTTPException(status_code=404, detail="Subscription not found")
            
            # Create dunning campaign
            campaign_id = await self._create_dunning_campaign(sub_data, 'failed_payment')
            
            # Attempt smart retry based on failure reason
            stripe_invoice = stripe.Invoice.retrieve(invoice_id)
            retry_success = await self._attempt_smart_retry(stripe_invoice, sub_data)
            
            if retry_success:
                # Cancel dunning campaign if retry successful
                await self._complete_dunning_campaign(campaign_id, success=True)
                return {'status': 'recovered', 'method': 'smart_retry'}
            
            # Start dunning sequence
            await self._execute_dunning_step(campaign_id, 1)
            
            return {
                'status': 'dunning_started',
                'campaign_id': campaign_id,
                'estimated_recovery_rate': await self._calculate_recovery_probability(sub_data)
            }
            
        except Exception as e:
            logger.error(f"Failed payment handling failed: {str(e)}")
            raise
    
    async def calculate_revenue_metrics(self, start_date: datetime, end_date: datetime) -> Dict:
        """Calculate comprehensive revenue metrics and analytics"""
        try:
            async with self.db_pool.acquire() as conn:
                # Monthly Recurring Revenue (MRR)
                mrr_data = await conn.fetchrow("""
                    SELECT 
                        SUM(
                            CASE 
                                WHEN sp.billing_interval = 'monthly' THEN s.unit_amount
                                WHEN sp.billing_interval = 'quarterly' THEN s.unit_amount / 3
                                WHEN sp.billing_interval = 'annually' THEN s.unit_amount / 12
                                ELSE 0
                            END
                        ) as current_mrr
                    FROM subscriptions s
                    JOIN subscription_plans sp ON s.plan_id = sp.id::text
                    WHERE s.status = 'active'
                """)
                
                # Customer metrics
                customer_metrics = await conn.fetchrow("""
                    SELECT 
                        COUNT(CASE WHEN lifecycle_stage = 'active' THEN 1 END) as active_customers,
                        COUNT(CASE WHEN created_at >= $1 THEN 1 END) as new_customers,
                        COUNT(CASE WHEN lifecycle_stage = 'churned' 
                                   AND updated_at >= $1 THEN 1 END) as churned_customers,
                        AVG(total_lifetime_value) as avg_ltv,
                        AVG(churn_risk_score) as avg_churn_risk
                    FROM customers
                    WHERE created_at <= $2
                """, start_date, end_date)
                
                # Payment metrics
                payment_metrics = await conn.fetchrow("""
                    SELECT 
                        COUNT(CASE WHEN status = 'succeeded' THEN 1 END) as successful_payments,
                        COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_payments,
                        SUM(CASE WHEN status = 'succeeded' THEN amount ELSE 0 END) as total_revenue,
                        AVG(CASE WHEN status = 'succeeded' THEN amount END) as avg_transaction_size
                    FROM payment_transactions
                    WHERE created_at BETWEEN $1 AND $2
                """, start_date, end_date)
                
                # Calculate derived metrics
                total_payments = payment_metrics['successful_payments'] + payment_metrics['failed_payments']
                payment_success_rate = (
                    payment_metrics['successful_payments'] / total_payments * 100
                    if total_payments > 0 else 0
                )
                
                # Calculate churn rate
                churn_rate = (
                    customer_metrics['churned_customers'] / 
                    (customer_metrics['active_customers'] + customer_metrics['churned_customers']) * 100
                    if (customer_metrics['active_customers'] + customer_metrics['churned_customers']) > 0 else 0
                )
                
                # Annual Recurring Revenue (ARR)
                arr = mrr_data['current_mrr'] * 12 if mrr_data['current_mrr'] else 0
                
                metrics = {
                    'period': {'start': start_date.isoformat(), 'end': end_date.isoformat()},
                    'revenue': {
                        'mrr': float(mrr_data['current_mrr'] or 0),
                        'arr': float(arr),
                        'total_revenue': float(payment_metrics['total_revenue'] or 0),
                        'avg_transaction_size': float(payment_metrics['avg_transaction_size'] or 0)
                    },
                    'customers': {
                        'active': customer_metrics['active_customers'],
                        'new': customer_metrics['new_customers'],
                        'churned': customer_metrics['churned_customers'],
                        'churn_rate': round(churn_rate, 2),
                        'avg_ltv': float(customer_metrics['avg_ltv'] or 0),
                        'avg_churn_risk': float(customer_metrics['avg_churn_risk'] or 0)
                    },
                    'payments': {
                        'successful': payment_metrics['successful_payments'],
                        'failed': payment_metrics['failed_payments'],
                        'success_rate': round(payment_success_rate, 2)
                    },
                    'calculated_at': datetime.utcnow().isoformat()
                }
                
                # Store metrics in database
                await self._store_revenue_metrics(metrics)
                
                return metrics
                
        except Exception as e:
            logger.error(f"Revenue metrics calculation failed: {str(e)}")
            raise
    
    # Private helper methods
    
    async def _ensure_stripe_price(self, plan: SubscriptionPlan) -> stripe.Price:
        """Ensure Stripe price exists for the plan"""
        try:
            # Try to find existing price
            prices = stripe.Price.list(
                product=f"christopher_coaching_{plan.id}",
                active=True
            )
            
            if prices.data:
                return prices.data[0]
            
            # Create product first
            product = stripe.Product.create(
                id=f"christopher_coaching_{plan.id}",
                name=plan.name,
                description=f"Christopher's AI Coaching - {plan.name}",
                metadata={
                    'plan_id': plan.id,
                    'business': 'christopher_ai_coaching'
                }
            )
            
            # Create price
            price_params = {
                'unit_amount': int(plan.price * 100),  # Stripe uses cents
                'currency': plan.currency.lower(),
                'product': product.id,
                'metadata': {
                    'plan_id': plan.id
                }
            }
            
            if plan.interval != 'one_time':
                price_params['recurring'] = {'interval': plan.interval}
            
            return stripe.Price.create(**price_params)
            
        except Exception as e:
            logger.error(f"Failed to ensure Stripe price for {plan.id}: {str(e)}")
            raise
    
    async def _validate_discount_code(self, code: str, plan_id: str) -> Optional[str]:
        """Validate discount code and return Stripe coupon ID"""
        try:
            async with self.db_pool.acquire() as conn:
                discount = await conn.fetchrow("""
                    SELECT * FROM discounts
                    WHERE code = $1 AND is_active = TRUE
                    AND (valid_until IS NULL OR valid_until > CURRENT_TIMESTAMP)
                    AND (max_redemptions IS NULL OR redemptions_count < max_redemptions)
                """, code)
            
            if not discount:
                return None
            
            # Check if discount applies to this plan
            if discount['applies_to'] == 'specific_plans':
                if plan_id not in discount['applicable_plans']:
                    return None
            
            # Create or retrieve Stripe coupon
            coupon_id = f"discount_{discount['id']}"
            
            try:
                coupon = stripe.Coupon.retrieve(coupon_id)
            except stripe.error.InvalidRequestError:
                # Create coupon in Stripe
                coupon_params = {
                    'id': coupon_id,
                    'name': discount['name'],
                    'metadata': {'discount_id': str(discount['id'])}
                }
                
                if discount['type'] == 'percentage':
                    coupon_params['percent_off'] = float(discount['value'])
                else:
                    coupon_params['amount_off'] = int(discount['value'] * 100)
                    coupon_params['currency'] = 'usd'
                
                if discount['duration'] == 'once':
                    coupon_params['duration'] = 'once'
                elif discount['duration'] == 'repeating':
                    coupon_params['duration'] = 'repeating'
                    coupon_params['duration_in_months'] = discount['duration_in_months']
                else:
                    coupon_params['duration'] = 'forever'
                
                coupon = stripe.Coupon.create(**coupon_params)
            
            # Increment redemption count
            await conn.execute("""
                UPDATE discounts SET redemptions_count = redemptions_count + 1
                WHERE id = $1
            """, discount['id'])
            
            return coupon_id
            
        except Exception as e:
            logger.error(f"Failed to validate discount code {code}: {str(e)}")
            return None
    
    async def _update_customer_lifecycle(self, customer_id: str, stage: str):
        """Update customer lifecycle stage"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                UPDATE customers 
                SET lifecycle_stage = $1, last_activity_at = CURRENT_TIMESTAMP
                WHERE id = $2
            """, stage, customer_id)
    
    async def _handle_successful_renewal(self, subscription: Dict, stripe_sub: stripe.Subscription):
        """Handle successful subscription renewal"""
        async with self.db_pool.acquire() as conn:
            # Update subscription period
            await conn.execute("""
                UPDATE subscriptions 
                SET current_period_start = $1, current_period_end = $2, updated_at = CURRENT_TIMESTAMP
                WHERE id = $3
            """, 
                datetime.fromtimestamp(stripe_sub.current_period_start),
                datetime.fromtimestamp(stripe_sub.current_period_end),
                subscription['id']
            )
            
            # Update customer LTV
            plan = COACHING_PLANS.get(subscription['plan_id'])
            if plan:
                await conn.execute("""
                    UPDATE customers 
                    SET total_lifetime_value = total_lifetime_value + $1,
                        last_activity_at = CURRENT_TIMESTAMP
                    WHERE id = $2
                """, plan.price, subscription['customer_id'])
    
    async def _handle_failed_payment(self, subscription: Dict, stripe_sub: stripe.Subscription):
        """Handle failed payment with smart retry logic"""
        # Update subscription status
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                UPDATE subscriptions 
                SET status = $1, updated_at = CURRENT_TIMESTAMP
                WHERE id = $2
            """, stripe_sub.status, subscription['id'])
        
        # Start dunning campaign
        await self._create_dunning_campaign(subscription, 'failed_payment')
    
    async def _create_dunning_campaign(self, subscription_data: Dict, campaign_type: str) -> str:
        """Create intelligent dunning campaign"""
        async with self.db_pool.acquire() as conn:
            campaign_id = await conn.fetchval("""
                INSERT INTO dunning_campaigns (
                    customer_id, subscription_id, campaign_type, status, total_steps,
                    next_action_at, campaign_config
                ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING id
            """, 
                subscription_data['customer_id'],
                subscription_data['id'],
                campaign_type,
                'active',
                5,  # 5-step dunning process
                datetime.utcnow() + timedelta(hours=2),  # First action in 2 hours
                {
                    'steps': [
                        {'type': 'email', 'delay_hours': 2, 'template': 'payment_failed_gentle'},
                        {'type': 'payment_retry', 'delay_hours': 24, 'smart_retry': True},
                        {'type': 'email', 'delay_hours': 72, 'template': 'payment_failed_urgent'},
                        {'type': 'sms', 'delay_hours': 168, 'template': 'payment_final_notice'},
                        {'type': 'cancel_subscription', 'delay_hours': 336}
                    ]
                }
            )
        
        return campaign_id
    
    async def _store_revenue_metrics(self, metrics: Dict):
        """Store calculated revenue metrics in database"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO revenue_metrics (
                    metric_date, metric_type, mrr, arr, active_customers, new_customers,
                    churned_customers, total_revenue, successful_payments, failed_payments,
                    payment_success_rate, avg_revenue_per_customer, customer_ltv
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                ON CONFLICT (metric_date, metric_type) 
                DO UPDATE SET
                    mrr = EXCLUDED.mrr,
                    arr = EXCLUDED.arr,
                    active_customers = EXCLUDED.active_customers,
                    new_customers = EXCLUDED.new_customers,
                    churned_customers = EXCLUDED.churned_customers,
                    total_revenue = EXCLUDED.total_revenue,
                    successful_payments = EXCLUDED.successful_payments,
                    failed_payments = EXCLUDED.failed_payments,
                    payment_success_rate = EXCLUDED.payment_success_rate,
                    avg_revenue_per_customer = EXCLUDED.avg_revenue_per_customer,
                    customer_ltv = EXCLUDED.customer_ltv
            """, 
                datetime.utcnow().date(),
                'daily',
                Decimal(str(metrics['revenue']['mrr'])),
                Decimal(str(metrics['revenue']['arr'])),
                metrics['customers']['active'],
                metrics['customers']['new'],
                metrics['customers']['churned'],
                Decimal(str(metrics['revenue']['total_revenue'])),
                metrics['payments']['successful'],
                metrics['payments']['failed'],
                Decimal(str(metrics['payments']['success_rate'])),
                Decimal(str(metrics['revenue']['avg_transaction_size'])),
                Decimal(str(metrics['customers']['avg_ltv']))
            )

# Initialize billing engine
billing_engine = BillingEngine()

# FastAPI app for webhook handling and API endpoints
app = FastAPI(title="Christopher's AI Coaching - Billing System")

@app.on_event("startup")
async def startup_event():
    await billing_engine.initialize()

@app.post("/webhooks/stripe")
async def handle_stripe_webhook(request):
    """Handle Stripe webhook events for real-time billing updates"""
    # Implementation for Stripe webhook handling
    pass

@app.post("/create-customer")
async def create_customer_endpoint(email: EmailStr, name: str):
    """Create new customer"""
    return await billing_engine.create_customer(email, name)

@app.post("/create-subscription")
async def create_subscription_endpoint(customer_id: str, plan_id: str, discount_code: str = None):
    """Create new subscription"""
    return await billing_engine.create_subscription(customer_id, plan_id, discount_code)

@app.get("/revenue-metrics")
async def get_revenue_metrics():
    """Get current revenue metrics"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    return await billing_engine.calculate_revenue_metrics(start_date, end_date)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)