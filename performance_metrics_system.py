"""
Performance Metrics and Analytics System for Christopher's Coaching Business
Focus: Comprehensive tracking, analysis, and optimization of customer experience metrics
"""

import asyncio
import json
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, asdict
from enum import Enum
import math
from collections import defaultdict, Counter

class MetricCategory(Enum):
    CUSTOMER_SATISFACTION = "customer_satisfaction"
    RESPONSE_TIMES = "response_times"
    RESOLUTION_RATES = "resolution_rates"
    ENGAGEMENT_METRICS = "engagement_metrics"
    RETENTION_METRICS = "retention_metrics"
    FINANCIAL_IMPACT = "financial_impact"
    AGENT_PERFORMANCE = "agent_performance"
    AUTOMATION_EFFECTIVENESS = "automation_effectiveness"
    EMOTIONAL_INTELLIGENCE = "emotional_intelligence"
    PREDICTIVE_ACCURACY = "predictive_accuracy"

class MetricFrequency(Enum):
    REAL_TIME = "real_time"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    URGENT = "urgent"

class TrendDirection(Enum):
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"
    VOLATILE = "volatile"

@dataclass
class MetricDefinition:
    metric_id: str
    name: str
    description: str
    category: MetricCategory
    calculation_method: str
    target_value: float
    threshold_warning: float
    threshold_critical: float
    frequency: MetricFrequency
    is_higher_better: bool
    unit: str
    dependencies: List[str]

@dataclass
class MetricValue:
    metric_id: str
    timestamp: datetime
    value: float
    metadata: Dict[str, Any]
    data_quality_score: float
    confidence_interval: Tuple[float, float]
    sample_size: int
    calculation_context: Dict[str, Any]

@dataclass
class PerformanceDashboard:
    dashboard_id: str
    name: str
    description: str
    metrics: List[str]  # metric_ids
    refresh_frequency: MetricFrequency
    target_audience: List[str]
    layout_config: Dict[str, Any]
    last_updated: datetime
    is_active: bool

@dataclass
class Alert:
    alert_id: str
    metric_id: str
    severity: AlertSeverity
    message: str
    triggered_at: datetime
    current_value: float
    threshold_breached: float
    recommended_actions: List[str]
    acknowledged: bool
    resolved: bool
    resolution_actions: List[str]

@dataclass
class TrendAnalysis:
    metric_id: str
    analysis_period: int  # days
    trend_direction: TrendDirection
    trend_strength: float  # 0-1
    rate_of_change: float
    seasonal_patterns: Dict[str, float]
    anomalies: List[Dict[str, Any]]
    forecast_values: List[Tuple[datetime, float]]
    confidence_level: float

