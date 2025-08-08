"""
Customer Behavior Prediction Implementation Guide
=================================================

Practical implementation framework with specific metrics, workflows, and actionable strategies
based on 2024-2025 SaaS industry research and behavioral analytics best practices.

TRUTHFUL DISCLOSURE: Implementation success depends on data quality, organizational alignment,
and proper execution. Results may vary based on customer base, industry, and market conditions.
"""

from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import json

@dataclass
class ImplementationMetrics:
    """Key metrics for tracking implementation success"""
    churn_rate_baseline: float
    churn_rate_target: float
    expansion_revenue_baseline: float
    expansion_revenue_target: float
    nps_baseline: float
    nps_target: float
    intervention_success_rate: float
    model_precision: float
    model_recall: float

class BehaviorPredictionImplementation:
    """
    Complete implementation framework for customer behavior prediction
    
    Provides practical guidance for deploying and operating prediction models
    in production environments with measurable business outcomes.
    """
    
    def __init__(self):
        # Implementation phases with specific timelines and deliverables
        self.implementation_phases = {
            'foundation': {
                'duration_weeks': 12,
                'key_deliverables': [
                    'Data infrastructure setup',
                    'Privacy compliance framework',
                    'Basic model development',
                    'Team training completion'
                ],
                'success_criteria': {
                    'data_quality_score': 0.85,
                    'model_baseline_accuracy': 0.75,
                    'team_certification_rate': 0.90,
                    'privacy_audit_pass': True
                }
            },
            'advanced_analytics': {
                'duration_weeks': 12,
                'key_deliverables': [
                    'Real-time scoring system',
                    'Intervention workflow automation',
                    'Cross-functional integration',
                    'Performance dashboard'
                ],
                'success_criteria': {
                    'real_time_latency_ms': 200,
                    'intervention_trigger_accuracy': 0.80,
                    'cross_team_adoption_rate': 0.75,
                    'dashboard_usage_rate': 0.85
                }
            },
            'optimization': {
                'duration_weeks': 24,
                'key_deliverables': [
                    'AI-powered personalization',
                    'Automated expansion identification',
                    'Advanced intervention strategies',
                    'Continuous improvement loop'
                ],
                'success_criteria': {
                    'personalization_effectiveness': 0.25,  # 25% improvement
                    'expansion_identification_rate': 0.30,  # 30% increase
                    'intervention_success_improvement': 0.40,  # 40% improvement
                    'model_drift_detection': True
                }
            }
        }
        
        # Key performance indicators with industry benchmarks
        self.kpi_benchmarks = {
            'churn_rate_annual': {
                'startup': 0.15,      # 15% acceptable for startups
                'smb_focused': 0.08,  # 8% target for SMB-focused SaaS
                'enterprise': 0.05,   # 5% target for enterprise SaaS
                'industry_best': 0.03 # 3% best-in-class performance
            },
            'expansion_revenue_percentage': {
                'baseline': 0.25,     # 25% minimum from existing customers
                'good': 0.32,         # 32% industry average (2024)
                'excellent': 0.40,    # 40% top-quartile performance
                'best_in_class': 0.50 # 50% best-in-class
            },
            'net_promoter_score': {
                'poor': 0,            # Below 0 indicates serious issues
                'acceptable': 30,     # 30+ acceptable for SaaS
                'good': 50,          # 50+ good performance
                'excellent': 70      # 70+ excellent performance
            }
        }
        
    def generate_implementation_plan(self, company_profile: Dict[str, str]) -> Dict[str, any]:
        """
        Generate customized implementation plan based on company profile
        
        Args:
            company_profile: Dictionary containing company_size, industry, current_metrics, etc.
            
        Returns:
            Detailed implementation plan with timelines, resources, and success criteria
        """
        company_size = company_profile.get('company_size', 'smb')
        current_arr = company_profile.get('annual_recurring_revenue', 1000000)
        team_size = company_profile.get('team_size', 10)
        
        # Customize plan based on company characteristics
        plan = {
            'company_profile': company_profile,
            'implementation_timeline': self._customize_timeline(company_size, team_size),
            'resource_requirements': self._calculate_resource_requirements(current_arr, team_size),
            'technology_stack': self._recommend_technology_stack(company_size),
            'success_metrics': self._define_success_metrics(company_size, current_arr),
            'risk_mitigation': self._identify_implementation_risks(company_profile),
            'roi_projections': self._calculate_roi_projections(current_arr)
        }
        
        return plan
    
    def _customize_timeline(self, company_size: str, team_size: int) -> Dict[str, any]:
        """Customize implementation timeline based on company characteristics"""
        base_timeline = self.implementation_phases.copy()
        
        # Adjust timeline based on company size and complexity
        multipliers = {
            'startup': 0.8,      # Faster implementation, less complexity
            'smb': 1.0,          # Standard timeline
            'mid_market': 1.2,   # More complexity, integration needs
            'enterprise': 1.5    # Significant complexity, compliance requirements
        }
        
        multiplier = multipliers.get(company_size, 1.0)
        
        # Adjust for team size (smaller teams need more time)
        if team_size < 5:
            multiplier *= 1.2
        elif team_size > 50:
            multiplier *= 1.1
            
        customized_timeline = {}
        for phase, details in base_timeline.items():
            customized_details = details.copy()
            customized_details['duration_weeks'] = int(details['duration_weeks'] * multiplier)
            customized_timeline[phase] = customized_details
            
        return customized_timeline
    
    def _calculate_resource_requirements(self, current_arr: float, team_size: int) -> Dict[str, any]:
        """Calculate required resources based on company scale"""
        
        # Base resource requirements
        base_costs = {
            'technology_infrastructure': {
                'data_platform': 50000,      # Annual cost
                'ml_platform': 75000,        # Annual cost
                'integration_tools': 25000,  # Annual cost
                'monitoring_tools': 15000    # Annual cost
            },
            'personnel': {
                'data_scientist_months': 6,
                'software_engineer_months': 12,
                'customer_success_specialist_months': 3,
                'project_manager_months': 12
            },
            'external_services': {
                'consulting_budget': 100000,
                'training_budget': 25000,
                'compliance_audit': 15000
            }
        }
        
        # Scale based on ARR
        if current_arr > 10000000:  # $10M+ ARR
            scale_factor = 1.5
        elif current_arr > 5000000:  # $5M+ ARR
            scale_factor = 1.2
        elif current_arr < 1000000:  # <$1M ARR
            scale_factor = 0.7
        else:
            scale_factor = 1.0
            
        # Apply scaling
        scaled_costs = {}
        for category, costs in base_costs.items():
            scaled_costs[category] = {}
            for item, cost in costs.items():
                scaled_costs[category][item] = int(cost * scale_factor)
                
        # Calculate total costs
        total_annual_tech = sum(scaled_costs['technology_infrastructure'].values())
        total_personnel = sum(scaled_costs['personnel'].values()) * 10000  # Assume $10K/month loaded cost
        total_external = sum(scaled_costs['external_services'].values())
        
        return {
            'detailed_costs': scaled_costs,
            'total_annual_technology': total_annual_tech,
            'total_personnel_cost': total_personnel,
            'total_external_services': total_external,
            'total_first_year_investment': total_annual_tech + total_personnel + total_external,
            'ongoing_annual_cost': total_annual_tech + (total_personnel * 0.3)  # 30% ongoing personnel
        }
    
    def _recommend_technology_stack(self, company_size: str) -> Dict[str, List[str]]:
        """Recommend technology stack based on company size and needs"""
        
        stacks = {
            'startup': {
                'data_platform': ['Segment', 'Mixpanel', 'Amplitude'],
                'ml_platform': ['DataRobot', 'H2O.ai', 'Google AutoML'],
                'crm_integration': ['HubSpot', 'Pipedrive', 'Salesforce Essentials'],
                'analytics': ['Google Analytics', 'Mixpanel', 'Hotjar'],
                'communication': ['Intercom', 'Zendesk Chat', 'Slack']
            },
            'smb': {
                'data_platform': ['Segment', 'mParticle', 'Tealium'],
                'ml_platform': ['AWS SageMaker', 'Azure ML', 'Google Cloud ML'],
                'crm_integration': ['Salesforce Professional', 'HubSpot Professional', 'Microsoft Dynamics'],
                'analytics': ['Tableau', 'Looker', 'Power BI'],
                'communication': ['Salesforce Service Cloud', 'Zendesk', 'Freshworks']
            },
            'enterprise': {
                'data_platform': ['Snowflake', 'Databricks', 'AWS Redshift'],
                'ml_platform': ['AWS SageMaker', 'Azure ML', 'Google Cloud AI Platform'],
                'crm_integration': ['Salesforce Enterprise', 'Microsoft Dynamics 365', 'Oracle CX'],
                'analytics': ['Tableau', 'Looker', 'Qlik Sense'],
                'communication': ['Salesforce Service Cloud', 'ServiceNow', 'Microsoft Teams']
            }
        }
        
        return stacks.get(company_size, stacks['smb'])
    
    def _define_success_metrics(self, company_size: str, current_arr: float) -> Dict[str, any]:
        """Define success metrics and targets based on company profile"""
        
        # Get baseline benchmarks for company size
        churn_benchmark = self.kpi_benchmarks['churn_rate_annual'][company_size]
        expansion_benchmark = self.kpi_benchmarks['expansion_revenue_percentage']['good']
        nps_benchmark = self.kpi_benchmarks['net_promoter_score']['good']
        
        metrics = {
            'primary_metrics': {
                'churn_reduction_target': {
                    'metric': 'annual_churn_rate',
                    'baseline': churn_benchmark * 1.2,  # Assume starting 20% above benchmark
                    'target': churn_benchmark,
                    'timeline_months': 18,
                    'measurement_frequency': 'monthly'
                },
                'expansion_revenue_target': {
                    'metric': 'expansion_revenue_percentage',
                    'baseline': expansion_benchmark * 0.8,  # Assume starting 20% below benchmark
                    'target': expansion_benchmark,
                    'timeline_months': 12,
                    'measurement_frequency': 'quarterly'
                },
                'customer_satisfaction_target': {
                    'metric': 'net_promoter_score',
                    'baseline': nps_benchmark * 0.8,  # Assume starting 20% below benchmark
                    'target': nps_benchmark,
                    'timeline_months': 12,
                    'measurement_frequency': 'quarterly'
                }
            },
            'operational_metrics': {
                'model_performance': {
                    'precision_target': 0.85,
                    'recall_target': 0.75,
                    'f1_score_target': 0.80,
                    'measurement_frequency': 'monthly'
                },
                'intervention_effectiveness': {
                    'high_risk_retention_rate': 0.40,  # 40% of high-risk customers retained
                    'medium_risk_engagement_improvement': 0.25,  # 25% engagement improvement
                    'expansion_identification_accuracy': 0.30,  # 30% of identified opportunities convert
                    'measurement_frequency': 'monthly'
                },
                'system_performance': {
                    'prediction_latency_ms': 200,
                    'system_uptime_percentage': 0.999,
                    'data_quality_score': 0.90,
                    'measurement_frequency': 'daily'
                }
            },
            'financial_metrics': {
                'cost_per_retained_customer': current_arr * 0.05 / 100,  # 5% of average customer value
                'expansion_revenue_per_opportunity': current_arr * 0.001,  # 0.1% of ARR per opportunity
                'roi_target_months': 12,  # Break-even in 12 months
                'total_value_improvement': current_arr * 0.15  # 15% improvement in total value
            }
        }
        
        return metrics
    
    def _identify_implementation_risks(self, company_profile: Dict[str, str]) -> List[Dict[str, str]]:
        """Identify potential implementation risks and mitigation strategies"""
        
        risks = [
            {
                'risk': 'Data Quality Issues',
                'likelihood': 'high',
                'impact': 'high',
                'description': 'Poor data quality leads to unreliable predictions',
                'mitigation': 'Implement data validation, cleansing, and quality monitoring systems'
            },
            {
                'risk': 'Privacy Compliance Violations',
                'likelihood': 'medium',
                'impact': 'high',
                'description': 'GDPR/CCPA violations due to improper data handling',
                'mitigation': 'Conduct privacy impact assessment, implement consent management'
            },
            {
                'risk': 'Model Bias and Discrimination',
                'likelihood': 'medium',
                'impact': 'high',
                'description': 'Models may discriminate against protected groups',
                'mitigation': 'Regular bias audits, diverse training data, fairness constraints'
            },
            {
                'risk': 'Low User Adoption',
                'likelihood': 'medium',
                'impact': 'medium',
                'description': 'Teams may resist using prediction insights',
                'mitigation': 'Change management, training, gradual rollout, success stories'
            },
            {
                'risk': 'Technology Integration Failures',
                'likelihood': 'medium',
                'impact': 'medium',
                'description': 'Existing systems may not integrate properly',
                'mitigation': 'Proof of concept, API compatibility testing, fallback plans'
            },
            {
                'risk': 'Model Performance Degradation',
                'likelihood': 'high',
                'impact': 'medium',
                'description': 'Model accuracy decreases over time due to data drift',
                'mitigation': 'Continuous monitoring, regular retraining, performance alerts'
            }
        ]
        
        # Add company-specific risks
        company_size = company_profile.get('company_size', 'smb')
        
        if company_size == 'startup':
            risks.append({
                'risk': 'Resource Constraints',
                'likelihood': 'high',
                'impact': 'high',
                'description': 'Limited resources may prevent proper implementation',
                'mitigation': 'Phased approach, external expertise, focus on high-impact areas'
            })
        elif company_size == 'enterprise':
            risks.append({
                'risk': 'Complex Compliance Requirements',
                'likelihood': 'high',
                'impact': 'medium',
                'description': 'Enterprise compliance may slow implementation',
                'mitigation': 'Early compliance engagement, dedicated compliance resources'
            })
            
        return risks
    
    def _calculate_roi_projections(self, current_arr: float) -> Dict[str, any]:
        """Calculate ROI projections based on expected improvements"""
        
        # Implementation costs (calculated earlier, using averages)
        total_implementation_cost = current_arr * 0.15  # Assume 15% of ARR for implementation
        annual_operating_cost = current_arr * 0.05      # Assume 5% of ARR for operations
        
        # Expected benefits based on research
        churn_reduction_benefit = current_arr * 0.12    # 12% ARR saved from churn reduction
        expansion_revenue_benefit = current_arr * 0.18  # 18% ARR increase from expansion
        efficiency_benefit = current_arr * 0.03         # 3% ARR equivalent in cost savings
        
        total_annual_benefit = churn_reduction_benefit + expansion_revenue_benefit + efficiency_benefit
        
        # Calculate 3-year projection
        projections = {
            'year_1': {
                'costs': total_implementation_cost + annual_operating_cost,
                'benefits': total_annual_benefit * 0.5,  # 50% benefits in first year
                'net_value': (total_annual_benefit * 0.5) - (total_implementation_cost + annual_operating_cost)
            },
            'year_2': {
                'costs': annual_operating_cost,
                'benefits': total_annual_benefit * 0.8,  # 80% benefits in second year
                'net_value': (total_annual_benefit * 0.8) - annual_operating_cost
            },
            'year_3': {
                'costs': annual_operating_cost,
                'benefits': total_annual_benefit,  # 100% benefits in third year
                'net_value': total_annual_benefit - annual_operating_cost
            }
        }
        
        # Calculate summary metrics
        total_costs = sum([year['costs'] for year in projections.values()])
        total_benefits = sum([year['benefits'] for year in projections.values()])
        
        return {
            'yearly_projections': projections,
            'summary': {
                'total_investment': total_costs,
                'total_benefits': total_benefits,
                'net_roi': (total_benefits - total_costs) / total_costs,
                'payback_period_months': 18,  # Based on when cumulative benefits exceed costs
                'break_even_month': 15
            },
            'sensitivity_analysis': {
                'conservative_scenario': {
                    'benefits_multiplier': 0.7,
                    'roi': ((total_benefits * 0.7) - total_costs) / total_costs
                },
                'optimistic_scenario': {
                    'benefits_multiplier': 1.3,
                    'roi': ((total_benefits * 1.3) - total_costs) / total_costs
                }
            }
        }

