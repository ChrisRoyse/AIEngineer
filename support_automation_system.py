"""
Support Automation System for Christopher's Coaching Business
Focus: Automated ticket classification, routing, escalation, and resolution workflows
"""

import asyncio
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, asdict
from enum import Enum
import logging

class TicketPriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5

class TicketStatus(Enum):
    NEW = "new"
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PENDING_CUSTOMER = "pending_customer"
    PENDING_INTERNAL = "pending_internal"
    RESOLVED = "resolved"
    CLOSED = "closed"
    CANCELED = "canceled"

class TicketCategory(Enum):
    TECHNICAL_SUPPORT = "technical_support"
    BILLING_INQUIRY = "billing_inquiry"
    PROGRAM_QUESTION = "program_question"
    SCHEDULING = "scheduling"
    ACCOUNT_ACCESS = "account_access"
    REFUND_REQUEST = "refund_request"
    COMPLAINT = "complaint"
    FEATURE_REQUEST = "feature_request"
    GENERAL_INQUIRY = "general_inquiry"
    EMERGENCY = "emergency"

class AutomationRule(Enum):
    AUTO_ASSIGN = "auto_assign"
    AUTO_RESPOND = "auto_respond"
    AUTO_ESCALATE = "auto_escalate"
    AUTO_CLOSE = "auto_close"
    AUTO_FOLLOW_UP = "auto_follow_up"
    AUTO_SURVEY = "auto_survey"

class AgentSkill(Enum):
    TECHNICAL = "technical"
    BILLING = "billing"
    COACHING = "coaching"
    SALES = "sales"
    MANAGEMENT = "management"
    CUSTOMER_SUCCESS = "customer_success"

@dataclass
class Agent:
    agent_id: str
    name: str
    email: str
    skills: List[AgentSkill]
    max_concurrent_tickets: int
    current_ticket_count: int
    availability_hours: Dict[str, Tuple[int, int]]  # day: (start_hour, end_hour)
    performance_metrics: Dict[str, float]
    is_available: bool
    timezone: str

@dataclass
class AutomationRule:
    rule_id: str
    name: str
    description: str
    conditions: Dict[str, Any]
    actions: List[Dict[str, Any]]
    priority: int
    is_active: bool
    created_date: datetime
    last_triggered: Optional[datetime]
    trigger_count: int

@dataclass
class Ticket:
    ticket_id: str
    customer_id: str
    title: str
    description: str
    category: TicketCategory
    priority: TicketPriority
    status: TicketStatus
    channel: str
    created_at: datetime
    updated_at: datetime
    assigned_agent_id: Optional[str]
    tags: List[str]
    sentiment_score: float
    urgency_score: float
    resolution_target: datetime
    first_response_target: datetime
    first_response_time: Optional[datetime]
    resolution_time: Optional[datetime]
    satisfaction_rating: Optional[int]
    metadata: Dict[str, Any]
    conversation_history: List[Dict[str, Any]]
    escalation_history: List[Dict[str, Any]]
    automation_flags: List[str]

@dataclass
class KnowledgeArticle:
    article_id: str
    title: str
    content: str
    category: TicketCategory
    keywords: List[str]
    confidence_threshold: float
    usage_count: int
    effectiveness_score: float
    last_updated: datetime

