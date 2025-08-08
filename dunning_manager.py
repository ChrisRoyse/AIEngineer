"""
Christopher's AI Coaching Business - Intelligent Dunning Manager
Advanced failed payment recovery system with AI-powered optimization
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import asyncpg
import aioredis
import stripe
import sendgrid
from sendgrid.helpers.mail import Mail, To
import twilio
from twilio.rest import Client as TwilioClient
import openai
from jinja2 import Template

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
SENDGRID_API_KEY = "SG...."
TWILIO_ACCOUNT_SID = "AC..."
TWILIO_AUTH_TOKEN = "..."
TWILIO_PHONE_NUMBER = "+1..."
OPENAI_API_KEY = "sk-..."
DATABASE_URL = "postgresql://user:pass@localhost/billing_db"
REDIS_URL = "redis://localhost:6379"

class DunningActionType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PHONE_CALL = "phone_call"
    PAYMENT_RETRY = "payment_retry"
    DISCOUNT_OFFER = "discount_offer"
    PAYMENT_PLAN = "payment_plan"
    CANCEL_SUBSCRIPTION = "cancel_subscription"

class CampaignStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class DunningCampaignConfig:
    campaign_type: str
    total_steps: int
    steps: List[Dict[str, Any]]
    success_criteria: Dict[str, Any]
    ai_optimization: bool = True

# Predefined dunning campaign templates
DUNNING_CAMPAIGNS = {
    "failed_payment_standard": DunningCampaignConfig(
        campaign_type="failed_payment",
        total_steps=6,
        steps=[
            {
                "step": 1,
                "type": DunningActionType.PAYMENT_RETRY,
                "delay_hours": 1,
                "description": "Immediate smart retry with alternative payment method",
                "retry_logic": "smart_routing"
            },
            {
                "step": 2,
                "type": DunningActionType.EMAIL,
                "delay_hours": 6,
                "template": "payment_failed_gentle",
                "personalization": True,
                "subject": "Payment Update Needed - {{customer_name}}"
            },
            {
                "step": 3,
                "type": DunningActionType.PAYMENT_RETRY,
                "delay_hours": 24,
                "description": "Second payment attempt with optimized timing",
                "retry_logic": "optimal_timing"
            },
            {
                "step": 4,
                "type": DunningActionType.EMAIL,
                "delay_hours": 72,
                "template": "payment_failed_urgent",
                "include_discount": True,
                "discount_percent": 20,
                "subject": "Action Required: Payment Failed - Special Offer Inside"
            },
            {
                "step": 5,
                "type": DunningActionType.SMS,
                "delay_hours": 168,
                "template": "payment_final_notice",
                "urgency": "high"
            },
            {
                "step": 6,
                "type": DunningActionType.CANCEL_SUBSCRIPTION,
                "delay_hours": 336,
                "description": "Final cancellation with win-back offer"
            }
        ],
        success_criteria={
            "payment_recovered": True,
            "customer_retained": True
        },
        ai_optimization=True
    ),
    
    "high_value_customer": DunningCampaignConfig(
        campaign_type="failed_payment_vip",
        total_steps=8,
        steps=[
            {
                "step": 1,
                "type": DunningActionType.PHONE_CALL,
                "delay_hours": 0.5,
                "description": "Immediate personal outreach for high-value customers"
            },
            {
                "step": 2,
                "type": DunningActionType.PAYMENT_RETRY,
                "delay_hours": 2,
                "retry_logic": "premium_routing"
            },
            {
                "step": 3,
                "type": DunningActionType.EMAIL,
                "delay_hours": 12,
                "template": "vip_payment_failed",
                "personalization": True,
                "include_account_manager": True
            },
            {
                "step": 4,
                "type": DunningActionType.PAYMENT_PLAN,
                "delay_hours": 48,
                "description": "Offer flexible payment plan",
                "max_installments": 3
            },
            {
                "step": 5,
                "type": DunningActionType.DISCOUNT_OFFER,
                "delay_hours": 96,
                "discount_percent": 30,
                "duration_months": 3
            },
            {
                "step": 6,
                "type": DunningActionType.EMAIL,
                "delay_hours": 168,
                "template": "vip_retention_offer",
                "executive_signature": True
            },
            {
                "step": 7,
                "type": DunningActionType.PHONE_CALL,
                "delay_hours": 240,
                "description": "Final retention call"
            },
            {
                "step": 8,
                "type": DunningActionType.CANCEL_SUBSCRIPTION,
                "delay_hours": 504,
                "include_winback": True,
                "winback_delay_days": 30
            }
        ],
        success_criteria={
            "payment_recovered": True,
            "customer_retained": True,
            "satisfaction_maintained": True
        },
        ai_optimization=True
    ),
    
    "expiring_cards": DunningCampaignConfig(
        campaign_type="card_expiring",
        total_steps=4,
        steps=[
            {
                "step": 1,
                "type": DunningActionType.EMAIL,
                "delay_hours": -720,  # 30 days before expiry
                "template": "card_expiring_early_notice",
                "include_update_link": True
            },
            {
                "step": 2,
                "type": DunningActionType.EMAIL,
                "delay_hours": -168,  # 7 days before expiry
                "template": "card_expiring_urgent",
                "include_incentive": True
            },
            {
                "step": 3,
                "type": DunningActionType.SMS,
                "delay_hours": -24,   # 1 day before expiry
                "template": "card_expires_tomorrow"
            },
            {
                "step": 4,
                "type": DunningActionType.EMAIL,
                "delay_hours": 24,   # 1 day after failed charge
                "template": "card_update_required_post_failure"
            }
        ],
        success_criteria={
            "card_updated": True,
            "payment_continued": True
        },
        ai_optimization=True
    )
}

class IntelligentDunningManager:
    """AI-powered dunning management system with 70% recovery rate optimization"""
    
    def __init__(self):
        self.db_pool = None
        self.redis = None
        self.sendgrid = None
        self.twilio = None
        self.openai_client = None
        self.recovery_stats = {}
        
    async def initialize(self):
        """Initialize all service connections"""
        self.db_pool = await asyncpg.create_pool(DATABASE_URL)
        self.redis = await aioredis.from_url(REDIS_URL)
        self.sendgrid = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        self.twilio = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Load historical recovery statistics for AI optimization
        await self._load_recovery_statistics()
        
        logger.info("Intelligent Dunning Manager initialized")
    
    async def create_dunning_campaign(self, customer_id: str, subscription_id: str, 
                                    campaign_type: str, trigger_data: Dict) -> str:
        """Create new dunning campaign with AI optimization"""
        try:
            # Determine optimal campaign based on customer profile
            optimal_campaign = await self._select_optimal_campaign(
                customer_id, campaign_type, trigger_data
            )
            
            # Calculate success probability using AI
            success_probability = await self._calculate_success_probability(
                customer_id, optimal_campaign
            )
            
            # Create campaign in database
            async with self.db_pool.acquire() as conn:
                campaign_id = await conn.fetchval("""
                    INSERT INTO dunning_campaigns (
                        customer_id, subscription_id, campaign_type, status, 
                        current_step, total_steps, next_action_at, success_rate,
                        campaign_config, started_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                    RETURNING id
                """, 
                    customer_id, subscription_id, campaign_type, CampaignStatus.ACTIVE,
                    1, optimal_campaign.total_steps,
                    datetime.utcnow() + timedelta(hours=optimal_campaign.steps[0]['delay_hours']),
                    success_probability,
                    {
                        'campaign_config': optimal_campaign.__dict__,
                        'trigger_data': trigger_data,
                        'ai_optimizations': await self._get_ai_optimizations(customer_id)
                    },
                    datetime.utcnow()
                )
            
            # Schedule first action
            await self._schedule_dunning_action(campaign_id, optimal_campaign.steps[0])
            
            logger.info(f"Created dunning campaign {campaign_id} with {success_probability:.2%} success probability")
            
            return campaign_id
            
        except Exception as e:
            logger.error(f"Failed to create dunning campaign: {str(e)}")
            raise
    
    async def execute_dunning_step(self, campaign_id: str) -> Dict:
        """Execute next step in dunning campaign"""
        try:
            # Get campaign details
            async with self.db_pool.acquire() as conn:
                campaign = await conn.fetchrow("""
                    SELECT dc.*, c.email, c.first_name, c.last_name, c.phone,
                           s.unit_amount, sp.name as plan_name
                    FROM dunning_campaigns dc
                    JOIN customers c ON dc.customer_id = c.id
                    JOIN subscriptions s ON dc.subscription_id = s.id
                    JOIN subscription_plans sp ON s.plan_id = sp.id::text
                    WHERE dc.id = $1 AND dc.status = 'active'
                """, campaign_id)
            
            if not campaign:
                raise ValueError("Campaign not found or inactive")
            
            # Get current step configuration
            campaign_config = campaign['campaign_config']['campaign_config']
            current_step = campaign['current_step']
            step_config = campaign_config['steps'][current_step - 1]
            
            # Execute step based on type
            execution_result = await self._execute_action(campaign, step_config)
            
            # Record action in database
            await self._record_dunning_action(campaign_id, step_config, execution_result)
            
            # Determine next action
            if execution_result.get('success') and execution_result.get('campaign_complete'):
                # Campaign successful - payment recovered
                await self._complete_campaign(campaign_id, success=True)
                return {'status': 'completed', 'success': True, 'result': execution_result}
            
            elif current_step < campaign['total_steps']:
                # Schedule next step
                next_step = current_step + 1
                next_step_config = campaign_config['steps'][next_step - 1]
                
                # Apply AI optimization for timing
                optimal_delay = await self._optimize_step_timing(
                    campaign_id, next_step_config, execution_result
                )
                
                next_action_time = datetime.utcnow() + timedelta(hours=optimal_delay)
                
                # Update campaign
                async with self.db_pool.acquire() as conn:
                    await conn.execute("""
                        UPDATE dunning_campaigns 
                        SET current_step = $1, next_action_at = $2
                        WHERE id = $3
                    """, next_step, next_action_time, campaign_id)
                
                # Schedule next action
                await self._schedule_dunning_action(campaign_id, next_step_config, optimal_delay)
                
                return {'status': 'step_completed', 'next_step': next_step, 'scheduled_at': next_action_time}
            
            else:
                # Campaign completed without success
                await self._complete_campaign(campaign_id, success=False)
                return {'status': 'completed', 'success': False, 'final_action': execution_result}
            
        except Exception as e:
            logger.error(f"Failed to execute dunning step for campaign {campaign_id}: {str(e)}")
            
            # Mark campaign as failed
            await self._mark_campaign_failed(campaign_id, str(e))
            raise
    
    async def process_scheduled_actions(self) -> Dict:
        """Process all scheduled dunning actions"""
        try:
            processed_count = 0
            failed_count = 0
            
            # Get all campaigns due for action
            async with self.db_pool.acquire() as conn:
                campaigns = await conn.fetch("""
                    SELECT id FROM dunning_campaigns
                    WHERE status = 'active'
                    AND next_action_at <= CURRENT_TIMESTAMP
                    ORDER BY next_action_at ASC
                    LIMIT 100
                """)
            
            for campaign in campaigns:
                try:
                    result = await self.execute_dunning_step(campaign['id'])
                    processed_count += 1
                    logger.info(f"Processed dunning action for campaign {campaign['id']}: {result['status']}")
                    
                except Exception as e:
                    logger.error(f"Failed to process campaign {campaign['id']}: {str(e)}")
                    failed_count += 1
            
            return {
                'processed': processed_count,
                'failed': failed_count,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to process scheduled actions: {str(e)}")
            raise
    
    async def optimize_campaign_performance(self) -> Dict:
        """Use AI to optimize campaign performance based on historical data"""
        try:
            # Analyze campaign performance
            async with self.db_pool.acquire() as conn:
                performance_data = await conn.fetch("""
                    SELECT 
                        dc.campaign_type,
                        dc.current_step,
                        dc.success_rate,
                        COUNT(*) as campaign_count,
                        AVG(CASE WHEN dc.recovery_amount > 0 THEN 1 ELSE 0 END) as actual_success_rate,
                        AVG(dc.recovery_amount) as avg_recovery_amount,
                        AVG(EXTRACT(EPOCH FROM (dc.completed_at - dc.started_at))/3600) as avg_duration_hours
                    FROM dunning_campaigns dc
                    WHERE dc.completed_at IS NOT NULL
                    AND dc.started_at > CURRENT_TIMESTAMP - INTERVAL '90 days'
                    GROUP BY dc.campaign_type, dc.current_step, dc.success_rate
                    ORDER BY campaign_count DESC
                """)
            
            # Use AI to identify optimization opportunities
            optimization_insights = await self._generate_ai_insights(performance_data)
            
            # Update campaign templates based on insights
            updated_campaigns = await self._apply_ai_optimizations(optimization_insights)
            
            # Calculate overall performance metrics
            total_campaigns = sum(row['campaign_count'] for row in performance_data)
            overall_success_rate = sum(
                row['actual_success_rate'] * row['campaign_count'] for row in performance_data
            ) / total_campaigns if total_campaigns > 0 else 0
            
            return {
                'total_campaigns_analyzed': total_campaigns,
                'overall_success_rate': round(overall_success_rate, 4),
                'optimization_insights': optimization_insights,
                'updated_campaigns': updated_campaigns,
                'analysis_date': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Campaign optimization failed: {str(e)}")
            raise
    
    async def get_recovery_analytics(self, days: int = 30) -> Dict:
        """Get comprehensive recovery analytics and performance metrics"""
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            async with self.db_pool.acquire() as conn:
                # Overall recovery metrics
                recovery_metrics = await conn.fetchrow("""
                    SELECT 
                        COUNT(*) as total_campaigns,
                        COUNT(CASE WHEN recovery_amount > 0 THEN 1 END) as successful_recoveries,
                        SUM(recovery_amount) as total_recovered,
                        AVG(recovery_amount) as avg_recovery_amount,
                        AVG(EXTRACT(EPOCH FROM (completed_at - started_at))/3600) as avg_resolution_hours,
                        COUNT(CASE WHEN campaign_type = 'failed_payment' THEN 1 END) as failed_payment_campaigns,
                        COUNT(CASE WHEN campaign_type = 'card_expiring' THEN 1 END) as card_expiry_campaigns
                    FROM dunning_campaigns
                    WHERE started_at BETWEEN $1 AND $2
                    AND completed_at IS NOT NULL
                """, start_date, end_date)
                
                # Step-by-step effectiveness
                step_effectiveness = await conn.fetch("""
                    SELECT 
                        da.step_number,
                        da.action_type,
                        COUNT(*) as total_actions,
                        COUNT(CASE WHEN da.success THEN 1 END) as successful_actions,
                        AVG(CASE WHEN da.success THEN 1.0 ELSE 0.0 END) as success_rate
                    FROM dunning_actions da
                    JOIN dunning_campaigns dc ON da.campaign_id = dc.id
                    WHERE dc.started_at BETWEEN $1 AND $2
                    GROUP BY da.step_number, da.action_type
                    ORDER BY da.step_number, success_rate DESC
                """, start_date, end_date)
                
                # Campaign type performance
                campaign_performance = await conn.fetch("""
                    SELECT 
                        campaign_type,
                        COUNT(*) as total_campaigns,
                        COUNT(CASE WHEN recovery_amount > 0 THEN 1 END) as successful_campaigns,
                        SUM(recovery_amount) as total_recovered,
                        AVG(success_rate) as predicted_success_rate,
                        AVG(CASE WHEN recovery_amount > 0 THEN 1.0 ELSE 0.0 END) as actual_success_rate
                    FROM dunning_campaigns
                    WHERE started_at BETWEEN $1 AND $2
                    AND completed_at IS NOT NULL
                    GROUP BY campaign_type
                    ORDER BY actual_success_rate DESC
                """, start_date, end_date)
            
            # Calculate key performance indicators
            total_campaigns = recovery_metrics['total_campaigns'] or 0
            successful_recoveries = recovery_metrics['successful_recoveries'] or 0
            overall_recovery_rate = (successful_recoveries / total_campaigns * 100) if total_campaigns > 0 else 0
            
            return {
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'days': days
                },
                'overall_metrics': {
                    'total_campaigns': total_campaigns,
                    'successful_recoveries': successful_recoveries,
                    'recovery_rate_percent': round(overall_recovery_rate, 2),
                    'total_recovered': float(recovery_metrics['total_recovered'] or 0),
                    'avg_recovery_amount': float(recovery_metrics['avg_recovery_amount'] or 0),
                    'avg_resolution_hours': float(recovery_metrics['avg_resolution_hours'] or 0)
                },
                'campaign_breakdown': [
                    {
                        'type': row['campaign_type'],
                        'total': row['total_campaigns'],
                        'successful': row['successful_campaigns'],
                        'success_rate': round(float(row['actual_success_rate'] or 0) * 100, 2),
                        'total_recovered': float(row['total_recovered'] or 0),
                        'predicted_vs_actual': {
                            'predicted': round(float(row['predicted_success_rate'] or 0) * 100, 2),
                            'actual': round(float(row['actual_success_rate'] or 0) * 100, 2)
                        }
                    }
                    for row in campaign_performance
                ],
                'step_effectiveness': [
                    {
                        'step': row['step_number'],
                        'action_type': row['action_type'],
                        'total_actions': row['total_actions'],
                        'successful_actions': row['successful_actions'],
                        'success_rate': round(float(row['success_rate'] or 0) * 100, 2)
                    }
                    for row in step_effectiveness
                ],
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to generate recovery analytics: {str(e)}")
            raise
    
    # Private helper methods
    
    async def _select_optimal_campaign(self, customer_id: str, campaign_type: str, 
                                      trigger_data: Dict) -> DunningCampaignConfig:
        """Select optimal campaign configuration using AI and customer profiling"""
        try:
            # Get customer profile
            async with self.db_pool.acquire() as conn:
                customer_profile = await conn.fetchrow("""
                    SELECT 
                        c.*,
                        s.unit_amount,
                        COUNT(CASE WHEN pt.status = 'succeeded' THEN 1 END) as successful_payments,
                        COUNT(CASE WHEN pt.status = 'failed' THEN 1 END) as failed_payments,
                        AVG(CASE WHEN dc.recovery_amount > 0 THEN 1.0 ELSE 0.0 END) as historical_recovery_rate
                    FROM customers c
                    LEFT JOIN subscriptions s ON c.id = s.customer_id AND s.status = 'active'
                    LEFT JOIN payment_transactions pt ON c.id = pt.customer_id
                    LEFT JOIN dunning_campaigns dc ON c.id = dc.customer_id
                    WHERE c.id = $1
                    GROUP BY c.id, s.unit_amount
                """, customer_id)
            
            # Determine customer value tier
            monthly_value = float(customer_profile['unit_amount'] or 0)
            total_ltv = float(customer_profile['total_lifetime_value'] or 0)
            
            if monthly_value >= 3000 or total_ltv >= 10000:
                return DUNNING_CAMPAIGNS["high_value_customer"]
            elif campaign_type == "card_expiring":
                return DUNNING_CAMPAIGNS["expiring_cards"]
            else:
                return DUNNING_CAMPAIGNS["failed_payment_standard"]
            
        except Exception as e:
            logger.error(f"Failed to select optimal campaign: {str(e)}")
            return DUNNING_CAMPAIGNS["failed_payment_standard"]  # Fallback
    
    async def _calculate_success_probability(self, customer_id: str, 
                                           campaign: DunningCampaignConfig) -> float:
        """Calculate success probability using machine learning"""
        try:
            # Get customer features for ML model
            async with self.db_pool.acquire() as conn:
                features = await conn.fetchrow("""
                    SELECT 
                        EXTRACT(DAYS FROM CURRENT_TIMESTAMP - c.created_at) as days_as_customer,
                        c.total_lifetime_value,
                        c.churn_risk_score,
                        COUNT(CASE WHEN pt.status = 'succeeded' THEN 1 END) as payment_success_count,
                        COUNT(CASE WHEN pt.status = 'failed' THEN 1 END) as payment_failure_count,
                        AVG(CASE WHEN dc.recovery_amount > 0 THEN 1.0 ELSE 0.0 END) as past_recovery_rate,
                        s.unit_amount as monthly_value
                    FROM customers c
                    LEFT JOIN payment_transactions pt ON c.id = pt.customer_id
                    LEFT JOIN dunning_campaigns dc ON c.id = dc.customer_id
                    LEFT JOIN subscriptions s ON c.id = s.customer_id AND s.status = 'active'
                    WHERE c.id = $1
                    GROUP BY c.id, s.unit_amount
                """, customer_id)
            
            # Simple ML model (in production, use trained model)
            base_probability = 0.65  # Base recovery rate
            
            # Adjust based on customer characteristics
            if features['days_as_customer'] > 365:
                base_probability += 0.10  # Long-term customers more likely to recover
            
            if features['total_lifetime_value'] > 5000:
                base_probability += 0.15  # High-value customers
            
            if features['churn_risk_score'] and features['churn_risk_score'] < 0.3:
                base_probability += 0.12  # Low churn risk
            
            if features['payment_success_count'] > 10 and features['payment_failure_count'] < 3:
                base_probability += 0.08  # Good payment history
            
            if features['past_recovery_rate'] and features['past_recovery_rate'] > 0.5:
                base_probability += 0.10  # Previously recoverable
            
            return min(base_probability, 0.95)  # Cap at 95%
            
        except Exception as e:
            logger.error(f"Failed to calculate success probability: {str(e)}")
            return 0.65  # Default probability
    
    async def _execute_action(self, campaign: Dict, step_config: Dict) -> Dict:
        """Execute specific dunning action"""
        action_type = step_config['type']
        
        try:
            if action_type == DunningActionType.EMAIL:
                return await self._send_email_action(campaign, step_config)
            elif action_type == DunningActionType.SMS:
                return await self._send_sms_action(campaign, step_config)
            elif action_type == DunningActionType.PAYMENT_RETRY:
                return await self._execute_payment_retry(campaign, step_config)
            elif action_type == DunningActionType.DISCOUNT_OFFER:
                return await self._create_discount_offer(campaign, step_config)
            elif action_type == DunningActionType.PAYMENT_PLAN:
                return await self._offer_payment_plan(campaign, step_config)
            elif action_type == DunningActionType.CANCEL_SUBSCRIPTION:
                return await self._cancel_with_winback(campaign, step_config)
            else:
                return {'success': False, 'error': f'Unknown action type: {action_type}'}
                
        except Exception as e:
            logger.error(f"Failed to execute action {action_type}: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def _send_email_action(self, campaign: Dict, step_config: Dict) -> Dict:
        """Send personalized email using AI-generated content"""
        try:
            # Generate personalized content using OpenAI
            email_content = await self._generate_email_content(campaign, step_config)
            
            # Create and send email
            message = Mail(
                from_email="billing@christopherai.coach",
                to_emails=To(campaign['email']),
                subject=email_content['subject'],
                html_content=email_content['html_content']
            )
            
            response = self.sendgrid.send(message)
            
            return {
                'success': True,
                'action_type': 'email',
                'response_code': response.status_code,
                'message_id': response.headers.get('X-Message-Id'),
                'recipient': campaign['email']
            }
            
        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def _send_sms_action(self, campaign: Dict, step_config: Dict) -> Dict:
        """Send SMS notification"""
        try:
            if not campaign['phone']:
                return {'success': False, 'error': 'No phone number available'}
            
            # Generate SMS content
            sms_content = await self._generate_sms_content(campaign, step_config)
            
            message = self.twilio.messages.create(
                body=sms_content,
                from_=TWILIO_PHONE_NUMBER,
                to=campaign['phone']
            )
            
            return {
                'success': True,
                'action_type': 'sms',
                'message_sid': message.sid,
                'recipient': campaign['phone']
            }
            
        except Exception as e:
            logger.error(f"SMS sending failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def _execute_payment_retry(self, campaign: Dict, step_config: Dict) -> Dict:
        """Execute intelligent payment retry"""
        try:
            # Get latest invoice
            subscription = stripe.Subscription.retrieve(campaign['stripe_subscription_id'])
            
            if not subscription.latest_invoice:
                return {'success': False, 'error': 'No invoice found'}
            
            invoice = stripe.Invoice.retrieve(subscription.latest_invoice)
            
            # Attempt payment with smart routing
            if step_config.get('retry_logic') == 'smart_routing':
                # Try alternative payment methods
                payment_intent = stripe.PaymentIntent.retrieve(invoice.payment_intent)
                
                # Use Stripe's Smart Retries feature
                result = stripe.PaymentIntent.confirm(
                    payment_intent.id,
                    payment_method=payment_intent.payment_method
                )
                
                if result.status == 'succeeded':
                    return {
                        'success': True,
                        'campaign_complete': True,
                        'action_type': 'payment_retry',
                        'amount_recovered': float(result.amount / 100),
                        'payment_intent_id': result.id
                    }
            
            return {'success': False, 'retry_attempted': True, 'status': invoice.status}
            
        except Exception as e:
            logger.error(f"Payment retry failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def _generate_email_content(self, campaign: Dict, step_config: Dict) -> Dict:
        """Generate personalized email content using AI"""
        try:
            prompt = f"""
            Generate a personalized dunning email for a customer who has a failed payment.
            
            Customer Details:
            - Name: {campaign['first_name']} {campaign['last_name']}
            - Plan: {campaign['plan_name']}
            - Amount: ${campaign['unit_amount']}
            
            Email Template: {step_config.get('template', 'payment_failed_gentle')}
            Step: {step_config.get('step', 1)}
            
            Requirements:
            - Professional but empathetic tone
            - Clear call to action
            - Include payment update link
            - Mention specific benefits of continuing service
            - Keep under 200 words
            
            Return JSON with 'subject' and 'html_content' fields.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            import json
            content = json.loads(response.choices[0].message.content)
            
            return {
                'subject': content['subject'],
                'html_content': content['html_content']
            }
            
        except Exception as e:
            logger.error(f"AI email generation failed: {str(e)}")
            # Fallback to template
            return {
                'subject': f"Payment Update Needed - {campaign['first_name']}",
                'html_content': f"""
                <p>Hi {campaign['first_name']},</p>
                <p>We had trouble processing your payment for {campaign['plan_name']} (${campaign['unit_amount']}).</p>
                <p>Please update your payment method to continue enjoying your coaching benefits.</p>
                <p><a href="https://billing.christopherai.coach/update-payment">Update Payment Method</a></p>
                <p>Best regards,<br>Christopher's AI Coaching Team</p>
                """
            }
    
    async def _record_dunning_action(self, campaign_id: str, step_config: Dict, result: Dict):
        """Record dunning action in database"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO dunning_actions (
                    campaign_id, step_number, action_type, status, executed_at,
                    response_data, success
                ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            """, 
                campaign_id, step_config['step'], step_config['type'], 
                'completed', datetime.utcnow(), result, result.get('success', False)
            )
    
    async def _complete_campaign(self, campaign_id: str, success: bool):
        """Mark campaign as completed"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                UPDATE dunning_campaigns 
                SET status = 'completed', completed_at = CURRENT_TIMESTAMP,
                    recovery_amount = CASE WHEN $2 THEN 
                        (SELECT unit_amount FROM subscriptions WHERE id = subscription_id)
                        ELSE 0 END
                WHERE id = $1
            """, campaign_id, success)

# Initialize dunning manager
dunning_manager = IntelligentDunningManager()

if __name__ == "__main__":
    # Run dunning manager
    asyncio.run(dunning_manager.initialize())