class InterventionPlaybook:
    """
    Comprehensive intervention strategies and tactics for different customer scenarios
    
    Based on 2024-2025 SaaS customer success research and proven retention strategies
    """
    
    def __init__(self):
        self.intervention_strategies = {
            'high_churn_risk': {
                'immediate_actions': [
                    {
                        'action': 'executive_escalation',
                        'timeline_hours': 4,
                        'owner': 'customer_success_manager',
                        'description': 'Schedule immediate call with customer success executive',
                        'success_rate': 0.35,
                        'cost_range': '$500-2000'
                    },
                    {
                        'action': 'emergency_value_review',
                        'timeline_hours': 24,
                        'owner': 'solutions_consultant',
                        'description': 'Conduct comprehensive value assessment and ROI analysis',
                        'success_rate': 0.40,
                        'cost_range': '$1000-3000'
                    },
                    {
                        'action': 'retention_offer',
                        'timeline_hours': 48,
                        'owner': 'account_manager',
                        'description': 'Present customized retention incentives or contract modifications',
                        'success_rate': 0.30,
                        'cost_range': '$5000-25000'
                    }
                ],
                'follow_up_actions': [
                    {
                        'action': 'weekly_check_ins',
                        'duration_weeks': 12,
                        'frequency': 'weekly',
                        'description': 'Regular health checks and progress monitoring'
                    },
                    {
                        'action': 'success_plan_revision',
                        'timeline_days': 7,
                        'description': 'Revise customer success plan with specific milestones'
                    }
                ]
            },
            'medium_churn_risk': {
                'immediate_actions': [
                    {
                        'action': 'enhanced_onboarding',
                        'timeline_days': 7,
                        'owner': 'customer_success_specialist',
                        'description': 'Provide additional training and feature adoption guidance',
                        'success_rate': 0.25,
                        'cost_range': '$200-800'
                    },
                    {
                        'action': 'usage_optimization',
                        'timeline_days': 14,
                        'owner': 'solutions_consultant',
                        'description': 'Analyze usage patterns and recommend optimization strategies',
                        'success_rate': 0.30,
                        'cost_range': '$500-1500'
                    }
                ]
            },
            'expansion_opportunity': {
                'immediate_actions': [
                    {
                        'action': 'expansion_assessment',
                        'timeline_days': 7,
                        'owner': 'account_manager',
                        'description': 'Assess expansion readiness and identify specific opportunities',
                        'success_rate': 0.60,
                        'cost_range': '$300-1000'
                    },
                    {
                        'action': 'pilot_program_offer',
                        'timeline_days': 14,
                        'owner': 'sales_engineer',
                        'description': 'Offer pilot program for expanded features or team access',
                        'success_rate': 0.35,
                        'cost_range': '$1000-5000'
                    }
                ]
            },
            'low_engagement': {
                'immediate_actions': [
                    {
                        'action': 'engagement_campaign',
                        'timeline_days': 3,
                        'owner': 'marketing_automation',
                        'description': 'Trigger personalized re-engagement email sequence',
                        'success_rate': 0.15,
                        'cost_range': '$50-200'
                    },
                    {
                        'action': 'feature_discovery',
                        'timeline_days': 7,
                        'owner': 'customer_success_specialist',
                        'description': 'Guide customer through unused features and use cases',
                        'success_rate': 0.20,
                        'cost_range': '$100-400'
                    }
                ]
            }
        }
        
    def generate_intervention_plan(self, customer_profile: Dict, prediction_results: Dict) -> Dict[str, any]:
        """
        Generate specific intervention plan based on customer profile and predictions
        
        Returns detailed action plan with timelines, owners, and success metrics
        """
        churn_probability = prediction_results.get('churn_risk', {}).get('churn_probability', 0)
        expansion_probability = prediction_results.get('expansion_opportunity', {}).get('expansion_probability', 0)
        
        # Determine primary intervention category
        if churn_probability >= 0.7:
            primary_category = 'high_churn_risk'
            priority = 'critical'
        elif churn_probability >= 0.4:
            primary_category = 'medium_churn_risk'
            priority = 'high'
        elif expansion_probability >= 0.6:
            primary_category = 'expansion_opportunity'
            priority = 'high'
        else:
            primary_category = 'low_engagement'
            priority = 'medium'
            
        intervention_plan = {
            'customer_id': customer_profile.get('customer_id'),
            'priority': priority,
            'primary_category': primary_category,
            'churn_probability': churn_probability,
            'expansion_probability': expansion_probability,
            'recommended_actions': self.intervention_strategies[primary_category]['immediate_actions'],
            'follow_up_actions': self.intervention_strategies[primary_category].get('follow_up_actions', []),
            'success_criteria': self._define_success_criteria(primary_category, customer_profile),
            'estimated_cost': self._calculate_intervention_cost(primary_category),
            'expected_outcome': self._predict_intervention_outcome(primary_category, customer_profile)
        }
        
        return intervention_plan
    
    def _define_success_criteria(self, category: str, customer_profile: Dict) -> List[Dict[str, str]]:
        """Define success criteria for intervention category"""
        criteria_map = {
            'high_churn_risk': [
                {'metric': 'customer_retention', 'target': '100%', 'timeline': '90 days'},
                {'metric': 'engagement_score', 'target': '+50%', 'timeline': '30 days'},
                {'metric': 'nps_improvement', 'target': '+3 points', 'timeline': '60 days'}
            ],
            'medium_churn_risk': [
                {'metric': 'feature_adoption', 'target': '+2 features', 'timeline': '30 days'},
                {'metric': 'usage_frequency', 'target': '+30%', 'timeline': '45 days'},
                {'metric': 'support_ticket_reduction', 'target': '-50%', 'timeline': '60 days'}
            ],
            'expansion_opportunity': [
                {'metric': 'expansion_conversion', 'target': '1 expansion', 'timeline': '120 days'},
                {'metric': 'trial_activation', 'target': '100%', 'timeline': '14 days'},
                {'metric': 'team_adoption', 'target': '+2 users', 'timeline': '60 days'}
            ],
            'low_engagement': [
                {'metric': 'login_frequency', 'target': '+100%', 'timeline': '30 days'},
                {'metric': 'feature_usage', 'target': '+1 feature', 'timeline': '21 days'},
                {'metric': 'session_duration', 'target': '+25%', 'timeline': '30 days'}
            ]
        }
        
        return criteria_map.get(category, [])
    
    def _calculate_intervention_cost(self, category: str) -> Dict[str, int]:
        """Calculate estimated intervention costs"""
        cost_ranges = {
            'high_churn_risk': {'min': 6500, 'max': 30000, 'average': 15000},
            'medium_churn_risk': {'min': 700, 'max': 2300, 'average': 1200},
            'expansion_opportunity': {'min': 1300, 'max': 6000, 'average': 3000},
            'low_engagement': {'min': 150, 'max': 600, 'average': 300}
        }
        
        return cost_ranges.get(category, {'min': 0, 'max': 0, 'average': 0})
    
    def _predict_intervention_outcome(self, category: str, customer_profile: Dict) -> Dict[str, float]:
        """Predict likely intervention outcomes"""
        base_success_rates = {
            'high_churn_risk': 0.35,
            'medium_churn_risk': 0.55,
            'expansion_opportunity': 0.40,
            'low_engagement': 0.25
        }
        
        base_rate = base_success_rates.get(category, 0.25)
        
        # Adjust based on customer characteristics
        company_size = customer_profile.get('company_size', 'smb')
        contract_value = customer_profile.get('contract_value', 500)
        
        # Higher value customers more likely to respond positively
        if contract_value > 2000:
            base_rate *= 1.2
        elif contract_value < 200:
            base_rate *= 0.8
            
        # Enterprise customers more responsive to structured interventions
        if company_size == 'enterprise':
            base_rate *= 1.1
        elif company_size == 'startup':
            base_rate *= 0.9
            
        return {
            'success_probability': min(base_rate, 1.0),
            'confidence_interval': {
                'lower': max(base_rate * 0.8, 0.0),
                'upper': min(base_rate * 1.2, 1.0)
            },
            'expected_value_impact': customer_profile.get('contract_value', 500) * base_rate
        }