class SupportAutomationSystem:
    """
    Comprehensive support automation system featuring:
    - Intelligent ticket classification and routing
    - Automated responses and escalation
    - Performance tracking and optimization
    - Knowledge base integration
    - SLA monitoring and enforcement
    """
    
    def __init__(self):
        self.tickets: Dict[str, Ticket] = {}
        self.agents: Dict[str, Agent] = {}
        self.automation_rules: Dict[str, AutomationRule] = {}
        self.knowledge_base: Dict[str, KnowledgeArticle] = {}
        self.performance_metrics: Dict[str, Any] = {}
        
        self.setup_agents()
        self.setup_automation_rules()
        self.setup_knowledge_base()
        self.setup_classification_patterns()
        self.setup_sla_targets()
    
    def setup_agents(self):
        """Initialize agent profiles with skills and availability"""
        
        agents_config = [
            {
                "agent_id": "AGT001",
                "name": "Sarah Johnson",
                "email": "sarah@coaching.com",
                "skills": [AgentSkill.TECHNICAL, AgentSkill.ACCOUNT_ACCESS],
                "max_concurrent_tickets": 8,
                "availability": {"monday": (9, 17), "tuesday": (9, 17), "wednesday": (9, 17), "thursday": (9, 17), "friday": (9, 17)}
            },
            {
                "agent_id": "AGT002", 
                "name": "Mike Chen",
                "email": "mike@coaching.com",
                "skills": [AgentSkill.BILLING, AgentSkill.SALES],
                "max_concurrent_tickets": 6,
                "availability": {"monday": (8, 16), "tuesday": (8, 16), "wednesday": (8, 16), "thursday": (8, 16), "friday": (8, 16)}
            },
            {
                "agent_id": "AGT003",
                "name": "Emily Rodriguez", 
                "email": "emily@coaching.com",
                "skills": [AgentSkill.COACHING, AgentSkill.CUSTOMER_SUCCESS],
                "max_concurrent_tickets": 10,
                "availability": {"monday": (10, 18), "tuesday": (10, 18), "wednesday": (10, 18), "thursday": (10, 18), "friday": (10, 18)}
            },
            {
                "agent_id": "AGT004",
                "name": "David Wilson",
                "email": "david@coaching.com", 
                "skills": [AgentSkill.MANAGEMENT, AgentSkill.COACHING, AgentSkill.CUSTOMER_SUCCESS],
                "max_concurrent_tickets": 5,
                "availability": {"monday": (9, 17), "tuesday": (9, 17), "wednesday": (9, 17), "thursday": (9, 17), "friday": (9, 17)}
            }
        ]
        
        for config in agents_config:
            agent = Agent(
                agent_id=config["agent_id"],
                name=config["name"],
                email=config["email"],
                skills=config["skills"],
                max_concurrent_tickets=config["max_concurrent_tickets"],
                current_ticket_count=0,
                availability_hours=config["availability"],
                performance_metrics={
                    "avg_resolution_time": 24.0,
                    "first_response_time": 2.0,
                    "customer_satisfaction": 4.5,
                    "tickets_resolved": 150,
                    "escalation_rate": 0.05
                },
                is_available=True,
                timezone="EST"
            )
            self.agents[agent.agent_id] = agent
    
    def setup_automation_rules(self):
        """Setup automation rules for ticket processing"""
        
        rules_config = [
            {
                "rule_id": "AR001",
                "name": "Auto-assign technical tickets",
                "description": "Automatically assign technical support tickets to technical agents",
                "conditions": {
                    "category": [TicketCategory.TECHNICAL_SUPPORT, TicketCategory.ACCOUNT_ACCESS],
                    "priority": [TicketPriority.LOW, TicketPriority.NORMAL, TicketPriority.HIGH]
                },
                "actions": [
                    {"type": "assign_agent", "skill_required": AgentSkill.TECHNICAL}
                ],
                "priority": 1
            },
            {
                "rule_id": "AR002", 
                "name": "Auto-escalate urgent complaints",
                "description": "Escalate complaints with high urgency to management",
                "conditions": {
                    "category": [TicketCategory.COMPLAINT],
                    "priority": [TicketPriority.HIGH, TicketPriority.URGENT, TicketPriority.CRITICAL]
                },
                "actions": [
                    {"type": "escalate", "target_skill": AgentSkill.MANAGEMENT},
                    {"type": "notify_manager"}
                ],
                "priority": 1
            },
            {
                "rule_id": "AR003",
                "name": "Auto-respond to billing inquiries", 
                "description": "Send automated response to billing questions",
                "conditions": {
                    "category": [TicketCategory.BILLING_INQUIRY],
                    "keywords": ["invoice", "payment", "charge", "bill"]
                },
                "actions": [
                    {"type": "auto_response", "template": "billing_inquiry_response"}
                ],
                "priority": 2
            },
            {
                "rule_id": "AR004",
                "name": "Follow-up on pending tickets",
                "description": "Automatically follow up on tickets pending customer response",
                "conditions": {
                    "status": [TicketStatus.PENDING_CUSTOMER],
                    "hours_since_update": 48
                },
                "actions": [
                    {"type": "send_reminder", "template": "customer_followup"}
                ],
                "priority": 3
            },
            {
                "rule_id": "AR005",
                "name": "Close resolved tickets",
                "description": "Automatically close tickets that have been resolved for 7 days",
                "conditions": {
                    "status": [TicketStatus.RESOLVED],
                    "hours_since_resolution": 168  # 7 days
                },
                "actions": [
                    {"type": "close_ticket"},
                    {"type": "send_satisfaction_survey"}
                ],
                "priority": 4
            }
        ]
        
        for config in rules_config:
            rule = AutomationRule(
                rule_id=config["rule_id"],
                name=config["name"],
                description=config["description"],
                conditions=config["conditions"],
                actions=config["actions"],
                priority=config["priority"],
                is_active=True,
                created_date=datetime.now(),
                last_triggered=None,
                trigger_count=0
            )
            self.automation_rules[rule.rule_id] = rule
    
    def setup_knowledge_base(self):
        """Initialize knowledge base with common solutions"""
        
        articles = [
            {
                "title": "How to Reset Your Password",
                "content": "To reset your password: 1) Go to login page 2) Click 'Forgot Password' 3) Enter your email 4) Check your inbox for reset link",
                "category": TicketCategory.ACCOUNT_ACCESS,
                "keywords": ["password", "reset", "login", "access", "forgot"]
            },
            {
                "title": "Understanding Your Coaching Program",
                "content": "Your coaching program includes: weekly 1-on-1 sessions, access to resources, email support, and progress tracking tools.",
                "category": TicketCategory.PROGRAM_QUESTION,
                "keywords": ["program", "coaching", "sessions", "resources", "what's included"]
            },
            {
                "title": "Billing and Payment Information",
                "content": "Payments are processed monthly. You can update your payment method in your account settings. Receipts are sent via email.",
                "category": TicketCategory.BILLING_INQUIRY,
                "keywords": ["billing", "payment", "invoice", "charge", "receipt"]
            },
            {
                "title": "Scheduling Your Coaching Sessions",
                "content": "Schedule sessions through your client portal or contact your coach directly. 24-hour cancellation notice required.",
                "category": TicketCategory.SCHEDULING,
                "keywords": ["schedule", "booking", "appointment", "session", "reschedule"]
            },
            {
                "title": "Technical Support Troubleshooting",
                "content": "For technical issues: 1) Clear browser cache 2) Try incognito mode 3) Check internet connection 4) Try different browser",
                "category": TicketCategory.TECHNICAL_SUPPORT,
                "keywords": ["technical", "error", "not working", "broken", "bug"]
            }
        ]
        
        for i, article in enumerate(articles):
            kb_article = KnowledgeArticle(
                article_id=f"KB{i+1:03d}",
                title=article["title"],
                content=article["content"],
                category=article["category"],
                keywords=article["keywords"],
                confidence_threshold=0.7,
                usage_count=0,
                effectiveness_score=0.8,
                last_updated=datetime.now()
            )
            self.knowledge_base[kb_article.article_id] = kb_article
    
    def setup_classification_patterns(self):
        """Setup patterns for automatic ticket classification"""
        
        self.classification_patterns = {
            TicketCategory.TECHNICAL_SUPPORT: [
                r'\b(error|bug|broken|not working|technical issue|can\'t access|website down)\b',
                r'\b(login|password|access|account)\b.*\b(problem|issue|error)\b'
            ],
            TicketCategory.BILLING_INQUIRY: [
                r'\b(bill|billing|invoice|payment|charge|refund|subscription)\b',
                r'\b(credit card|payment method|auto-renewal|cancel subscription)\b'
            ],
            TicketCategory.PROGRAM_QUESTION: [
                r'\b(coaching|program|session|curriculum|materials)\b',
                r'\b(what\'s included|how it works|program details)\b'
            ],
            TicketCategory.SCHEDULING: [
                r'\b(schedule|reschedule|appointment|booking|session time)\b',
                r'\b(calendar|availability|meeting|session)\b'
            ],
            TicketCategory.COMPLAINT: [
                r'\b(complaint|unhappy|dissatisfied|disappointed|terrible|awful)\b',
                r'\b(angry|frustrated|worst|horrible|unacceptable)\b'
            ],
            TicketCategory.REFUND_REQUEST: [
                r'\b(refund|money back|cancel|return|reimbursement)\b',
                r'\b(want my money|get refund|cancel subscription)\b'
            ]
        }
    
    def setup_sla_targets(self):
        """Setup SLA targets for different ticket types"""
        
        self.sla_targets = {
            TicketPriority.CRITICAL: {"first_response_hours": 1, "resolution_hours": 4},
            TicketPriority.URGENT: {"first_response_hours": 2, "resolution_hours": 8}, 
            TicketPriority.HIGH: {"first_response_hours": 4, "resolution_hours": 24},
            TicketPriority.NORMAL: {"first_response_hours": 8, "resolution_hours": 48},
            TicketPriority.LOW: {"first_response_hours": 24, "resolution_hours": 120}
        }
    
    async def create_ticket(self, customer_id: str, title: str, description: str, 
                          channel: str, metadata: Dict[str, Any] = None) -> Ticket:
        """Create new support ticket with automated classification"""
        
        ticket_id = f"TK-{datetime.now().strftime('%Y%m%d')}-{len(self.tickets) + 1:05d}"
        
        # Classify ticket
        category = await self.classify_ticket(title, description)
        priority = await self.calculate_priority(title, description, customer_id, category)
        sentiment_score = await self.analyze_sentiment(title + " " + description)
        urgency_score = await self.calculate_urgency(title, description, customer_id)
        
        # Calculate SLA targets
        now = datetime.now()
        first_response_target = now + timedelta(hours=self.sla_targets[priority]["first_response_hours"])
        resolution_target = now + timedelta(hours=self.sla_targets[priority]["resolution_hours"])
        
        ticket = Ticket(
            ticket_id=ticket_id,
            customer_id=customer_id,
            title=title,
            description=description,
            category=category,
            priority=priority,
            status=TicketStatus.NEW,
            channel=channel,
            created_at=now,
            updated_at=now,
            assigned_agent_id=None,
            tags=await self.extract_tags(title, description),
            sentiment_score=sentiment_score,
            urgency_score=urgency_score,
            resolution_target=resolution_target,
            first_response_target=first_response_target,
            first_response_time=None,
            resolution_time=None,
            satisfaction_rating=None,
            metadata=metadata or {},
            conversation_history=[],
            escalation_history=[],
            automation_flags=[]
        )
        
        self.tickets[ticket_id] = ticket
        
        # Process through automation rules
        await self.process_automation_rules(ticket)
        
        return ticket
    
    async def classify_ticket(self, title: str, description: str) -> TicketCategory:
        """Automatically classify ticket based on content"""
        
        content = (title + " " + description).lower()
        category_scores = {}
        
        # Score each category based on pattern matches
        for category, patterns in self.classification_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, content, re.IGNORECASE))
                score += matches
            category_scores[category] = score
        
        # Return category with highest score, or general inquiry if no matches
        if category_scores and max(category_scores.values()) > 0:
            return max(category_scores, key=category_scores.get)
        else:
            return TicketCategory.GENERAL_INQUIRY
    
    async def calculate_priority(self, title: str, description: str, 
                               customer_id: str, category: TicketCategory) -> TicketPriority:
        """Calculate ticket priority based on multiple factors"""
        
        content = (title + " " + description).lower()
        priority_score = 0
        
        # Urgency indicators
        urgent_keywords = ["urgent", "emergency", "critical", "asap", "immediately", "can't work"]
        priority_score += sum(2 for keyword in urgent_keywords if keyword in content)
        
        # Category-based scoring
        category_priorities = {
            TicketCategory.EMERGENCY: 4,
            TicketCategory.COMPLAINT: 3,
            TicketCategory.REFUND_REQUEST: 2,
            TicketCategory.ACCOUNT_ACCESS: 2,
            TicketCategory.BILLING_INQUIRY: 1,
            TicketCategory.TECHNICAL_SUPPORT: 1,
            TicketCategory.PROGRAM_QUESTION: 0,
            TicketCategory.SCHEDULING: 0
        }
        priority_score += category_priorities.get(category, 0)
        
        # Customer tier influence (would integrate with customer data)
        # High-tier customers get priority boost
        priority_score += 1  # Simplified - would check actual customer tier
        
        # Map score to priority level
        if priority_score >= 6:
            return TicketPriority.CRITICAL
        elif priority_score >= 4:
            return TicketPriority.URGENT
        elif priority_score >= 2:
            return TicketPriority.HIGH
        elif priority_score >= 1:
            return TicketPriority.NORMAL
        else:
            return TicketPriority.LOW
    
    async def analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment of ticket content (-1 to 1)"""
        
        text_lower = text.lower()
        
        # Negative sentiment indicators
        negative_words = ["angry", "frustrated", "terrible", "awful", "hate", "horrible", "worst", "furious", "unacceptable"]
        negative_score = sum(1 for word in negative_words if word in text_lower)
        
        # Positive sentiment indicators  
        positive_words = ["great", "excellent", "amazing", "wonderful", "fantastic", "love", "perfect", "pleased"]
        positive_score = sum(1 for word in positive_words if word in text_lower)
        
        # Calculate sentiment (-1 to 1)
        if negative_score > 0 or positive_score > 0:
            sentiment = (positive_score - negative_score) / max(1, positive_score + negative_score)
        else:
            sentiment = 0.0  # Neutral
        
        return max(-1.0, min(1.0, sentiment))
    
    async def calculate_urgency(self, title: str, description: str, customer_id: str) -> float:
        """Calculate urgency score (0-1) based on various factors"""
        
        content = (title + " " + description).lower()
        urgency_score = 0.0
        
        # Time-sensitive keywords
        urgent_indicators = ["urgent", "asap", "immediately", "emergency", "critical", "can't work", "blocking"]
        urgency_score += min(0.5, len([word for word in urgent_indicators if word in content]) * 0.1)
        
        # Business impact keywords
        impact_indicators = ["all users", "entire team", "can't access", "system down", "not working"]
        urgency_score += min(0.3, len([phrase for phrase in impact_indicators if phrase in content]) * 0.1)
        
        # Customer history factor (simplified)
        urgency_score += 0.2  # Would calculate based on customer's escalation history
        
        return min(1.0, urgency_score)
    
    async def extract_tags(self, title: str, description: str) -> List[str]:
        """Extract relevant tags from ticket content"""
        
        content = (title + " " + description).lower()
        tags = []
        
        # Technology tags
        tech_tags = ["website", "mobile", "app", "browser", "login", "password", "email"]
        tags.extend([tag for tag in tech_tags if tag in content])
        
        # Process tags
        process_tags = ["onboarding", "billing", "scheduling", "refund", "cancellation"]
        tags.extend([tag for tag in process_tags if tag in content])
        
        # Urgency tags
        if any(word in content for word in ["urgent", "emergency", "critical"]):
            tags.append("urgent")
        
        # Sentiment tags
        if any(word in content for word in ["angry", "frustrated", "unhappy"]):
            tags.append("negative_sentiment")
        
        return list(set(tags))  # Remove duplicates
    
    async def process_automation_rules(self, ticket: Ticket):
        """Process ticket through automation rules"""
        
        # Sort rules by priority
        sorted_rules = sorted(self.automation_rules.values(), key=lambda r: r.priority)
        
        for rule in sorted_rules:
            if not rule.is_active:
                continue
                
            if await self.evaluate_rule_conditions(ticket, rule):
                await self.execute_rule_actions(ticket, rule)
                
                # Update rule statistics
                rule.last_triggered = datetime.now()
                rule.trigger_count += 1
                
                # Add automation flag to ticket
                ticket.automation_flags.append(f"rule_{rule.rule_id}")
    
    async def evaluate_rule_conditions(self, ticket: Ticket, rule: AutomationRule) -> bool:
        """Evaluate if ticket matches rule conditions"""
        
        conditions = rule.conditions
        
        # Check category condition
        if "category" in conditions:
            if ticket.category not in conditions["category"]:
                return False
        
        # Check priority condition
        if "priority" in conditions:
            if ticket.priority not in conditions["priority"]:
                return False
        
        # Check status condition
        if "status" in conditions:
            if ticket.status not in conditions["status"]:
                return False
        
        # Check keyword condition
        if "keywords" in conditions:
            content = (ticket.title + " " + ticket.description).lower()
            if not any(keyword in content for keyword in conditions["keywords"]):
                return False
        
        # Check time-based conditions
        if "hours_since_update" in conditions:
            hours_since = (datetime.now() - ticket.updated_at).total_seconds() / 3600
            if hours_since < conditions["hours_since_update"]:
                return False
        
        if "hours_since_resolution" in conditions:
            if not ticket.resolution_time:
                return False
            hours_since = (datetime.now() - ticket.resolution_time).total_seconds() / 3600
            if hours_since < conditions["hours_since_resolution"]:
                return False
        
        return True
    
    async def execute_rule_actions(self, ticket: Ticket, rule: AutomationRule):
        """Execute actions defined in automation rule"""
        
        for action in rule.actions:
            action_type = action["type"]
            
            if action_type == "assign_agent":
                await self.auto_assign_agent(ticket, action.get("skill_required"))
            
            elif action_type == "auto_response":
                await self.send_auto_response(ticket, action.get("template"))
            
            elif action_type == "escalate":
                await self.escalate_ticket(ticket, action.get("target_skill"))
            
            elif action_type == "close_ticket":
                await self.close_ticket(ticket)
            
            elif action_type == "send_reminder":
                await self.send_reminder(ticket, action.get("template"))
            
            elif action_type == "send_satisfaction_survey":
                await self.send_satisfaction_survey(ticket)
            
            elif action_type == "notify_manager":
                await self.notify_manager(ticket)
    
    async def auto_assign_agent(self, ticket: Ticket, required_skill: Optional[AgentSkill] = None):
        """Automatically assign ticket to most suitable agent"""
        
        if ticket.assigned_agent_id:
            return  # Already assigned
        
        suitable_agents = []
        
        for agent in self.agents.values():
            # Check if agent is available
            if not agent.is_available:
                continue
            
            # Check if agent has capacity
            if agent.current_ticket_count >= agent.max_concurrent_tickets:
                continue
            
            # Check if agent has required skill
            if required_skill and required_skill not in agent.skills:
                continue
            
            # Check availability hours (simplified)
            current_hour = datetime.now().hour
            # Would check against agent's availability schedule
            
            suitable_agents.append(agent)
        
        if suitable_agents:
            # Select best agent based on workload and performance
            best_agent = min(suitable_agents, key=lambda a: a.current_ticket_count)
            
            ticket.assigned_agent_id = best_agent.agent_id
            ticket.status = TicketStatus.OPEN
            best_agent.current_ticket_count += 1
            
            # Log assignment
            ticket.conversation_history.append({
                "timestamp": datetime.now(),
                "type": "assignment",
                "content": f"Automatically assigned to {best_agent.name}",
                "agent_id": "SYSTEM"
            })
    
    async def send_auto_response(self, ticket: Ticket, template: str):
        """Send automated response to customer"""
        
        # Get knowledge base article
        relevant_article = await self.find_relevant_knowledge(ticket)
        
        responses = {
            "billing_inquiry_response": f"Thank you for your billing inquiry. We've received your request and our billing team will respond within 8 hours. In the meantime, you can view your billing history in your account portal.",
            "technical_support_response": f"We've received your technical support request. Our technical team will investigate and respond within 4 hours. Please try clearing your browser cache and cookies as a first troubleshooting step."
        }
        
        response_content = responses.get(template, "Thank you for contacting us. We've received your request and will respond shortly.")
        
        # Add knowledge base content if relevant
        if relevant_article and relevant_article.effectiveness_score > 0.7:
            response_content += f"\n\nYou might find this helpful: {relevant_article.title}\n{relevant_article.content}"
            relevant_article.usage_count += 1
        
        # Log response
        ticket.conversation_history.append({
            "timestamp": datetime.now(),
            "type": "auto_response",
            "content": response_content,
            "agent_id": "SYSTEM"
        })
        
        # Set first response time if not set
        if not ticket.first_response_time:
            ticket.first_response_time = datetime.now()
        
        ticket.status = TicketStatus.PENDING_CUSTOMER
    
    async def find_relevant_knowledge(self, ticket: Ticket) -> Optional[KnowledgeArticle]:
        """Find most relevant knowledge base article"""
        
        ticket_content = (ticket.title + " " + ticket.description).lower()
        best_match = None
        best_score = 0
        
        for article in self.knowledge_base.values():
            if article.category == ticket.category:
                # Calculate relevance score based on keyword matches
                keyword_matches = sum(1 for keyword in article.keywords if keyword in ticket_content)
                if keyword_matches > best_score:
                    best_score = keyword_matches
                    best_match = article
        
        return best_match if best_score >= 2 else None
    
    async def escalate_ticket(self, ticket: Ticket, target_skill: Optional[AgentSkill] = None):
        """Escalate ticket to higher level agent"""
        
        # Find suitable escalation target
        escalation_agents = [
            agent for agent in self.agents.values()
            if agent.is_available and 
            (not target_skill or target_skill in agent.skills) and
            AgentSkill.MANAGEMENT in agent.skills
        ]
        
        if escalation_agents:
            # Remove from current agent if assigned
            if ticket.assigned_agent_id:
                current_agent = self.agents.get(ticket.assigned_agent_id)
                if current_agent:
                    current_agent.current_ticket_count -= 1
            
            # Assign to escalation agent
            escalation_agent = escalation_agents[0]  # Simplified selection
            ticket.assigned_agent_id = escalation_agent.agent_id
            escalation_agent.current_ticket_count += 1
            
            # Increase priority
            if ticket.priority.value < TicketPriority.CRITICAL.value:
                ticket.priority = TicketPriority(ticket.priority.value + 1)
            
            # Log escalation
            ticket.escalation_history.append({
                "timestamp": datetime.now(),
                "reason": "Automated escalation rule triggered",
                "from_agent": ticket.assigned_agent_id,
                "to_agent": escalation_agent.agent_id,
                "escalation_level": len(ticket.escalation_history) + 1
            })
    
    async def close_ticket(self, ticket: Ticket):
        """Close resolved ticket"""
        
        if ticket.status == TicketStatus.RESOLVED:
            ticket.status = TicketStatus.CLOSED
            ticket.updated_at = datetime.now()
            
            # Free up agent capacity
            if ticket.assigned_agent_id:
                agent = self.agents.get(ticket.assigned_agent_id)
                if agent:
                    agent.current_ticket_count = max(0, agent.current_ticket_count - 1)
    
    async def send_reminder(self, ticket: Ticket, template: str):
        """Send reminder to customer"""
        
        reminders = {
            "customer_followup": "We're following up on your support request. Please let us know if you need any additional assistance or if your issue has been resolved."
        }
        
        reminder_content = reminders.get(template, "Following up on your support request.")
        
        ticket.conversation_history.append({
            "timestamp": datetime.now(),
            "type": "reminder",
            "content": reminder_content,
            "agent_id": "SYSTEM"
        })
    
    async def send_satisfaction_survey(self, ticket: Ticket):
        """Send satisfaction survey to customer"""
        
        survey_content = "How was your support experience? Please rate us from 1-5 stars and provide any feedback."
        
        ticket.conversation_history.append({
            "timestamp": datetime.now(),
            "type": "survey",
            "content": survey_content,
            "agent_id": "SYSTEM"
        })
    
    async def notify_manager(self, ticket: Ticket):
        """Notify manager about high-priority ticket"""
        
        managers = [agent for agent in self.agents.values() if AgentSkill.MANAGEMENT in agent.skills]
        
        if managers:
            notification = f"High-priority ticket {ticket.ticket_id} requires attention: {ticket.title}"
            # Would send actual notification to manager
            print(f"Manager notification: {notification}")
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Calculate system performance metrics"""
        
        if not self.tickets:
            return {"message": "No tickets to analyze"}
        
        tickets = list(self.tickets.values())
        
        # Response time metrics
        first_response_times = [
            (ticket.first_response_time - ticket.created_at).total_seconds() / 3600
            for ticket in tickets
            if ticket.first_response_time
        ]
        
        # Resolution time metrics
        resolution_times = [
            (ticket.resolution_time - ticket.created_at).total_seconds() / 3600
            for ticket in tickets
            if ticket.resolution_time
        ]
        
        # SLA compliance
        sla_breaches = 0
        for ticket in tickets:
            if ticket.first_response_time and ticket.first_response_time > ticket.first_response_target:
                sla_breaches += 1
            if ticket.resolution_time and ticket.resolution_time > ticket.resolution_target:
                sla_breaches += 1
        
        # Satisfaction metrics
        satisfaction_scores = [
            ticket.satisfaction_rating
            for ticket in tickets
            if ticket.satisfaction_rating
        ]
        
        return {
            "total_tickets": len(tickets),
            "avg_first_response_hours": sum(first_response_times) / len(first_response_times) if first_response_times else 0,
            "avg_resolution_hours": sum(resolution_times) / len(resolution_times) if resolution_times else 0,
            "sla_compliance_rate": (len(tickets) * 2 - sla_breaches) / (len(tickets) * 2) if tickets else 1.0,
            "avg_satisfaction": sum(satisfaction_scores) / len(satisfaction_scores) if satisfaction_scores else 0,
            "ticket_distribution": {
                category.value: len([t for t in tickets if t.category == category])
                for category in TicketCategory
            },
            "priority_distribution": {
                priority.value: len([t for t in tickets if t.priority == priority])
                for priority in TicketPriority
            },
            "automation_effectiveness": len([t for t in tickets if t.automation_flags]) / len(tickets) if tickets else 0
        }
    
    async def run_maintenance_tasks(self):
        """Run periodic maintenance tasks"""
        
        current_time = datetime.now()
        
        # Process automation rules for existing tickets
        for ticket in self.tickets.values():
            if ticket.status not in [TicketStatus.CLOSED, TicketStatus.CANCELED]:
                await self.process_automation_rules(ticket)
        
        # Check for SLA breaches
        for ticket in self.tickets.values():
            if ticket.status in [TicketStatus.NEW, TicketStatus.OPEN, TicketStatus.IN_PROGRESS]:
                if not ticket.first_response_time and current_time > ticket.first_response_target:
                    # SLA breach - escalate
                    await self.escalate_ticket(ticket)
        
        # Update agent availability
        for agent in self.agents.values():
            # Would check actual agent schedules and status
            agent.is_available = True  # Simplified
    
    async def generate_ticket_summary(self, ticket_id: str) -> Dict[str, Any]:
        """Generate comprehensive ticket summary"""
        
        ticket = self.tickets.get(ticket_id)
        if not ticket:
            return {"error": "Ticket not found"}
        
        assigned_agent = self.agents.get(ticket.assigned_agent_id) if ticket.assigned_agent_id else None
        
        return {
            "ticket_id": ticket.ticket_id,
            "customer_id": ticket.customer_id,
            "title": ticket.title,
            "category": ticket.category.value,
            "priority": ticket.priority.value,
            "status": ticket.status.value,
            "created_at": ticket.created_at.isoformat(),
            "assigned_agent": assigned_agent.name if assigned_agent else None,
            "first_response_time_hours": (
                (ticket.first_response_time - ticket.created_at).total_seconds() / 3600
                if ticket.first_response_time else None
            ),
            "resolution_time_hours": (
                (ticket.resolution_time - ticket.created_at).total_seconds() / 3600
                if ticket.resolution_time else None
            ),
            "sla_status": {
                "first_response_met": (
                    ticket.first_response_time <= ticket.first_response_target
                    if ticket.first_response_time else False
                ),
                "resolution_met": (
                    ticket.resolution_time <= ticket.resolution_target
                    if ticket.resolution_time else None
                )
            },
            "sentiment_score": ticket.sentiment_score,
            "urgency_score": ticket.urgency_score,
            "tags": ticket.tags,
            "automation_flags": ticket.automation_flags,
            "escalation_count": len(ticket.escalation_history),
            "conversation_count": len(ticket.conversation_history)
        }