class PerformanceMetricsSystem:
    """
    Comprehensive performance metrics system featuring:
    - Multi-dimensional metric tracking and analysis
    - Real-time dashboard and alerting
    - Predictive trend analysis
    - ROI and business impact measurement
    - Automated reporting and insights
    """
    
    def __init__(self):
        self.metric_definitions: Dict[str, MetricDefinition] = {}
        self.metric_values: Dict[str, List[MetricValue]] = {}
        self.dashboards: Dict[str, PerformanceDashboard] = {}
        self.alerts: Dict[str, Alert] = {}
        self.trend_analyses: Dict[str, TrendAnalysis] = {}
        
        self.setup_metric_definitions()
        self.setup_dashboards()
        self.setup_alerting_rules()
        self.setup_benchmarks()
    
    def setup_metric_definitions(self):
        """Define all performance metrics to track"""
        
        metrics_config = [
            # Customer Satisfaction Metrics
            {
                "metric_id": "csat_score",
                "name": "Customer Satisfaction Score",
                "description": "Average customer satisfaction rating (1-5 scale)",
                "category": MetricCategory.CUSTOMER_SATISFACTION,
                "calculation_method": "average",
                "target_value": 4.5,
                "threshold_warning": 4.0,
                "threshold_critical": 3.5,
                "frequency": MetricFrequency.DAILY,
                "is_higher_better": True,
                "unit": "rating",
                "dependencies": []
            },
            {
                "metric_id": "nps_score",
                "name": "Net Promoter Score",
                "description": "Net Promoter Score based on customer loyalty survey",
                "category": MetricCategory.CUSTOMER_SATISFACTION,
                "calculation_method": "nps_formula",
                "target_value": 50.0,
                "threshold_warning": 30.0,
                "threshold_critical": 10.0,
                "frequency": MetricFrequency.WEEKLY,
                "is_higher_better": True,
                "unit": "score",
                "dependencies": []
            },
            {
                "metric_id": "ces_score",
                "name": "Customer Effort Score",
                "description": "Average customer effort score (1-5 scale, lower is better)",
                "category": MetricCategory.CUSTOMER_SATISFACTION,
                "calculation_method": "average",
                "target_value": 2.0,
                "threshold_warning": 3.0,
                "threshold_critical": 3.5,
                "frequency": MetricFrequency.DAILY,
                "is_higher_better": False,
                "unit": "rating",
                "dependencies": []
            },
            
            # Response Time Metrics
            {
                "metric_id": "first_response_time",
                "name": "First Response Time",
                "description": "Average time to first response in hours",
                "category": MetricCategory.RESPONSE_TIMES,
                "calculation_method": "average",
                "target_value": 2.0,
                "threshold_warning": 4.0,
                "threshold_critical": 8.0,
                "frequency": MetricFrequency.HOURLY,
                "is_higher_better": False,
                "unit": "hours",
                "dependencies": []
            },
            {
                "metric_id": "resolution_time",
                "name": "Average Resolution Time",
                "description": "Average time to resolve customer issues in hours",
                "category": MetricCategory.RESPONSE_TIMES,
                "calculation_method": "average",
                "target_value": 24.0,
                "threshold_warning": 48.0,
                "threshold_critical": 72.0,
                "frequency": MetricFrequency.DAILY,
                "is_higher_better": False,
                "unit": "hours",
                "dependencies": []
            },
            
            # Resolution Rate Metrics
            {
                "metric_id": "first_contact_resolution",
                "name": "First Contact Resolution Rate",
                "description": "Percentage of issues resolved in first contact",
                "category": MetricCategory.RESOLUTION_RATES,
                "calculation_method": "percentage",
                "target_value": 80.0,
                "threshold_warning": 70.0,
                "threshold_critical": 60.0,
                "frequency": MetricFrequency.DAILY,
                "is_higher_better": True,
                "unit": "percentage",
                "dependencies": []
            },
            {
                "metric_id": "sla_compliance",
                "name": "SLA Compliance Rate",
                "description": "Percentage of tickets meeting SLA requirements",
                "category": MetricCategory.RESOLUTION_RATES,
                "calculation_method": "percentage",
                "target_value": 95.0,
                "threshold_warning": 90.0,
                "threshold_critical": 85.0,
                "frequency": MetricFrequency.DAILY,
                "is_higher_better": True,
                "unit": "percentage",
                "dependencies": []
            },
            
            # Engagement Metrics
            {
                "metric_id": "customer_health_score",
                "name": "Average Customer Health Score",
                "description": "Average customer relationship health score (0-1)",
                "category": MetricCategory.ENGAGEMENT_METRICS,
                "calculation_method": "average",
                "target_value": 0.8,
                "threshold_warning": 0.6,
                "threshold_critical": 0.4,
                "frequency": MetricFrequency.DAILY,
                "is_higher_better": True,
                "unit": "score",
                "dependencies": []
            },
            {
                "metric_id": "engagement_rate",
                "name": "Customer Engagement Rate",
                "description": "Percentage of customers actively engaged",
                "category": MetricCategory.ENGAGEMENT_METRICS,
                "calculation_method": "percentage",
                "target_value": 85.0,
                "threshold_warning": 75.0,
                "threshold_critical": 65.0,
                "frequency": MetricFrequency.WEEKLY,
                "is_higher_better": True,
                "unit": "percentage",
                "dependencies": []
            },
            
            # Retention Metrics
            {
                "metric_id": "churn_rate",
                "name": "Customer Churn Rate",
                "description": "Monthly customer churn rate percentage",
                "category": MetricCategory.RETENTION_METRICS,
                "calculation_method": "percentage",
                "target_value": 5.0,
                "threshold_warning": 8.0,
                "threshold_critical": 12.0,
                "frequency": MetricFrequency.MONTHLY,
                "is_higher_better": False,
                "unit": "percentage",
                "dependencies": []
            },
            {
                "metric_id": "retention_rate",
                "name": "Customer Retention Rate",
                "description": "Monthly customer retention rate percentage",
                "category": MetricCategory.RETENTION_METRICS,
                "calculation_method": "percentage",
                "target_value": 95.0,
                "threshold_warning": 92.0,
                "threshold_critical": 88.0,
                "frequency": MetricFrequency.MONTHLY,
                "is_higher_better": True,
                "unit": "percentage",
                "dependencies": []
            },
            
            # Financial Impact Metrics
            {
                "metric_id": "customer_lifetime_value",
                "name": "Customer Lifetime Value",
                "description": "Average customer lifetime value in dollars",
                "category": MetricCategory.FINANCIAL_IMPACT,
                "calculation_method": "average",
                "target_value": 5000.0,
                "threshold_warning": 4000.0,
                "threshold_critical": 3000.0,
                "frequency": MetricFrequency.MONTHLY,
                "is_higher_better": True,
                "unit": "dollars",
                "dependencies": []
            },
            {
                "metric_id": "support_cost_per_ticket",
                "name": "Support Cost per Ticket",
                "description": "Average cost to resolve each support ticket",
                "category": MetricCategory.FINANCIAL_IMPACT,
                "calculation_method": "average",
                "target_value": 25.0,
                "threshold_warning": 35.0,
                "threshold_critical": 50.0,
                "frequency": MetricFrequency.WEEKLY,
                "is_higher_better": False,
                "unit": "dollars",
                "dependencies": []
            },
            
            # Automation Effectiveness
            {
                "metric_id": "automation_success_rate",
                "name": "Automation Success Rate",
                "description": "Percentage of automated interactions that succeed",
                "category": MetricCategory.AUTOMATION_EFFECTIVENESS,
                "calculation_method": "percentage",
                "target_value": 85.0,
                "threshold_warning": 75.0,
                "threshold_critical": 65.0,
                "frequency": MetricFrequency.DAILY,
                "is_higher_better": True,
                "unit": "percentage",
                "dependencies": []
            },
            
            # Emotional Intelligence Metrics
            {
                "metric_id": "sentiment_accuracy",
                "name": "Sentiment Analysis Accuracy",
                "description": "Accuracy of automated sentiment analysis",
                "category": MetricCategory.EMOTIONAL_INTELLIGENCE,
                "calculation_method": "percentage",
                "target_value": 85.0,
                "threshold_warning": 80.0,
                "threshold_critical": 75.0,
                "frequency": MetricFrequency.WEEKLY,
                "is_higher_better": True,
                "unit": "percentage",
                "dependencies": []
            },
            {
                "metric_id": "empathy_score",
                "name": "Average Empathy Score",
                "description": "Customer-rated empathy in interactions (1-5)",
                "category": MetricCategory.EMOTIONAL_INTELLIGENCE,
                "calculation_method": "average",
                "target_value": 4.5,
                "threshold_warning": 4.0,
                "threshold_critical": 3.5,
                "frequency": MetricFrequency.WEEKLY,
                "is_higher_better": True,
                "unit": "rating",
                "dependencies": []
            }
        ]
        
        for config in metrics_config:
            metric = MetricDefinition(
                metric_id=config["metric_id"],
                name=config["name"],
                description=config["description"],
                category=MetricCategory(config["category"]),
                calculation_method=config["calculation_method"],
                target_value=config["target_value"],
                threshold_warning=config["threshold_warning"],
                threshold_critical=config["threshold_critical"],
                frequency=MetricFrequency(config["frequency"]),
                is_higher_better=config["is_higher_better"],
                unit=config["unit"],
                dependencies=config["dependencies"]
            )
            self.metric_definitions[metric.metric_id] = metric
            self.metric_values[metric.metric_id] = []
    
    def setup_dashboards(self):
        """Setup performance dashboards for different stakeholders"""
        
        dashboards_config = [
            {
                "dashboard_id": "executive_dashboard",
                "name": "Executive Performance Dashboard",
                "description": "High-level KPIs for executive team",
                "metrics": [
                    "csat_score", "nps_score", "churn_rate", "customer_lifetime_value",
                    "first_contact_resolution", "sla_compliance"
                ],
                "target_audience": ["executives", "leadership"],
                "refresh_frequency": MetricFrequency.HOURLY
            },
            {
                "dashboard_id": "operations_dashboard",
                "name": "Operations Dashboard",
                "description": "Operational metrics for day-to-day management",
                "metrics": [
                    "first_response_time", "resolution_time", "automation_success_rate",
                    "customer_health_score", "engagement_rate", "support_cost_per_ticket"
                ],
                "target_audience": ["operations", "managers"],
                "refresh_frequency": MetricFrequency.REAL_TIME
            },
            {
                "dashboard_id": "customer_success_dashboard",
                "name": "Customer Success Dashboard",
                "description": "Customer-focused metrics for success team",
                "metrics": [
                    "customer_health_score", "engagement_rate", "retention_rate",
                    "empathy_score", "ces_score", "sentiment_accuracy"
                ],
                "target_audience": ["customer_success", "coaches"],
                "refresh_frequency": MetricFrequency.DAILY
            },
            {
                "dashboard_id": "support_team_dashboard",
                "name": "Support Team Dashboard",
                "description": "Support team performance metrics",
                "metrics": [
                    "first_response_time", "resolution_time", "first_contact_resolution",
                    "sla_compliance", "csat_score", "automation_success_rate"
                ],
                "target_audience": ["support_agents", "support_managers"],
                "refresh_frequency": MetricFrequency.REAL_TIME
            }
        ]
        
        for config in dashboards_config:
            dashboard = PerformanceDashboard(
                dashboard_id=config["dashboard_id"],
                name=config["name"],
                description=config["description"],
                metrics=config["metrics"],
                refresh_frequency=config["refresh_frequency"],
                target_audience=config["target_audience"],
                layout_config={"layout": "grid", "columns": 3},
                last_updated=datetime.now(),
                is_active=True
            )
            self.dashboards[dashboard.dashboard_id] = dashboard
    
    def setup_alerting_rules(self):
        """Setup alerting rules for metric thresholds"""
        
        self.alerting_rules = {}
        for metric_id, metric_def in self.metric_definitions.items():
            self.alerting_rules[metric_id] = {
                "warning_enabled": True,
                "critical_enabled": True,
                "escalation_delay_minutes": 30,
                "notification_channels": ["email", "slack"],
                "auto_acknowledge": False
            }
    
    def setup_benchmarks(self):
        """Setup industry benchmarks for comparison"""
        
        self.industry_benchmarks = {
            "csat_score": {"excellent": 4.5, "good": 4.0, "average": 3.5, "poor": 3.0},
            "nps_score": {"excellent": 70, "good": 50, "average": 30, "poor": 10},
            "first_response_time": {"excellent": 1.0, "good": 2.0, "average": 4.0, "poor": 8.0},
            "first_contact_resolution": {"excellent": 90, "good": 80, "average": 70, "poor": 60},
            "churn_rate": {"excellent": 3.0, "good": 5.0, "average": 8.0, "poor": 12.0},
            "automation_success_rate": {"excellent": 90, "good": 85, "average": 75, "poor": 65}
        }
    
    async def record_metric_value(self, metric_id: str, value: float, 
                                timestamp: Optional[datetime] = None,
                                metadata: Dict[str, Any] = None,
                                sample_size: int = 1) -> MetricValue:
        """Record a new metric value"""
        
        if metric_id not in self.metric_definitions:
            raise ValueError(f"Unknown metric ID: {metric_id}")
        
        timestamp = timestamp or datetime.now()
        metadata = metadata or {}
        
        # Calculate confidence interval (simplified)
        confidence_interval = (value * 0.95, value * 1.05)
        
        # Calculate data quality score
        data_quality_score = await self.calculate_data_quality(metric_id, value, metadata)
        
        metric_value = MetricValue(
            metric_id=metric_id,
            timestamp=timestamp,
            value=value,
            metadata=metadata,
            data_quality_score=data_quality_score,
            confidence_interval=confidence_interval,
            sample_size=sample_size,
            calculation_context={"source": "manual_input", "version": "1.0"}
        )
        
        self.metric_values[metric_id].append(metric_value)
        
        # Check for alerts
        await self.check_metric_alerts(metric_id, value)
        
        # Update trend analysis if enough data points
        if len(self.metric_values[metric_id]) >= 5:
            await self.update_trend_analysis(metric_id)
        
        return metric_value
    
    async def calculate_data_quality(self, metric_id: str, value: float, 
                                   metadata: Dict[str, Any]) -> float:
        """Calculate data quality score for metric value"""
        
        quality_score = 1.0
        
        # Check for reasonable value ranges
        metric_def = self.metric_definitions[metric_id]
        
        # Penalize extreme outliers
        if len(self.metric_values[metric_id]) > 0:
            recent_values = [mv.value for mv in self.metric_values[metric_id][-10:]]
            avg_value = statistics.mean(recent_values)
            std_dev = statistics.stdev(recent_values) if len(recent_values) > 1 else 0
            
            if std_dev > 0:
                z_score = abs((value - avg_value) / std_dev)
                if z_score > 3.0:  # More than 3 standard deviations
                    quality_score *= 0.7
        
        # Check metadata completeness
        required_metadata = ["source", "collection_method"]
        metadata_completeness = sum(1 for key in required_metadata if key in metadata) / len(required_metadata)
        quality_score *= (0.8 + 0.2 * metadata_completeness)
        
        return round(quality_score, 3)
    
    async def check_metric_alerts(self, metric_id: str, value: float):
        """Check if metric value triggers any alerts"""
        
        metric_def = self.metric_definitions[metric_id]
        alerts_triggered = []
        
        # Check critical threshold
        is_critical_breach = (
            (metric_def.is_higher_better and value < metric_def.threshold_critical) or
            (not metric_def.is_higher_better and value > metric_def.threshold_critical)
        )
        
        if is_critical_breach:
            alert = await self.create_alert(
                metric_id=metric_id,
                severity=AlertSeverity.CRITICAL,
                current_value=value,
                threshold_breached=metric_def.threshold_critical
            )
            alerts_triggered.append(alert)
        
        # Check warning threshold
        elif (
            (metric_def.is_higher_better and value < metric_def.threshold_warning) or
            (not metric_def.is_higher_better and value > metric_def.threshold_warning)
        ):
            alert = await self.create_alert(
                metric_id=metric_id,
                severity=AlertSeverity.WARNING,
                current_value=value,
                threshold_breached=metric_def.threshold_warning
            )
            alerts_triggered.append(alert)
        
        return alerts_triggered
    
    async def create_alert(self, metric_id: str, severity: AlertSeverity, 
                         current_value: float, threshold_breached: float) -> Alert:
        """Create a new alert for metric threshold breach"""
        
        metric_def = self.metric_definitions[metric_id]
        alert_id = f"ALT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{metric_id}"
        
        # Generate alert message
        direction = "below" if metric_def.is_higher_better else "above"
        message = f"{metric_def.name} is {direction} {severity.value} threshold: {current_value:.2f} {metric_def.unit} (threshold: {threshold_breached:.2f})"
        
        # Generate recommended actions
        recommended_actions = await self.generate_alert_actions(metric_id, severity, current_value)
        
        alert = Alert(
            alert_id=alert_id,
            metric_id=metric_id,
            severity=severity,
            message=message,
            triggered_at=datetime.now(),
            current_value=current_value,
            threshold_breached=threshold_breached,
            recommended_actions=recommended_actions,
            acknowledged=False,
            resolved=False,
            resolution_actions=[]
        )
        
        self.alerts[alert_id] = alert
        return alert
    
    async def generate_alert_actions(self, metric_id: str, severity: AlertSeverity, 
                                   current_value: float) -> List[str]:
        """Generate recommended actions for alert"""
        
        actions = []
        
        metric_specific_actions = {
            "csat_score": [
                "Review recent customer feedback",
                "Analyze support interaction quality",
                "Implement customer satisfaction recovery program",
                "Schedule team training on customer service excellence"
            ],
            "first_response_time": [
                "Check agent availability and workload",
                "Implement priority routing for urgent tickets",
                "Consider adding temporary support staff",
                "Review automation rules for faster initial responses"
            ],
            "churn_rate": [
                "Activate customer retention campaign",
                "Analyze churn reasons from exit interviews",
                "Implement proactive customer success outreach",
                "Review and improve onboarding process"
            ],
            "automation_success_rate": [
                "Review failed automation cases",
                "Update chatbot training data",
                "Improve automation routing rules",
                "Fallback to human agents more quickly"
            ]
        }
        
        actions = metric_specific_actions.get(metric_id, [
            "Investigate root cause of metric decline",
            "Implement corrective action plan",
            "Monitor metric closely for improvement"
        ])
        
        if severity == AlertSeverity.CRITICAL:
            actions.insert(0, "Immediate escalation to management required")
        
        return actions[:5]  # Return top 5 actions
    
    async def calculate_metric(self, metric_id: str, data_source: Dict[str, Any], 
                             calculation_period: Optional[timedelta] = None) -> float:
        """Calculate metric value from data source"""
        
        metric_def = self.metric_definitions[metric_id]
        calculation_method = metric_def.calculation_method
        
        if calculation_method == "average":
            return await self.calculate_average_metric(metric_id, data_source, calculation_period)
        elif calculation_method == "percentage":
            return await self.calculate_percentage_metric(metric_id, data_source, calculation_period)
        elif calculation_method == "nps_formula":
            return await self.calculate_nps_metric(data_source, calculation_period)
        else:
            raise ValueError(f"Unknown calculation method: {calculation_method}")
    
    async def calculate_average_metric(self, metric_id: str, data_source: Dict[str, Any], 
                                     calculation_period: Optional[timedelta]) -> float:
        """Calculate average-based metric"""
        
        # In production, this would integrate with actual data sources
        # Simulating data retrieval and calculation
        
        if metric_id == "csat_score":
            satisfaction_scores = data_source.get("satisfaction_scores", [4.0, 4.2, 4.1, 4.3, 4.0])
            return statistics.mean(satisfaction_scores) if satisfaction_scores else 0.0
        
        elif metric_id == "first_response_time":
            response_times = data_source.get("response_times_hours", [1.5, 2.0, 1.8, 2.2, 1.9])
            return statistics.mean(response_times) if response_times else 0.0
        
        elif metric_id == "resolution_time":
            resolution_times = data_source.get("resolution_times_hours", [18, 22, 16, 25, 20])
            return statistics.mean(resolution_times) if resolution_times else 0.0
        
        elif metric_id == "customer_health_score":
            health_scores = data_source.get("health_scores", [0.8, 0.75, 0.82, 0.78, 0.85])
            return statistics.mean(health_scores) if health_scores else 0.0
        
        # Default calculation
        values = data_source.get("values", [])
        return statistics.mean(values) if values else 0.0
    
    async def calculate_percentage_metric(self, metric_id: str, data_source: Dict[str, Any], 
                                        calculation_period: Optional[timedelta]) -> float:
        """Calculate percentage-based metric"""
        
        if metric_id == "first_contact_resolution":
            resolved_first_contact = data_source.get("resolved_first_contact", 85)
            total_tickets = data_source.get("total_tickets", 100)
            return (resolved_first_contact / total_tickets * 100) if total_tickets > 0 else 0.0
        
        elif metric_id == "sla_compliance":
            sla_met = data_source.get("sla_met", 92)
            total_tickets = data_source.get("total_tickets", 100)
            return (sla_met / total_tickets * 100) if total_tickets > 0 else 0.0
        
        elif metric_id == "churn_rate":
            churned_customers = data_source.get("churned_customers", 5)
            total_customers = data_source.get("total_customers", 100)
            return (churned_customers / total_customers * 100) if total_customers > 0 else 0.0
        
        elif metric_id == "automation_success_rate":
            successful_automations = data_source.get("successful_automations", 85)
            total_automations = data_source.get("total_automations", 100)
            return (successful_automations / total_automations * 100) if total_automations > 0 else 0.0
        
        # Default percentage calculation
        numerator = data_source.get("numerator", 0)
        denominator = data_source.get("denominator", 1)
        return (numerator / denominator * 100) if denominator > 0 else 0.0
    
    async def calculate_nps_metric(self, data_source: Dict[str, Any], 
                                 calculation_period: Optional[timedelta]) -> float:
        """Calculate Net Promoter Score"""
        
        scores = data_source.get("nps_scores", [9, 8, 7, 10, 9, 6, 8, 9, 10, 7])
        
        if not scores:
            return 0.0
        
        promoters = len([s for s in scores if s >= 9])
        detractors = len([s for s in scores if s <= 6])
        total = len(scores)
        
        nps = ((promoters - detractors) / total * 100) if total > 0 else 0.0
        return round(nps, 1)
    
    async def update_trend_analysis(self, metric_id: str):
        """Update trend analysis for metric"""
        
        if metric_id not in self.metric_values or len(self.metric_values[metric_id]) < 5:
            return
        
        values = self.metric_values[metric_id]
        analysis_period = 30  # days
        
        # Get recent values within analysis period
        cutoff_date = datetime.now() - timedelta(days=analysis_period)
        recent_values = [v for v in values if v.timestamp >= cutoff_date]
        
        if len(recent_values) < 3:
            return
        
        # Calculate trend direction and strength
        value_list = [v.value for v in recent_values]
        timestamps = [(v.timestamp - recent_values[0].timestamp).total_seconds() / 3600 for v in recent_values]
        
        # Simple linear regression for trend
        trend_slope = await self.calculate_linear_regression_slope(timestamps, value_list)
        
        # Determine trend direction
        if abs(trend_slope) < 0.01:
            trend_direction = TrendDirection.STABLE
        elif trend_slope > 0:
            trend_direction = TrendDirection.IMPROVING if self.metric_definitions[metric_id].is_higher_better else TrendDirection.DECLINING
        else:
            trend_direction = TrendDirection.DECLINING if self.metric_definitions[metric_id].is_higher_better else TrendDirection.IMPROVING
        
        # Calculate trend strength
        trend_strength = min(1.0, abs(trend_slope) * 10)
        
        # Calculate rate of change
        if len(value_list) >= 2:
            rate_of_change = (value_list[-1] - value_list[0]) / value_list[0] * 100 if value_list[0] != 0 else 0
        else:
            rate_of_change = 0.0
        
        # Detect anomalies
        anomalies = await self.detect_anomalies(recent_values)
        
        # Generate forecast (simplified)
        forecast_values = await self.generate_forecast(recent_values, days=7)
        
        trend_analysis = TrendAnalysis(
            metric_id=metric_id,
            analysis_period=analysis_period,
            trend_direction=trend_direction,
            trend_strength=trend_strength,
            rate_of_change=rate_of_change,
            seasonal_patterns={},  # Would calculate seasonal patterns with more data
            anomalies=anomalies,
            forecast_values=forecast_values,
            confidence_level=0.8  # Simplified confidence level
        )
        
        self.trend_analyses[metric_id] = trend_analysis
    
    async def calculate_linear_regression_slope(self, x_values: List[float], 
                                              y_values: List[float]) -> float:
        """Calculate slope of linear regression line"""
        
        if len(x_values) != len(y_values) or len(x_values) < 2:
            return 0.0
        
        n = len(x_values)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)
        
        denominator = n * sum_x2 - sum_x * sum_x
        if denominator == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / denominator
        return slope
    
    async def detect_anomalies(self, values: List[MetricValue]) -> List[Dict[str, Any]]:
        """Detect anomalies in metric values"""
        
        if len(values) < 5:
            return []
        
        value_list = [v.value for v in values]
        mean_value = statistics.mean(value_list)
        std_dev = statistics.stdev(value_list)
        
        anomalies = []
        for i, value_obj in enumerate(values):
            z_score = abs((value_obj.value - mean_value) / std_dev) if std_dev > 0 else 0
            
            if z_score > 2.5:  # More than 2.5 standard deviations
                anomalies.append({
                    "timestamp": value_obj.timestamp,
                    "value": value_obj.value,
                    "z_score": z_score,
                    "type": "statistical_outlier"
                })
        
        return anomalies
    
    async def generate_forecast(self, values: List[MetricValue], 
                              days: int) -> List[Tuple[datetime, float]]:
        """Generate simple forecast for metric values"""
        
        if len(values) < 3:
            return []
        
        # Simple linear extrapolation
        value_list = [v.value for v in values]
        timestamps = [(v.timestamp - values[0].timestamp).total_seconds() / 3600 for v in values]
        
        slope = await self.calculate_linear_regression_slope(timestamps, value_list)
        intercept = statistics.mean(value_list) - slope * statistics.mean(timestamps)
        
        forecast = []
        last_timestamp = values[-1].timestamp
        
        for i in range(1, days + 1):
            forecast_timestamp = last_timestamp + timedelta(days=i)
            hours_ahead = timestamps[-1] + (i * 24)
            forecast_value = intercept + slope * hours_ahead
            
            forecast.append((forecast_timestamp, forecast_value))
        
        return forecast
    
    async def generate_performance_report(self, report_type: str = "comprehensive",
                                        period_days: int = 30) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)
        
        report = {
            "report_metadata": {
                "report_type": report_type,
                "period_start": start_date.isoformat(),
                "period_end": end_date.isoformat(),
                "generated_at": datetime.now().isoformat(),
                "period_days": period_days
            },
            "executive_summary": {},
            "metric_performance": {},
            "trend_analysis": {},
            "alerts_summary": {},
            "benchmarking": {},
            "recommendations": []
        }
        
        # Executive Summary
        critical_metrics = ["csat_score", "nps_score", "churn_rate", "customer_lifetime_value"]
        summary_data = {}
        
        for metric_id in critical_metrics:
            if metric_id in self.metric_values and self.metric_values[metric_id]:
                recent_values = [v for v in self.metric_values[metric_id] 
                               if v.timestamp >= start_date]
                if recent_values:
                    current_value = recent_values[-1].value
                    avg_value = statistics.mean([v.value for v in recent_values])
                    summary_data[metric_id] = {
                        "current": current_value,
                        "average": avg_value,
                        "target": self.metric_definitions[metric_id].target_value,
                        "status": "on_track" if abs(current_value - self.metric_definitions[metric_id].target_value) <= self.metric_definitions[metric_id].target_value * 0.1 else "needs_attention"
                    }
        
        report["executive_summary"] = summary_data
        
        # Metric Performance
        for metric_id, metric_def in self.metric_definitions.items():
            if metric_id in self.metric_values and self.metric_values[metric_id]:
                period_values = [v for v in self.metric_values[metric_id] 
                               if v.timestamp >= start_date]
                
                if period_values:
                    values = [v.value for v in period_values]
                    report["metric_performance"][metric_id] = {
                        "name": metric_def.name,
                        "current_value": period_values[-1].value,
                        "period_average": statistics.mean(values),
                        "period_min": min(values),
                        "period_max": max(values),
                        "target_value": metric_def.target_value,
                        "target_achievement": (period_values[-1].value / metric_def.target_value * 100) if metric_def.target_value != 0 else 0,
                        "data_points": len(period_values),
                        "unit": metric_def.unit
                    }
        
        # Trend Analysis Summary
        for metric_id, trend in self.trend_analyses.items():
            report["trend_analysis"][metric_id] = {
                "direction": trend.trend_direction.value,
                "strength": trend.trend_strength,
                "rate_of_change": f"{trend.rate_of_change:.1f}%",
                "anomalies_detected": len(trend.anomalies),
                "confidence_level": trend.confidence_level
            }
        
        # Alerts Summary
        period_alerts = [alert for alert in self.alerts.values() 
                        if alert.triggered_at >= start_date]
        
        alert_summary = Counter([alert.severity.value for alert in period_alerts])
        report["alerts_summary"] = {
            "total_alerts": len(period_alerts),
            "by_severity": dict(alert_summary),
            "resolved_alerts": len([a for a in period_alerts if a.resolved]),
            "open_alerts": len([a for a in period_alerts if not a.resolved])
        }
        
        # Benchmarking
        for metric_id, current_performance in report["metric_performance"].items():
            if metric_id in self.industry_benchmarks:
                benchmarks = self.industry_benchmarks[metric_id]
                current_value = current_performance["current_value"]
                
                # Determine performance tier
                if current_value >= benchmarks["excellent"]:
                    tier = "excellent"
                elif current_value >= benchmarks["good"]:
                    tier = "good"
                elif current_value >= benchmarks["average"]:
                    tier = "average"
                else:
                    tier = "poor"
                
                report["benchmarking"][metric_id] = {
                    "current_tier": tier,
                    "benchmarks": benchmarks,
                    "gap_to_excellent": benchmarks["excellent"] - current_value
                }
        
        # Generate Recommendations
        recommendations = await self.generate_performance_recommendations(report)
        report["recommendations"] = recommendations
        
        return report
    
    async def generate_performance_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on performance analysis"""
        
        recommendations = []
        
        # Analyze metric performance for recommendations
        for metric_id, performance in report["metric_performance"].items():
            target_achievement = performance.get("target_achievement", 0)
            
            if target_achievement < 80:  # Less than 80% of target
                metric_def = self.metric_definitions[metric_id]
                
                if metric_id == "csat_score":
                    recommendations.append("Implement customer satisfaction improvement initiative - focus on support quality and response times")
                elif metric_id == "first_response_time":
                    recommendations.append("Optimize support team scheduling and implement automated acknowledgment for faster first responses")
                elif metric_id == "churn_rate":
                    recommendations.append("Launch customer retention program with proactive outreach and success coaching")
                elif metric_id == "automation_success_rate":
                    recommendations.append("Review and improve chatbot training data and automation routing logic")
        
        # Analyze trend directions
        declining_metrics = [metric_id for metric_id, trend in report["trend_analysis"].items() 
                           if trend["direction"] == "declining"]
        
        if len(declining_metrics) > 3:
            recommendations.append("Multiple metrics showing decline - conduct comprehensive service audit and improvement program")
        
        # Analyze alerts
        if report["alerts_summary"]["total_alerts"] > 10:
            recommendations.append("High alert volume indicates systematic issues - prioritize root cause analysis and prevention")
        
        # Benchmarking recommendations
        poor_performers = [metric_id for metric_id, benchmark in report["benchmarking"].items() 
                          if benchmark["current_tier"] == "poor"]
        
        if poor_performers:
            recommendations.append(f"Focus on improving {', '.join(poor_performers)} to meet industry standards")
        
        return recommendations[:10]  # Return top 10 recommendations
    
    async def get_dashboard_data(self, dashboard_id: str) -> Dict[str, Any]:
        """Get current data for specified dashboard"""
        
        if dashboard_id not in self.dashboards:
            raise ValueError(f"Dashboard not found: {dashboard_id}")
        
        dashboard = self.dashboards[dashboard_id]
        dashboard_data = {
            "dashboard_id": dashboard_id,
            "name": dashboard.name,
            "description": dashboard.description,
            "last_updated": datetime.now().isoformat(),
            "metrics": {}
        }
        
        for metric_id in dashboard.metrics:
            if metric_id in self.metric_values and self.metric_values[metric_id]:
                latest_value = self.metric_values[metric_id][-1]
                metric_def = self.metric_definitions[metric_id]
                
                # Calculate status
                if metric_def.is_higher_better:
                    if latest_value.value >= metric_def.target_value:
                        status = "excellent"
                    elif latest_value.value >= metric_def.threshold_warning:
                        status = "good"
                    elif latest_value.value >= metric_def.threshold_critical:
                        status = "warning"
                    else:
                        status = "critical"
                else:
                    if latest_value.value <= metric_def.target_value:
                        status = "excellent"
                    elif latest_value.value <= metric_def.threshold_warning:
                        status = "good"
                    elif latest_value.value <= metric_def.threshold_critical:
                        status = "warning"
                    else:
                        status = "critical"
                
                dashboard_data["metrics"][metric_id] = {
                    "name": metric_def.name,
                    "current_value": latest_value.value,
                    "target_value": metric_def.target_value,
                    "unit": metric_def.unit,
                    "status": status,
                    "timestamp": latest_value.timestamp.isoformat(),
                    "trend": self.trend_analyses.get(metric_id, {}).get("direction", "unknown") if metric_id in self.trend_analyses else "unknown"
                }
        
        return dashboard_data

# Example usage and testing
async def main():
    """Example usage of the Performance Metrics System"""
    
    # Initialize the system
    metrics_system = PerformanceMetricsSystem()
    
    print("=== Performance Metrics System Demo ===\n")
    
    # Simulate recording some metric values
    sample_data_sources = [
        {
            "metric_id": "csat_score",
            "data": {
                "satisfaction_scores": [4.2, 4.5, 4.1, 4.4, 4.3, 4.0, 4.6]
            }
        },
        {
            "metric_id": "first_response_time",
            "data": {
                "response_times_hours": [1.8, 2.1, 1.5, 2.8, 1.9, 2.0, 2.2]
            }
        },
        {
            "metric_id": "churn_rate",
            "data": {
                "churned_customers": 8,
                "total_customers": 150
            }
        },
        {
            "metric_id": "automation_success_rate",
            "data": {
                "successful_automations": 87,
                "total_automations": 100
            }
        },
        {
            "metric_id": "nps_score",
            "data": {
                "nps_scores": [9, 8, 7, 10, 9, 6, 8, 9, 10, 7, 8, 9]
            }
        }
    ]
    
    # Record metrics over time
    for i in range(7):  # Simulate 7 days of data
        timestamp = datetime.now() - timedelta(days=6-i)
        
        for data_source in sample_data_sources:
            metric_id = data_source["metric_id"]
            data = data_source["data"]
            
            # Calculate metric value
            value = await metrics_system.calculate_metric(metric_id, data)
            
            # Record the value
            await metrics_system.record_metric_value(
                metric_id=metric_id,
                value=value,
                timestamp=timestamp,
                metadata={"source": "automated_calculation", "period": "daily"},
                sample_size=len(data.get("satisfaction_scores", data.get("nps_scores", [1])))
            )
            
            print(f"Recorded {metric_id}: {value:.2f}")
    
    print("\n" + "="*60)
    
    # Generate performance report
    print("\n=== Performance Report ===")
    report = await metrics_system.generate_performance_report(period_days=7)
    
    print(f"Report Period: {report['report_metadata']['period_days']} days")
    print(f"Generated At: {report['report_metadata']['generated_at']}")
    
    print("\nExecutive Summary:")
    for metric_id, summary in report["executive_summary"].items():
        print(f"  {metric_id}: {summary['current']:.2f} (Target: {summary['target']:.2f}) - {summary['status']}")
    
    print("\nTrend Analysis:")
    for metric_id, trend in report["trend_analysis"].items():
        print(f"  {metric_id}: {trend['direction']} ({trend['rate_of_change']} change)")
    
    print(f"\nAlerts Summary:")
    print(f"  Total Alerts: {report['alerts_summary']['total_alerts']}")
    print(f"  By Severity: {report['alerts_summary']['by_severity']}")
    
    print("\nRecommendations:")
    for i, recommendation in enumerate(report["recommendations"], 1):
        print(f"  {i}. {recommendation}")
    
    # Show dashboard data
    print("\n=== Executive Dashboard ===")
    dashboard_data = await metrics_system.get_dashboard_data("executive_dashboard")
    
    for metric_id, metric_data in dashboard_data["metrics"].items():
        status_emoji = {"excellent": "✅", "good": "🟢", "warning": "🟡", "critical": "🔴"}.get(metric_data["status"], "⚪")
        print(f"  {status_emoji} {metric_data['name']}: {metric_data['current_value']:.2f} {metric_data['unit']} ({metric_data['status']})")
    
    # Show active alerts
    active_alerts = [alert for alert in metrics_system.alerts.values() if not alert.resolved]
    if active_alerts:
        print(f"\n=== Active Alerts ({len(active_alerts)}) ===")
        for alert in active_alerts[-5:]:  # Show last 5 alerts
            severity_emoji = {"critical": "🚨", "warning": "⚠️", "info": "ℹ️"}.get(alert.severity.value, "⚪")
            print(f"  {severity_emoji} {alert.message}")
            if alert.recommended_actions:
                print(f"    Action: {alert.recommended_actions[0]}")

if __name__ == "__main__":
    asyncio.run(main())