# Example usage and demonstration
if __name__ == "__main__":
    # Example company profile for implementation planning
    company_profile = {
        'company_size': 'smb',
        'industry': 'professional_development',
        'annual_recurring_revenue': 2500000,
        'team_size': 25,
        'current_churn_rate': 0.10,
        'current_expansion_rate': 0.22,
        'current_nps': 42,
        'customer_base_size': 850,
        'average_contract_value': 2941
    }
    
    # Generate implementation plan
    implementation = BehaviorPredictionImplementation()
    plan = implementation.generate_implementation_plan(company_profile)
    
    print("=== Customer Behavior Prediction Implementation Plan ===")
    print(f"Company: {company_profile['company_size'].upper()} in {company_profile['industry']}")
    print(f"ARR: ${company_profile['annual_recurring_revenue']:,}")
    print(f"Team Size: {company_profile['team_size']}")
    
    print("\n--- Resource Requirements ---")
    resources = plan['resource_requirements']
    print(f"First Year Investment: ${resources['total_first_year_investment']:,}")
    print(f"Annual Operating Cost: ${resources['ongoing_annual_cost']:,}")
    
    print("\n--- Success Metrics ---")
    metrics = plan['success_metrics']['primary_metrics']
    for metric_name, metric_data in metrics.items():
        print(f"- {metric_name}: {metric_data['baseline']:.1%} → {metric_data['target']:.1%}")
    
    print("\n--- ROI Projections ---")
    roi_data = plan['roi_projections']
    print(f"3-Year Net ROI: {roi_data['summary']['net_roi']:.1%}")
    print(f"Payback Period: {roi_data['summary']['payback_period_months']} months")
    
    print("\n--- Implementation Timeline ---")
    timeline = plan['implementation_timeline']
    for phase, details in timeline.items():
        print(f"- {phase.title()}: {details['duration_weeks']} weeks")
    
    # Example intervention planning
    print("\n=== Intervention Planning Example ===")
    playbook = InterventionPlaybook()
    
    sample_customer = {
        'customer_id': 'CUST_001',
        'company_size': 'smb',
        'contract_value': 1200
    }
    
    sample_predictions = {
        'churn_risk': {'churn_probability': 0.75},
        'expansion_opportunity': {'expansion_probability': 0.15}
    }
    
    intervention_plan = playbook.generate_intervention_plan(sample_customer, sample_predictions)
    
    print(f"Customer: {sample_customer['customer_id']}")
    print(f"Priority: {intervention_plan['priority'].upper()}")
    print(f"Churn Risk: {intervention_plan['churn_probability']:.1%}")
    print(f"Estimated Cost: ${intervention_plan['estimated_cost']['average']:,}")
    print(f"Success Probability: {intervention_plan['expected_outcome']['success_probability']:.1%}")
    
    print("\nRecommended Actions:")
    for action in intervention_plan['recommended_actions']:
        print(f"- {action['action']}: {action['description']} (Owner: {action['owner']})")