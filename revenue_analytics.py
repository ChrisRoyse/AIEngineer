"""
Christopher's AI Coaching Business - Revenue Analytics Engine
Comprehensive revenue tracking, forecasting, and business intelligence system
"""

import asyncio
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import asyncpg
import aioredis
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RevenueMetrics:
    mrr: Decimal
    arr: Decimal
    new_mrr: Decimal
    expansion_mrr: Decimal
    contraction_mrr: Decimal
    churn_mrr: Decimal
    net_new_mrr: Decimal
    active_customers: int
    new_customers: int
    churned_customers: int
    total_revenue: Decimal
    payment_success_rate: float
    avg_revenue_per_customer: Decimal
    customer_ltv: Decimal
    churn_rate: float

class RevenueAnalyticsEngine:
    """Advanced revenue analytics with predictive modeling and business intelligence"""
    
    def __init__(self, db_url: str, redis_url: str):
        self.db_url = db_url
        self.redis_url = redis_url
        self.db_pool = None
        self.redis = None
        self.models = {}
        self.cached_metrics = {}
        
    async def initialize(self):
        """Initialize database connections and ML models"""
        self.db_pool = await asyncpg.create_pool(self.db_url)
        self.redis = await aioredis.from_url(self.redis_url)
        
        # Initialize ML models
        await self._initialize_ml_models()
        
        logger.info("Revenue Analytics Engine initialized")
    
    async def calculate_comprehensive_metrics(self, start_date: datetime, 
                                            end_date: datetime) -> Dict[str, Any]:
        """Calculate comprehensive revenue metrics with advanced analytics"""
        try:
            # Check cache first
            cache_key = f"revenue_metrics:{start_date.date()}:{end_date.date()}"
            cached_result = await self.redis.get(cache_key)
            
            if cached_result:
                return json.loads(cached_result)
            
            # Calculate core metrics
            core_metrics = await self._calculate_core_metrics(start_date, end_date)
            cohort_metrics = await self._calculate_cohort_metrics(start_date, end_date)
            payment_metrics = await self._calculate_payment_metrics(start_date, end_date)
            churn_metrics = await self._calculate_churn_metrics(start_date, end_date)
            ltv_metrics = await self._calculate_ltv_metrics()
            
            # Generate forecasts
            mrr_forecast = await self._forecast_mrr(90)  # 90-day forecast
            churn_prediction = await self._predict_churn_risk()
            
            # Calculate growth rates
            growth_rates = await self._calculate_growth_rates(start_date, end_date)
            
            # Generate insights
            business_insights = await self._generate_business_insights(core_metrics, churn_metrics)
            
            comprehensive_metrics = {
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'days': (end_date - start_date).days
                },
                'core_metrics': core_metrics,
                'cohort_analysis': cohort_metrics,
                'payment_performance': payment_metrics,
                'churn_analysis': churn_metrics,
                'ltv_analysis': ltv_metrics,
                'growth_rates': growth_rates,
                'forecasts': {
                    'mrr_forecast': mrr_forecast,
                    'churn_prediction': churn_prediction
                },
                'business_insights': business_insights,
                'calculated_at': datetime.utcnow().isoformat()
            }
            
            # Cache result for 1 hour
            await self.redis.setex(cache_key, 3600, json.dumps(comprehensive_metrics, default=str))
            
            # Store in database for historical tracking
            await self._store_metrics_snapshot(comprehensive_metrics)
            
            return comprehensive_metrics
            
        except Exception as e:
            logger.error(f"Failed to calculate comprehensive metrics: {str(e)}")
            raise
    
    async def generate_revenue_dashboard(self, period_days: int = 90) -> Dict[str, str]:
        """Generate interactive revenue dashboard with visualizations"""
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=period_days)
            
            # Get metrics data
            metrics = await self.calculate_comprehensive_metrics(start_date, end_date)
            
            # Get historical data for trending
            historical_data = await self._get_historical_metrics(period_days * 2)
            
            # Create visualizations
            charts = await self._create_dashboard_charts(metrics, historical_data)
            
            dashboard = {
                'title': f"Christopher's AI Coaching - Revenue Dashboard ({period_days} days)",
                'generated_at': datetime.utcnow().isoformat(),
                'period': metrics['period'],
                'summary_stats': self._extract_summary_stats(metrics),
                'charts': charts,
                'key_insights': metrics['business_insights']
            }
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Failed to generate dashboard: {str(e)}")
            raise
    
    async def analyze_customer_segments(self) -> Dict[str, Any]:
        """Perform detailed customer segmentation analysis"""
        try:
            async with self.db_pool.acquire() as conn:
                # RFM Analysis (Recency, Frequency, Monetary)
                rfm_data = await conn.fetch("""
                    WITH customer_metrics AS (
                        SELECT 
                            c.id,
                            c.email,
                            c.total_lifetime_value,
                            EXTRACT(DAYS FROM CURRENT_TIMESTAMP - c.last_activity_at) as recency_days,
                            COUNT(DISTINCT pt.id) as payment_frequency,
                            AVG(pt.amount) as avg_payment_amount,
                            SUM(CASE WHEN pt.status = 'succeeded' THEN pt.amount ELSE 0 END) as total_payments,
                            s.unit_amount as current_mrr,
                            c.lifecycle_stage,
                            c.churn_risk_score
                        FROM customers c
                        LEFT JOIN payment_transactions pt ON c.id = pt.customer_id
                        LEFT JOIN subscriptions s ON c.id = s.customer_id AND s.status = 'active'
                        WHERE c.created_at > CURRENT_TIMESTAMP - INTERVAL '2 years'
                        GROUP BY c.id, c.email, c.total_lifetime_value, c.last_activity_at, 
                                 s.unit_amount, c.lifecycle_stage, c.churn_risk_score
                    )
                    SELECT 
                        *,
                        CASE 
                            WHEN total_payments >= 10000 THEN 'VIP'
                            WHEN total_payments >= 5000 THEN 'High Value'
                            WHEN total_payments >= 1000 THEN 'Medium Value'
                            ELSE 'Low Value'
                        END as value_segment,
                        CASE 
                            WHEN recency_days <= 7 THEN 'Active'
                            WHEN recency_days <= 30 THEN 'Recent'
                            WHEN recency_days <= 90 THEN 'At Risk'
                            ELSE 'Inactive'
                        END as recency_segment,
                        CASE 
                            WHEN payment_frequency >= 12 THEN 'High Frequency'
                            WHEN payment_frequency >= 6 THEN 'Medium Frequency'
                            ELSE 'Low Frequency'
                        END as frequency_segment
                    FROM customer_metrics
                """)
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(rfm_data)
            
            # Create customer segments
            segments = self._create_customer_segments(df)
            
            # Calculate segment performance
            segment_performance = self._analyze_segment_performance(df)
            
            # Generate recommendations
            segment_recommendations = self._generate_segment_recommendations(segments, segment_performance)
            
            return {
                'total_customers_analyzed': len(df),
                'segments': segments,
                'segment_performance': segment_performance,
                'recommendations': segment_recommendations,
                'analysis_date': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Customer segmentation analysis failed: {str(e)}")
            raise
    
    async def forecast_revenue(self, forecast_days: int = 365) -> Dict[str, Any]:
        """Generate comprehensive revenue forecasting using machine learning"""
        try:
            # Get historical data for model training
            historical_data = await self._get_revenue_time_series(days=730)  # 2 years
            
            if len(historical_data) < 30:
                raise ValueError("Insufficient historical data for forecasting")
            
            # Prepare data for ML models
            df = pd.DataFrame(historical_data)
            df['date'] = pd.to_datetime(df['metric_date'])
            df = df.sort_values('date')
            
            # Create features
            df = self._create_forecasting_features(df)
            
            # Train models and generate forecasts
            forecasts = {}
            
            # MRR Forecast
            forecasts['mrr'] = await self._forecast_metric(df, 'mrr', forecast_days)
            
            # Customer Count Forecast
            forecasts['customers'] = await self._forecast_metric(df, 'active_customers', forecast_days)
            
            # Churn Rate Forecast
            churn_data = await self._get_churn_time_series(days=365)
            if len(churn_data) >= 12:  # At least 12 data points
                churn_df = pd.DataFrame(churn_data)
                forecasts['churn_rate'] = await self._forecast_metric(churn_df, 'monthly_churn_rate', forecast_days)
            
            # Calculate derived forecasts
            forecasts['arr'] = [mrr * 12 for mrr in forecasts['mrr']['values']]
            forecasts['revenue'] = await self._calculate_revenue_forecast(forecasts, forecast_days)
            
            # Generate scenarios (best case, worst case, most likely)
            scenarios = self._generate_forecast_scenarios(forecasts)
            
            # Calculate forecast confidence
            confidence_metrics = self._calculate_forecast_confidence(df, forecasts)
            
            return {
                'forecast_period': {
                    'start_date': (datetime.utcnow() + timedelta(days=1)).date().isoformat(),
                    'end_date': (datetime.utcnow() + timedelta(days=forecast_days)).date().isoformat(),
                    'days': forecast_days
                },
                'forecasts': forecasts,
                'scenarios': scenarios,
                'confidence_metrics': confidence_metrics,
                'model_performance': {
                    'training_data_points': len(df),
                    'model_accuracy': confidence_metrics.get('overall_accuracy', 0),
                    'last_updated': datetime.utcnow().isoformat()
                },
                'assumptions': [
                    "Current pricing structure remains stable",
                    "No major market disruptions",
                    "Marketing spend remains consistent",
                    "Product quality and customer satisfaction maintained",
                    "Economic conditions remain stable"
                ]
            }
            
        except Exception as e:
            logger.error(f"Revenue forecasting failed: {str(e)}")
            raise
    
    async def analyze_pricing_optimization(self) -> Dict[str, Any]:
        """Analyze pricing optimization opportunities"""
        try:
            # Get pricing and conversion data
            async with self.db_pool.acquire() as conn:
                pricing_data = await conn.fetch("""
                    WITH plan_metrics AS (
                        SELECT 
                            sp.id as plan_id,
                            sp.name,
                            sp.base_price,
                            sp.billing_interval,
                            COUNT(s.id) as active_subscriptions,
                            AVG(c.churn_risk_score) as avg_churn_risk,
                            COUNT(CASE WHEN c.lifecycle_stage = 'churned' 
                                       AND c.updated_at > CURRENT_TIMESTAMP - INTERVAL '90 days' 
                                       THEN 1 END) as recent_churns,
                            AVG(c.total_lifetime_value) as avg_ltv,
                            COUNT(CASE WHEN s.created_at > CURRENT_TIMESTAMP - INTERVAL '30 days' 
                                       THEN 1 END) as new_subscriptions_30d
                        FROM subscription_plans sp
                        LEFT JOIN subscriptions s ON sp.id::text = s.plan_id AND s.status = 'active'
                        LEFT JOIN customers c ON s.customer_id = c.id
                        WHERE sp.is_active = TRUE
                        GROUP BY sp.id, sp.name, sp.base_price, sp.billing_interval
                    )
                    SELECT 
                        *,
                        CASE WHEN active_subscriptions > 0 
                             THEN recent_churns::float / active_subscriptions * 100 
                             ELSE 0 END as churn_rate_percent,
                        base_price * active_subscriptions as monthly_revenue
                    FROM plan_metrics
                    ORDER BY monthly_revenue DESC
                """)
            
            # Analyze price sensitivity
            price_sensitivity = await self._analyze_price_sensitivity(pricing_data)
            
            # Calculate optimal pricing
            pricing_recommendations = self._calculate_optimal_pricing(pricing_data, price_sensitivity)
            
            # Revenue impact projections
            revenue_projections = self._project_pricing_impact(pricing_recommendations)
            
            return {
                'current_pricing_analysis': [
                    {
                        'plan': row['name'],
                        'current_price': float(row['base_price']),
                        'active_subscriptions': row['active_subscriptions'],
                        'monthly_revenue': float(row['monthly_revenue'] or 0),
                        'churn_rate': round(float(row['churn_rate_percent'] or 0), 2),
                        'avg_ltv': float(row['avg_ltv'] or 0),
                        'avg_churn_risk': float(row['avg_churn_risk'] or 0)
                    }
                    for row in pricing_data
                ],
                'price_sensitivity_analysis': price_sensitivity,
                'optimization_recommendations': pricing_recommendations,
                'revenue_impact_projections': revenue_projections,
                'analysis_date': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Pricing optimization analysis failed: {str(e)}")
            raise
    
    async def generate_executive_report(self, period_days: int = 30) -> Dict[str, Any]:
        """Generate comprehensive executive revenue report"""
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=period_days)
            
            # Get comprehensive metrics
            metrics = await self.calculate_comprehensive_metrics(start_date, end_date)
            
            # Get previous period for comparison
            prev_start = start_date - timedelta(days=period_days)
            prev_metrics = await self.calculate_comprehensive_metrics(prev_start, start_date)
            
            # Calculate period-over-period changes
            comparisons = self._calculate_period_comparisons(metrics, prev_metrics)
            
            # Get key performance indicators
            kpis = self._extract_executive_kpis(metrics, comparisons)
            
            # Generate strategic insights
            strategic_insights = await self._generate_strategic_insights(metrics, comparisons)
            
            # Risk analysis
            risk_analysis = await self._analyze_business_risks(metrics)
            
            # Opportunity analysis
            opportunities = await self._identify_growth_opportunities(metrics)
            
            # Create executive summary
            executive_summary = self._create_executive_summary(kpis, strategic_insights, risk_analysis)
            
            return {
                'report_title': f"Executive Revenue Report - {period_days} Day Period",
                'report_period': {
                    'current': {'start': start_date.date(), 'end': end_date.date()},
                    'previous': {'start': prev_start.date(), 'end': start_date.date()}
                },
                'executive_summary': executive_summary,
                'key_performance_indicators': kpis,
                'period_comparisons': comparisons,
                'strategic_insights': strategic_insights,
                'risk_analysis': risk_analysis,
                'growth_opportunities': opportunities,
                'detailed_metrics': {
                    'current_period': metrics,
                    'previous_period': prev_metrics
                },
                'generated_at': datetime.utcnow().isoformat(),
                'generated_by': "Christopher's AI Revenue Analytics Engine"
            }
            
        except Exception as e:
            logger.error(f"Executive report generation failed: {str(e)}")
            raise
    
    # Private helper methods
    
    async def _calculate_core_metrics(self, start_date: datetime, end_date: datetime) -> Dict:
        """Calculate core MRR, ARR, and customer metrics"""
        async with self.db_pool.acquire() as conn:
            # Current MRR calculation
            mrr_data = await conn.fetchrow("""
                SELECT 
                    SUM(
                        CASE 
                            WHEN sp.billing_interval = 'monthly' THEN s.unit_amount
                            WHEN sp.billing_interval = 'quarterly' THEN s.unit_amount / 3
                            WHEN sp.billing_interval = 'annually' THEN s.unit_amount / 12
                            ELSE 0
                        END
                    ) as current_mrr,
                    COUNT(DISTINCT s.customer_id) as active_customers,
                    AVG(s.unit_amount) as avg_subscription_value
                FROM subscriptions s
                JOIN subscription_plans sp ON s.plan_id = sp.id::text
                WHERE s.status = 'active'
            """)
            
            # New MRR (from new customers in period)
            new_mrr_data = await conn.fetchrow("""
                SELECT 
                    SUM(
                        CASE 
                            WHEN sp.billing_interval = 'monthly' THEN s.unit_amount
                            WHEN sp.billing_interval = 'quarterly' THEN s.unit_amount / 3
                            WHEN sp.billing_interval = 'annually' THEN s.unit_amount / 12
                            ELSE 0
                        END
                    ) as new_mrr,
                    COUNT(DISTINCT s.customer_id) as new_customers
                FROM subscriptions s
                JOIN subscription_plans sp ON s.plan_id = sp.id::text
                JOIN customers c ON s.customer_id = c.id
                WHERE s.status = 'active'
                AND c.created_at BETWEEN $1 AND $2
            """, start_date, end_date)
            
            # Churned MRR
            churn_mrr_data = await conn.fetchrow("""
                SELECT 
                    SUM(
                        CASE 
                            WHEN sp.billing_interval = 'monthly' THEN s.unit_amount
                            WHEN sp.billing_interval = 'quarterly' THEN s.unit_amount / 3
                            WHEN sp.billing_interval = 'annually' THEN s.unit_amount / 12
                            ELSE 0
                        END
                    ) as churn_mrr,
                    COUNT(DISTINCT s.customer_id) as churned_customers
                FROM subscriptions s
                JOIN subscription_plans sp ON s.plan_id = sp.id::text
                WHERE s.status IN ('canceled', 'unpaid')
                AND s.canceled_at BETWEEN $1 AND $2
            """, start_date, end_date)
            
            # Total revenue in period
            revenue_data = await conn.fetchrow("""
                SELECT 
                    SUM(CASE WHEN pt.status = 'succeeded' THEN pt.amount ELSE 0 END) as total_revenue,
                    COUNT(CASE WHEN pt.status = 'succeeded' THEN 1 END) as successful_payments,
                    COUNT(CASE WHEN pt.status = 'failed' THEN 1 END) as failed_payments
                FROM payment_transactions pt
                WHERE pt.created_at BETWEEN $1 AND $2
            """, start_date, end_date)
        
        # Calculate derived metrics
        current_mrr = float(mrr_data['current_mrr'] or 0)
        new_mrr = float(new_mrr_data['new_mrr'] or 0)
        churn_mrr = float(churn_mrr_data['churn_mrr'] or 0)
        
        total_payments = (revenue_data['successful_payments'] or 0) + (revenue_data['failed_payments'] or 0)
        payment_success_rate = (
            (revenue_data['successful_payments'] or 0) / total_payments * 100
            if total_payments > 0 else 0
        )
        
        return {
            'mrr': current_mrr,
            'arr': current_mrr * 12,
            'new_mrr': new_mrr,
            'churn_mrr': churn_mrr,
            'net_new_mrr': new_mrr - churn_mrr,
            'active_customers': mrr_data['active_customers'] or 0,
            'new_customers': new_mrr_data['new_customers'] or 0,
            'churned_customers': churn_mrr_data['churned_customers'] or 0,
            'total_revenue': float(revenue_data['total_revenue'] or 0),
            'payment_success_rate': round(payment_success_rate, 2),
            'avg_subscription_value': float(mrr_data['avg_subscription_value'] or 0),
            'avg_revenue_per_customer': (
                current_mrr / mrr_data['active_customers']
                if mrr_data['active_customers'] > 0 else 0
            )
        }
    
    async def _calculate_cohort_metrics(self, start_date: datetime, end_date: datetime) -> Dict:
        """Calculate customer cohort analysis"""
        async with self.db_pool.acquire() as conn:
            # Monthly cohorts
            cohort_data = await conn.fetch("""
                WITH cohorts AS (
                    SELECT 
                        DATE_TRUNC('month', c.created_at) as cohort_month,
                        c.id as customer_id,
                        c.created_at,
                        c.total_lifetime_value,
                        CASE WHEN c.lifecycle_stage = 'churned' THEN c.updated_at ELSE NULL END as churn_date
                    FROM customers c
                    WHERE c.created_at >= $1 - INTERVAL '12 months'
                ),
                cohort_metrics AS (
                    SELECT 
                        cohort_month,
                        COUNT(customer_id) as cohort_size,
                        AVG(total_lifetime_value) as avg_ltv,
                        COUNT(CASE WHEN churn_date IS NULL THEN 1 END) as retained_customers,
                        COUNT(CASE WHEN churn_date IS NOT NULL THEN 1 END) as churned_customers
                    FROM cohorts
                    GROUP BY cohort_month
                )
                SELECT 
                    cohort_month,
                    cohort_size,
                    avg_ltv,
                    retained_customers,
                    churned_customers,
                    CASE WHEN cohort_size > 0 
                         THEN retained_customers::float / cohort_size * 100 
                         ELSE 0 END as retention_rate
                FROM cohort_metrics
                ORDER BY cohort_month DESC
            """, start_date)
        
        cohorts = [
            {
                'month': row['cohort_month'].strftime('%Y-%m'),
                'size': row['cohort_size'],
                'avg_ltv': float(row['avg_ltv'] or 0),
                'retained': row['retained_customers'],
                'churned': row['churned_customers'],
                'retention_rate': round(float(row['retention_rate'] or 0), 2)
            }
            for row in cohort_data
        ]
        
        return {'monthly_cohorts': cohorts}
    
    async def _initialize_ml_models(self):
        """Initialize machine learning models for forecasting"""
        self.models = {
            'mrr_forecast': RandomForestRegressor(n_estimators=100, random_state=42),
            'customer_forecast': LinearRegression(),
            'churn_prediction': RandomForestRegressor(n_estimators=50, random_state=42)
        }
        logger.info("ML models initialized")
    
    def _create_forecasting_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create features for ML forecasting models"""
        df = df.copy()
        
        # Time-based features
        df['day_of_week'] = df['date'].dt.dayofweek
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['days_since_start'] = (df['date'] - df['date'].min()).dt.days
        
        # Lag features
        for col in ['mrr', 'active_customers']:
            if col in df.columns:
                df[f'{col}_lag_1'] = df[col].shift(1)
                df[f'{col}_lag_7'] = df[col].shift(7)
                df[f'{col}_lag_30'] = df[col].shift(30)
        
        # Rolling averages
        for col in ['mrr', 'active_customers']:
            if col in df.columns:
                df[f'{col}_ma_7'] = df[col].rolling(window=7).mean()
                df[f'{col}_ma_30'] = df[col].rolling(window=30).mean()
        
        # Growth rates
        for col in ['mrr', 'active_customers']:
            if col in df.columns:
                df[f'{col}_growth'] = df[col].pct_change()
        
        return df.fillna(method='bfill').fillna(0)
    
    async def _store_metrics_snapshot(self, metrics: Dict):
        """Store metrics snapshot in database for historical tracking"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO revenue_metrics_snapshots (
                    snapshot_date, period_start, period_end, metrics_data
                ) VALUES ($1, $2, $3, $4)
                ON CONFLICT (snapshot_date, period_start, period_end)
                DO UPDATE SET metrics_data = EXCLUDED.metrics_data
            """, 
                datetime.utcnow().date(),
                datetime.fromisoformat(metrics['period']['start_date'].replace('Z', '+00:00')),
                datetime.fromisoformat(metrics['period']['end_date'].replace('Z', '+00:00')),
                json.dumps(metrics)
            )

# Initialize analytics engine
analytics_engine = RevenueAnalyticsEngine(
    db_url="postgresql://user:pass@localhost/billing_db",
    redis_url="redis://localhost:6379"
)

if __name__ == "__main__":
    # Example usage
    async def main():
        await analytics_engine.initialize()
        
        # Generate comprehensive metrics
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        metrics = await analytics_engine.calculate_comprehensive_metrics(start_date, end_date)
        print(json.dumps(metrics, indent=2, default=str))
        
        # Generate executive report
        exec_report = await analytics_engine.generate_executive_report(30)
        print("\nExecutive Report Generated")
        
        # Customer segmentation
        segments = await analytics_engine.analyze_customer_segments()
        print(f"\nCustomer Segments: {len(segments['segments'])} segments identified")
    
    asyncio.run(main())