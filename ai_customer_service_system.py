"""
AI-Powered Customer Service System for Christopher's Coaching Business
Mission: Achieve 95%+ satisfaction scores and 40%+ retention improvements
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import re

# External library imports (would be installed via pip)
# from transformers import pipeline
# from langchain.llms import OpenAI
# from langchain.chains import ConversationChain
# from langchain.memory import ConversationBufferWindowMemory
# import openai
# import pandas as pd
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class TicketStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PENDING_CUSTOMER = "pending_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"

class Channel(Enum):
    EMAIL = "email"
    CHAT = "chat"
    PHONE = "phone"
    SOCIAL = "social"
    FORM = "form"

class SentimentScore(Enum):
    VERY_NEGATIVE = -2
    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1
    VERY_POSITIVE = 2

@dataclass
class Customer:
    customer_id: str
    name: str
    email: str
    phone: Optional[str]
    coaching_program: Optional[str]
    tier: str  # Bronze, Silver, Gold, Platinum
    join_date: datetime
    last_interaction: Optional[datetime]
    satisfaction_score: float
    health_score: float
    communication_preference: Channel
    timezone: str
    tags: List[str]

@dataclass
class Ticket:
    ticket_id: str
    customer_id: str
    channel: Channel
    subject: str
    content: str
    priority: Priority
    status: TicketStatus
    category: str
    sentiment_score: SentimentScore
    created_at: datetime
    updated_at: datetime
    assigned_agent: Optional[str]
    resolution_time: Optional[int]  # minutes
    satisfaction_rating: Optional[int]
    tags: List[str]

@dataclass
class ChatSession:
    session_id: str
    customer_id: str
    messages: List[Dict[str, Any]]
    bot_responses: List[Dict[str, Any]]
    escalated_to_human: bool
    sentiment_trend: List[SentimentScore]
    satisfaction_score: Optional[int]
    created_at: datetime
    ended_at: Optional[datetime]

class AICustomerServiceSystem:
    """
    Comprehensive AI-powered customer service system with:
    - Intelligent chatbot with NLP
    - Automated ticket routing
    - Sentiment analysis
    - Multi-channel support
    - 24/7 availability with human handoff
    """
    
    def __init__(self):
        self.customers: Dict[str, Customer] = {}
        self.tickets: Dict[str, Ticket] = {}
        self.chat_sessions: Dict[str, ChatSession] = {}
        self.knowledge_base: Dict[str, str] = {}
        self.escalation_rules: List[Dict] = []
        self.business_hours = {"start": 9, "end": 17}  # 9 AM to 5 PM
        
        # AI Components (would use actual AI services in production)
        self.setup_ai_components()
        self.setup_knowledge_base()
        self.setup_escalation_rules()
    
    def setup_ai_components(self):
        """Initialize AI components for NLP and sentiment analysis"""
        # In production, these would be actual AI service connections
        self.sentiment_analyzer = None  # pipeline("sentiment-analysis")
        self.nlp_processor = None  # OpenAI or similar
        self.intent_classifier = None  # Custom trained model
        
        # Simulated AI responses for demo
        self.ai_responses = {
            "greeting": [
                "Hello! I'm here to help you with your coaching journey. How can I assist you today?",
                "Welcome! I'm your AI assistant. What can I help you with?",
                "Hi there! I'm ready to support you. What questions do you have?"
            ],
            "coaching_question": [
                "That's a great coaching question! Let me connect you with some resources or our coaching team.",
                "I understand you have questions about your coaching program. Let me help you find the right information."
            ],
            "technical_issue": [
                "I see you're experiencing a technical issue. Let me help troubleshoot or escalate this to our tech support team.",
                "Technical problems can be frustrating. I'm here to help resolve this quickly."
            ],
            "billing_question": [
                "I'll help you with your billing question. For security, I may need to transfer you to our billing specialist.",
                "Let me assist with your billing inquiry while ensuring your account information stays secure."
            ]
        }
    
    def setup_knowledge_base(self):
        """Initialize knowledge base with common questions and answers"""
        self.knowledge_base = {
            "coaching program duration": "Our coaching programs typically run for 3-12 months depending on your specific goals and chosen package.",
            "session scheduling": "You can schedule sessions through your client portal or by contacting your dedicated coach directly.",
            "payment methods": "We accept all major credit cards, PayPal, and offer payment plans for longer programs.",
            "refund policy": "We offer a 30-day satisfaction guarantee. Please contact support for refund requests.",
            "program materials": "All program materials are available in your client portal within 24 hours of enrollment.",
            "coach availability": "Your dedicated coach will respond to messages within 24 hours during business days.",
            "technical support": "For technical issues, please clear your browser cache or try accessing from a different device.",
            "program benefits": "Our coaching programs include 1-on-1 sessions, group workshops, resource library, and ongoing support."
        }
    
    def setup_escalation_rules(self):
        """Define rules for when to escalate to human agents"""
        self.escalation_rules = [
            {
                "condition": "sentiment_very_negative",
                "action": "immediate_human_escalation",
                "priority": Priority.CRITICAL
            },
            {
                "condition": "billing_dispute",
                "action": "billing_specialist_escalation",
                "priority": Priority.HIGH
            },
            {
                "condition": "coaching_complaint",
                "action": "coaching_manager_escalation",
                "priority": Priority.HIGH
            },
            {
                "condition": "technical_issue_complex",
                "action": "tech_support_escalation",
                "priority": Priority.MEDIUM
            },
            {
                "condition": "multiple_failed_bot_responses",
                "action": "human_escalation",
                "priority": Priority.MEDIUM
            }
        ]
    
    async def process_incoming_message(self, customer_id: str, message: str, channel: Channel) -> Dict[str, Any]:
        """Process incoming customer message with AI analysis"""
        
        # Analyze sentiment
        sentiment = await self.analyze_sentiment(message)
        
        # Classify intent
        intent = await self.classify_intent(message)
        
        # Check for escalation triggers
        should_escalate, escalation_reason = await self.check_escalation_triggers(
            customer_id, message, sentiment, intent, channel
        )
        
        if should_escalate:
            return await self.escalate_to_human(customer_id, message, escalation_reason, channel)
        
        # Generate AI response
        response = await self.generate_ai_response(customer_id, message, intent, sentiment)
        
        # Log interaction
        await self.log_interaction(customer_id, message, response, sentiment, intent, channel)
        
        return {
            "response": response,
            "sentiment": sentiment.value,
            "intent": intent,
            "escalated": False,
            "confidence_score": 0.85  # Simulated confidence
        }
    
    async def analyze_sentiment(self, text: str) -> SentimentScore:
        """Analyze sentiment of customer message"""
        # In production, use actual sentiment analysis
        # result = self.sentiment_analyzer(text)
        
        # Simulated sentiment analysis
        negative_words = ["angry", "frustrated", "terrible", "awful", "hate", "horrible", "worst"]
        positive_words = ["great", "excellent", "amazing", "wonderful", "fantastic", "love", "perfect"]
        
        text_lower = text.lower()
        negative_count = sum(1 for word in negative_words if word in text_lower)
        positive_count = sum(1 for word in positive_words if word in text_lower)
        
        if negative_count > positive_count and negative_count > 0:
            return SentimentScore.NEGATIVE if negative_count == 1 else SentimentScore.VERY_NEGATIVE
        elif positive_count > negative_count and positive_count > 0:
            return SentimentScore.POSITIVE if positive_count == 1 else SentimentScore.VERY_POSITIVE
        else:
            return SentimentScore.NEUTRAL
    
    async def classify_intent(self, text: str) -> str:
        """Classify customer intent from message"""
        # In production, use trained intent classifier
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["schedule", "appointment", "session", "meeting"]):
            return "scheduling"
        elif any(word in text_lower for word in ["bill", "payment", "charge", "invoice", "refund"]):
            return "billing"
        elif any(word in text_lower for word in ["coach", "program", "goal", "progress"]):
            return "coaching_question"
        elif any(word in text_lower for word in ["technical", "login", "access", "broken", "error"]):
            return "technical_issue"
        elif any(word in text_lower for word in ["cancel", "complaint", "unhappy", "dissatisfied"]):
            return "complaint"
        else:
            return "general_inquiry"
    
    async def check_escalation_triggers(self, customer_id: str, message: str, 
                                      sentiment: SentimentScore, intent: str, 
                                      channel: Channel) -> Tuple[bool, Optional[str]]:
        """Check if message should be escalated to human agent"""
        
        # Immediate escalation triggers
        if sentiment == SentimentScore.VERY_NEGATIVE:
            return True, "Very negative sentiment detected"
        
        if intent == "complaint":
            return True, "Customer complaint requires human attention"
        
        if intent == "billing" and "dispute" in message.lower():
            return True, "Billing dispute requires specialist"
        
        # Check customer history for escalation patterns
        customer = self.customers.get(customer_id)
        if customer and customer.satisfaction_score < 3.0:
            return True, "Low customer satisfaction score"
        
        # Business hours check for complex issues
        current_hour = datetime.now().hour
        if not (self.business_hours["start"] <= current_hour <= self.business_hours["end"]):
            if intent in ["coaching_question", "billing"]:
                return True, "Complex issue outside business hours"
        
        return False, None
    
    async def generate_ai_response(self, customer_id: str, message: str, 
                                 intent: str, sentiment: SentimentScore) -> str:
        """Generate appropriate AI response based on intent and context"""
        
        # Get customer context
        customer = self.customers.get(customer_id)
        
        # Knowledge base lookup
        kb_response = await self.search_knowledge_base(message)
        if kb_response:
            return kb_response
        
        # Intent-based responses
        if intent in self.ai_responses:
            base_response = self.ai_responses[intent][0]  # Use first response for simplicity
            
            # Personalize response if customer data available
            if customer:
                base_response = f"Hi {customer.name.split()[0]}, {base_response}"
            
            return base_response
        
        # Default response
        return "Thank you for your message. I'm here to help! Could you please provide more details about what you need assistance with?"
    
    async def search_knowledge_base(self, query: str) -> Optional[str]:
        """Search knowledge base for relevant answers"""
        query_lower = query.lower()
        
        for key, answer in self.knowledge_base.items():
            if any(word in query_lower for word in key.split()):
                return f"Based on your question about {key}: {answer}"
        
        return None
    
    async def escalate_to_human(self, customer_id: str, message: str, 
                              reason: str, channel: Channel) -> Dict[str, Any]:
        """Escalate conversation to human agent"""
        
        # Create high-priority ticket
        ticket = await self.create_ticket(
            customer_id=customer_id,
            channel=channel,
            subject=f"Escalated: {reason}",
            content=message,
            priority=Priority.HIGH,
            category="escalated"
        )
        
        # Notify available agents
        await self.notify_agents(ticket)
        
        return {
            "response": "I'm connecting you with one of our specialist team members who can better assist you. They'll be with you shortly.",
            "escalated": True,
            "ticket_id": ticket.ticket_id,
            "estimated_wait_time": await self.estimate_wait_time()
        }
    
    async def create_ticket(self, customer_id: str, channel: Channel, subject: str,
                          content: str, priority: Priority, category: str) -> Ticket:
        """Create new support ticket"""
        
        ticket_id = f"TK-{datetime.now().strftime('%Y%m%d')}-{len(self.tickets) + 1:04d}"
        
        # Analyze sentiment for ticket content
        sentiment = await self.analyze_sentiment(content)
        
        ticket = Ticket(
            ticket_id=ticket_id,
            customer_id=customer_id,
            channel=channel,
            subject=subject,
            content=content,
            priority=priority,
            status=TicketStatus.OPEN,
            category=category,
            sentiment_score=sentiment,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            assigned_agent=None,
            resolution_time=None,
            satisfaction_rating=None,
            tags=[]
        )
        
        self.tickets[ticket_id] = ticket
        return ticket
    
    async def auto_route_ticket(self, ticket: Ticket) -> Optional[str]:
        """Automatically route ticket to appropriate agent/team"""
        
        routing_rules = {
            "billing": ["billing_specialist_1", "billing_specialist_2"],
            "technical_issue": ["tech_support_1", "tech_support_2"],
            "coaching_question": ["coach_manager", "senior_coach"],
            "complaint": ["customer_success_manager"],
            "escalated": ["team_lead", "customer_success_manager"]
        }
        
        if ticket.category in routing_rules:
            available_agents = routing_rules[ticket.category]
            # In production, check agent availability and workload
            return available_agents[0]  # Simplified assignment
        
        return None
    
    async def notify_agents(self, ticket: Ticket):
        """Notify relevant agents about new ticket"""
        assigned_agent = await self.auto_route_ticket(ticket)
        
        if assigned_agent:
            ticket.assigned_agent = assigned_agent
            # In production, send actual notifications
            logging.info(f"Ticket {ticket.ticket_id} assigned to {assigned_agent}")
    
    async def estimate_wait_time(self) -> str:
        """Estimate wait time for human agent"""
        # Simple estimation based on current queue
        open_tickets = len([t for t in self.tickets.values() if t.status == TicketStatus.OPEN])
        
        if open_tickets == 0:
            return "Less than 5 minutes"
        elif open_tickets <= 3:
            return "5-15 minutes"
        elif open_tickets <= 10:
            return "15-30 minutes"
        else:
            return "30-60 minutes"
    
    async def log_interaction(self, customer_id: str, message: str, response: str,
                            sentiment: SentimentScore, intent: str, channel: Channel):
        """Log customer interaction for analytics"""
        
        interaction_log = {
            "timestamp": datetime.now().isoformat(),
            "customer_id": customer_id,
            "channel": channel.value,
            "message": message,
            "response": response,
            "sentiment": sentiment.value,
            "intent": intent,
            "resolved_by_ai": True
        }
        
        # In production, save to database or analytics platform
        logging.info(f"Interaction logged: {interaction_log}")
    
    async def get_customer_health_score(self, customer_id: str) -> float:
        """Calculate customer health score based on interactions and satisfaction"""
        customer = self.customers.get(customer_id)
        if not customer:
            return 0.0
        
        # Factors for health score calculation
        satisfaction_weight = 0.4
        recency_weight = 0.3
        engagement_weight = 0.3
        
        # Satisfaction component (0-1)
        satisfaction_component = customer.satisfaction_score / 5.0
        
        # Recency component (0-1)
        days_since_interaction = (datetime.now() - (customer.last_interaction or customer.join_date)).days
        recency_component = max(0, 1 - (days_since_interaction / 30))  # Decay over 30 days
        
        # Engagement component (simplified)
        engagement_component = 0.7  # Would calculate based on actual engagement metrics
        
        health_score = (
            satisfaction_component * satisfaction_weight +
            recency_component * recency_weight +
            engagement_component * engagement_weight
        )
        
        return round(health_score, 2)
    
    async def generate_proactive_outreach(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Generate proactive outreach based on customer health and behavior"""
        
        health_score = await self.get_customer_health_score(customer_id)
        customer = self.customers.get(customer_id)
        
        if not customer:
            return None
        
        outreach_recommendations = []
        
        # Low health score intervention
        if health_score < 0.5:
            outreach_recommendations.append({
                "type": "health_intervention",
                "priority": "high",
                "message": f"Hi {customer.name.split()[0]}, I noticed it's been a while since we connected. How is your coaching journey going? I'm here to help if you need anything!",
                "channel": customer.communication_preference
            })
        
        # Milestone celebrations
        days_since_join = (datetime.now() - customer.join_date).days
        if days_since_join in [30, 60, 90, 180, 365]:  # Milestone days
            outreach_recommendations.append({
                "type": "milestone_celebration",
                "priority": "medium",
                "message": f"Congratulations {customer.name.split()[0]}! You've been on your coaching journey for {days_since_join} days. How are you feeling about your progress?",
                "channel": customer.communication_preference
            })
        
        return outreach_recommendations[0] if outreach_recommendations else None