# Example usage and testing
async def main():
    """Example usage of the Support Automation System"""
    
    # Initialize the system
    support_system = SupportAutomationSystem()
    
    print("=== Support Automation System Demo ===\n")
    
    # Create test tickets
    test_tickets = [
        {
            "customer_id": "CUST001",
            "title": "Can't log into my account - urgent!",
            "description": "I've been trying to log in for hours but keep getting error messages. This is blocking my work.",
            "channel": "email"
        },
        {
            "customer_id": "CUST002", 
            "title": "Question about my coaching program",
            "description": "I'd like to understand what's included in my coaching package and how to access the materials.",
            "channel": "chat"
        },
        {
            "customer_id": "CUST003",
            "title": "Billing issue - wrong amount charged",
            "description": "I was charged $299 but my program should only be $199. Please help resolve this billing error.",
            "channel": "phone"
        },
        {
            "customer_id": "CUST004",
            "title": "This service is terrible!",
            "description": "I'm extremely disappointed with the coaching program. It's not what was promised and I want a full refund immediately.",
            "channel": "email"
        }
    ]
    
    created_tickets = []
    for ticket_data in test_tickets:
        ticket = await support_system.create_ticket(**ticket_data)
        created_tickets.append(ticket)
        print(f"Created ticket {ticket.ticket_id}:")
        print(f"  Category: {ticket.category.value}")
        print(f"  Priority: {ticket.priority.value}")
        print(f"  Assigned to: {support_system.agents[ticket.assigned_agent_id].name if ticket.assigned_agent_id else 'Unassigned'}")
        print(f"  Status: {ticket.status.value}")
        print(f"  Automation flags: {ticket.automation_flags}")
        print("-" * 50)
    
    # Run maintenance to process automation rules
    await support_system.run_maintenance_tasks()
    
    # Show performance metrics
    print("\n=== Performance Metrics ===")
    metrics = await support_system.get_performance_metrics()
    for key, value in metrics.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")
    
    # Show detailed ticket summary
    print(f"\n=== Sample Ticket Summary ===")
    if created_tickets:
        summary = await support_system.generate_ticket_summary(created_tickets[0].ticket_id)
        for key, value in summary.items():
            if isinstance(value, dict):
                print(f"{key}:")
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            else:
                print(f"{key}: {value}")

if __name__ == "__main__":
    asyncio.run(main())