# Multi-channel support integration
class MultiChannelSupport:
    """Handle support across multiple channels"""
    
    def __init__(self, ai_system: AICustomerServiceSystem):
        self.ai_system = ai_system
        self.channel_configs = {
            Channel.EMAIL: {"response_time_sla": 120},  # 2 hours
            Channel.CHAT: {"response_time_sla": 1},     # 1 minute
            Channel.PHONE: {"response_time_sla": 0.05}, # 3 seconds
            Channel.SOCIAL: {"response_time_sla": 60},  # 1 hour
        }
    
    async def handle_email_inquiry(self, from_email: str, subject: str, body: str) -> Dict[str, Any]:
        """Handle incoming email inquiry"""
        # Look up customer by email
        customer_id = await self.find_customer_by_email(from_email)
        
        if not customer_id:
            # Create new customer record
            customer_id = await self.create_customer_from_email(from_email)
        
        return await self.ai_system.process_incoming_message(customer_id, body, Channel.EMAIL)
    
    async def handle_chat_message(self, session_id: str, customer_id: str, message: str) -> Dict[str, Any]:
        """Handle incoming chat message"""
        return await self.ai_system.process_incoming_message(customer_id, message, Channel.CHAT)
    
    async def handle_social_media_mention(self, platform: str, username: str, message: str) -> Dict[str, Any]:
        """Handle social media mention or message"""
        # Look up customer by social media username
        customer_id = await self.find_customer_by_social(platform, username)
        
        if not customer_id:
            customer_id = await self.create_customer_from_social(platform, username)
        
        return await self.ai_system.process_incoming_message(customer_id, message, Channel.SOCIAL)
    
    async def find_customer_by_email(self, email: str) -> Optional[str]:
        """Find customer by email address"""
        for customer_id, customer in self.ai_system.customers.items():
            if customer.email == email:
                return customer_id
        return None
    
    async def find_customer_by_social(self, platform: str, username: str) -> Optional[str]:
        """Find customer by social media username"""
        # Simplified - would integrate with customer database
        return None
    
    async def create_customer_from_email(self, email: str) -> str:
        """Create new customer record from email inquiry"""
        customer_id = f"CUST-{datetime.now().strftime('%Y%m%d')}-{len(self.ai_system.customers) + 1:04d}"
        
        customer = Customer(
            customer_id=customer_id,
            name=email.split('@')[0],  # Simplified name extraction
            email=email,
            phone=None,
            coaching_program=None,
            tier="Bronze",
            join_date=datetime.now(),
            last_interaction=None,
            satisfaction_score=5.0,
            health_score=1.0,
            communication_preference=Channel.EMAIL,
            timezone="UTC",
            tags=["new_customer"]
        )
        
        self.ai_system.customers[customer_id] = customer
        return customer_id
    
    async def create_customer_from_social(self, platform: str, username: str) -> str:
        """Create new customer record from social media interaction"""
        customer_id = f"CUST-{datetime.now().strftime('%Y%m%d')}-{len(self.ai_system.customers) + 1:04d}"
        
        customer = Customer(
            customer_id=customer_id,
            name=username,
            email="",
            phone=None,
            coaching_program=None,
            tier="Bronze",
            join_date=datetime.now(),
            last_interaction=None,
            satisfaction_score=5.0,
            health_score=1.0,
            communication_preference=Channel.SOCIAL,
            timezone="UTC",
            tags=["new_customer", f"{platform}_customer"]
        )
        
        self.ai_system.customers[customer_id] = customer
        return customer_id

# Example usage and testing
async def main():
    """Example usage of the AI Customer Service System"""
    
    # Initialize the system
    ai_system = AICustomerServiceSystem()
    multi_channel = MultiChannelSupport(ai_system)
    
    # Add sample customer
    sample_customer = Customer(
        customer_id="CUST-20250808-0001",
        name="John Smith",
        email="john.smith@example.com",
        phone="+1-555-123-4567",
        coaching_program="Executive Leadership",
        tier="Gold",
        join_date=datetime.now() - timedelta(days=45),
        last_interaction=datetime.now() - timedelta(days=3),
        satisfaction_score=4.2,
        health_score=0.8,
        communication_preference=Channel.EMAIL,
        timezone="EST",
        tags=["engaged", "high_value"]
    )
    
    ai_system.customers[sample_customer.customer_id] = sample_customer
    
    # Test AI response system
    print("=== AI Customer Service System Demo ===\n")
    
    # Test cases
    test_messages = [
        ("How do I schedule my next coaching session?", "scheduling"),
        ("I'm having trouble logging into my account", "technical_issue"),
        ("I want to cancel my subscription, this is terrible!", "complaint"),
        ("What payment methods do you accept?", "billing"),
        ("I love my coaching program, it's amazing!", "general_inquiry")
    ]
    
    for message, expected_intent in test_messages:
        print(f"Customer Message: {message}")
        
        response = await ai_system.process_incoming_message(
            sample_customer.customer_id, 
            message, 
            Channel.CHAT
        )
        
        print(f"AI Response: {response['response']}")
        print(f"Sentiment: {response['sentiment']}")
        print(f"Intent: {response['intent']}")
        print(f"Escalated: {response['escalated']}")
        print("-" * 50)
    
    # Test proactive outreach
    print("\n=== Proactive Outreach Recommendation ===")
    outreach = await ai_system.generate_proactive_outreach(sample_customer.customer_id)
    if outreach:
        print(f"Type: {outreach['type']}")
        print(f"Priority: {outreach['priority']}")
        print(f"Message: {outreach['message']}")
    
    print(f"\nCustomer Health Score: {await ai_system.get_customer_health_score(sample_customer.customer_id)}")

if __name__ == "__main__":
    asyncio.run(main())