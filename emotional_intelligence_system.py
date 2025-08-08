"""
Emotional Intelligence System for Christopher's Coaching Business
Focus: Sentiment analysis, empathetic responses, emotional intelligence frameworks
"""

import asyncio
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
import math

class EmotionalState(Enum):
    VERY_NEGATIVE = -2
    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1
    VERY_POSITIVE = 2

class EmotionCategory(Enum):
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    TRUST = "trust"
    ANTICIPATION = "anticipation"
    FRUSTRATION = "frustration"
    EXCITEMENT = "excitement"
    ANXIETY = "anxiety"
    CONFIDENCE = "confidence"

class CommunicationStyle(Enum):
    EMPATHETIC = "empathetic"
    SUPPORTIVE = "supportive"
    ENCOURAGING = "encouraging"
    PROFESSIONAL = "professional"
    SOLUTION_FOCUSED = "solution_focused"
    CELEBRATORY = "celebratory"
    REASSURING = "reassuring"
    MOTIVATIONAL = "motivational"

class ConflictLevel(Enum):
    NONE = 0
    LOW = 1
    MODERATE = 2
    HIGH = 3
    CRITICAL = 4

class CulturalContext(Enum):
    WESTERN_DIRECT = "western_direct"
    ASIAN_INDIRECT = "asian_indirect"
    LATIN_EXPRESSIVE = "latin_expressive"
    NORTHERN_RESERVED = "northern_reserved"
    UNIVERSAL = "universal"

@dataclass
class EmotionalProfile:
    customer_id: str
    dominant_emotions: List[EmotionCategory]
    emotional_volatility: float  # 0-1, how much emotions fluctuate
    sensitivity_level: float     # 0-1, how sensitive to communication style
    preferred_communication_style: CommunicationStyle
    cultural_context: CulturalContext
    emotional_triggers: List[str]
    positive_motivators: List[str]
    stress_indicators: List[str]
    recovery_patterns: Dict[str, float]
    last_updated: datetime

@dataclass
class SentimentAnalysis:
    text: str
    overall_sentiment: EmotionalState
    confidence_score: float
    emotion_scores: Dict[EmotionCategory, float]
    key_phrases: List[str]
    intensity_level: float      # 0-1
    subjectivity_level: float   # 0-1, objective vs subjective
    detected_intent: str
    emotional_triggers: List[str]
    timestamp: datetime

@dataclass
class EmpatheticResponse:
    original_message: str
    emotional_context: SentimentAnalysis
    response_strategy: CommunicationStyle
    empathetic_acknowledgment: str
    supportive_content: str
    solution_component: str
    follow_up_questions: List[str]
    tone_adjustments: Dict[str, str]
    cultural_adaptations: Dict[str, str]
    predicted_effectiveness: float

@dataclass
class ConflictAssessment:
    interaction_id: str
    customer_id: str
    conflict_level: ConflictLevel
    escalation_indicators: List[str]
    root_cause_analysis: Dict[str, float]
    de_escalation_strategies: List[str]
    resolution_approaches: List[str]
    success_probability: float
    estimated_resolution_time: int  # minutes
    follow_up_requirements: List[str]

class EmotionalIntelligenceSystem:
    """
    Comprehensive emotional intelligence system featuring:
    - Advanced sentiment analysis and emotion detection
    - Empathetic response generation
    - Conflict detection and de-escalation
    - Cultural sensitivity adaptation
    - Emotional journey mapping
    """
    
    def __init__(self):
        self.emotional_profiles: Dict[str, EmotionalProfile] = {}
        self.sentiment_history: Dict[str, List[SentimentAnalysis]] = {}
        self.response_templates: Dict[CommunicationStyle, Dict[EmotionCategory, List[str]]] = {}
        self.conflict_assessments: Dict[str, ConflictAssessment] = {}
        
        self.setup_emotion_detection()
        self.setup_response_templates()
        self.setup_cultural_adaptations()
        self.setup_de_escalation_strategies()
    
    def setup_emotion_detection(self):
        """Setup emotion detection patterns and scoring"""
        
        self.emotion_patterns = {
            EmotionCategory.JOY: {
                "keywords": ["happy", "excited", "thrilled", "delighted", "pleased", "satisfied", "wonderful", "amazing", "fantastic", "great", "excellent", "love", "enjoy"],
                "intensifiers": ["really", "very", "extremely", "absolutely", "totally", "completely"],
                "phrases": ["couldn't be happier", "over the moon", "on cloud nine", "feeling great"]
            },
            EmotionCategory.SADNESS: {
                "keywords": ["sad", "disappointed", "upset", "down", "depressed", "unhappy", "miserable", "heartbroken", "devastated", "discouraged"],
                "intensifiers": ["very", "really", "extremely", "deeply", "completely"],
                "phrases": ["feeling down", "really disappointed", "quite upset"]
            },
            EmotionCategory.ANGER: {
                "keywords": ["angry", "furious", "mad", "irritated", "annoyed", "frustrated", "outraged", "livid", "pissed", "hate"],
                "intensifiers": ["really", "very", "extremely", "absolutely", "completely"],
                "phrases": ["fed up", "had enough", "can't stand", "absolutely furious"]
            },
            EmotionCategory.FEAR: {
                "keywords": ["scared", "afraid", "worried", "nervous", "anxious", "concerned", "terrified", "frightened", "panic"],
                "intensifiers": ["really", "very", "extremely", "quite", "deeply"],
                "phrases": ["really worried", "quite concerned", "scared about"]
            },
            EmotionCategory.FRUSTRATION: {
                "keywords": ["frustrated", "stuck", "blocked", "confused", "overwhelmed", "stressed", "struggling"],
                "intensifiers": ["really", "very", "extremely", "quite", "deeply"],
                "phrases": ["can't figure out", "don't understand", "not working", "having trouble"]
            },
            EmotionCategory.EXCITEMENT: {
                "keywords": ["excited", "eager", "enthusiastic", "pumped", "thrilled", "energized", "motivated", "inspired"],
                "intensifiers": ["really", "very", "extremely", "super", "totally"],
                "phrases": ["can't wait", "looking forward", "really excited about"]
            },
            EmotionCategory.ANXIETY: {
                "keywords": ["anxious", "nervous", "worried", "concerned", "stressed", "tense", "uneasy", "apprehensive"],
                "intensifiers": ["really", "very", "quite", "extremely", "deeply"],
                "phrases": ["feeling anxious", "bit nervous", "really worried"]
            },
            EmotionCategory.CONFIDENCE: {
                "keywords": ["confident", "sure", "certain", "determined", "ready", "prepared", "capable", "strong"],
                "intensifiers": ["very", "really", "quite", "extremely", "absolutely"],
                "phrases": ["feel confident", "ready to", "sure about"]
            }
        }
        
        self.sentiment_keywords = {
            EmotionalState.VERY_POSITIVE: ["amazing", "fantastic", "incredible", "outstanding", "exceptional", "phenomenal", "brilliant", "perfect"],
            EmotionalState.POSITIVE: ["good", "great", "nice", "pleased", "satisfied", "happy", "enjoy", "like", "appreciate"],
            EmotionalState.NEUTRAL: ["okay", "fine", "normal", "average", "standard", "typical", "regular"],
            EmotionalState.NEGATIVE: ["bad", "poor", "disappointing", "unsatisfied", "unhappy", "dislike", "problem", "issue"],
            EmotionalState.VERY_NEGATIVE: ["terrible", "awful", "horrible", "disgusting", "outrageous", "unacceptable", "worst", "hate"]
        }
        
        self.intensity_modifiers = {
            "very": 1.5, "really": 1.4, "extremely": 2.0, "absolutely": 1.8, "completely": 1.7,
            "quite": 1.3, "pretty": 1.2, "rather": 1.2, "somewhat": 0.8, "slightly": 0.6,
            "a bit": 0.7, "a little": 0.6, "kind of": 0.7, "sort of": 0.6
        }
    
    def setup_response_templates(self):
        """Setup empathetic response templates for different emotional states"""
        
        self.response_templates = {
            CommunicationStyle.EMPATHETIC: {
                EmotionCategory.JOY: [
                    "I'm so happy to hear that! Your excitement is contagious.",
                    "That's wonderful news! I can feel your enthusiasm, and it's fantastic.",
                    "I'm thrilled for you! It sounds like things are going really well."
                ],
                EmotionCategory.SADNESS: [
                    "I can hear that this is really difficult for you, and I want you to know that's completely understandable.",
                    "I'm sorry you're going through this tough time. Your feelings are valid, and it's okay to feel this way.",
                    "This sounds really challenging, and I appreciate you sharing how you're feeling with me."
                ],
                EmotionCategory.ANGER: [
                    "I can understand why you'd be frustrated about this. That sounds really difficult to deal with.",
                    "I hear how upset you are, and I want you to know that your concerns are completely valid.",
                    "This situation would be frustrating for anyone. Let's work together to find a solution."
                ],
                EmotionCategory.FRUSTRATION: [
                    "I can sense your frustration, and I completely understand why you'd feel this way.",
                    "This sounds really challenging, and I appreciate your patience as we work through it.",
                    "I hear that this is causing you stress. Let's break this down together and find a path forward."
                ],
                EmotionCategory.ANXIETY: [
                    "I can understand why this would make you feel anxious. Those feelings are completely normal.",
                    "It sounds like you're feeling overwhelmed, and that's totally understandable given the situation.",
                    "I hear your concern, and I want to help ease some of that worry."
                ]
            },
            CommunicationStyle.SUPPORTIVE: {
                EmotionCategory.JOY: [
                    "That's fantastic! I'm here to support you in maintaining this positive momentum.",
                    "Excellent progress! Let's build on this success together.",
                    "I'm so proud of your achievement! You've earned this moment of celebration."
                ],
                EmotionCategory.SADNESS: [
                    "I'm here to support you through this difficult time. You don't have to face this alone.",
                    "This is tough, but I believe in your strength to work through it. I'm here to help.",
                    "Your feelings matter, and I'm committed to supporting you however you need."
                ],
                EmotionCategory.FRUSTRATION: [
                    "I'm here to help you work through this challenge. We'll tackle it step by step together.",
                    "Let's find a solution that works for you. I'm committed to helping you overcome this obstacle.",
                    "This is frustrating, but we can figure this out together. I'm here to support you."
                ]
            },
            CommunicationStyle.SOLUTION_FOCUSED: {
                EmotionCategory.FRUSTRATION: [
                    "I understand this is challenging. Let's identify the specific issues and create an action plan.",
                    "This sounds frustrating. Let me help you break this down into manageable steps we can address.",
                    "I hear your concern. Here's how we can move forward to resolve this situation."
                ],
                EmotionCategory.ANXIETY: [
                    "I understand your concerns. Let's create a clear plan to address each worry systematically.",
                    "These are valid concerns. Let me outline some concrete steps we can take to improve this situation.",
                    "Let's turn this anxiety into action. Here are some specific things we can do right now."
                ]
            }
        }
        
        self.acknowledgment_templates = {
            EmotionalState.VERY_POSITIVE: [
                "I can feel your excitement and enthusiasm!",
                "Your positive energy is wonderful to experience.",
                "It's clear this means a lot to you, and that's beautiful."
            ],
            EmotionalState.POSITIVE: [
                "I'm glad to hear things are going well for you.",
                "It sounds like you're feeling good about this.",
                "I can sense your satisfaction with how things are progressing."
            ],
            EmotionalState.NEUTRAL: [
                "I appreciate you taking the time to share this with me.",
                "Thank you for letting me know how you're feeling.",
                "I understand where you're coming from."
            ],
            EmotionalState.NEGATIVE: [
                "I can hear that this is challenging for you.",
                "I understand this isn't the experience you were hoping for.",
                "I can sense your disappointment, and that's completely valid."
            ],
            EmotionalState.VERY_NEGATIVE: [
                "I can clearly see how upset and frustrated you are about this.",
                "This is obviously causing you significant distress, and I take that seriously.",
                "I understand this situation is extremely difficult for you."
            ]
        }
    
    def setup_cultural_adaptations(self):
        """Setup cultural context adaptations"""
        
        self.cultural_adaptations = {
            CulturalContext.WESTERN_DIRECT: {
                "communication_style": "direct and clear",
                "emotional_expression": "open acknowledgment",
                "solution_approach": "immediate action-oriented",
                "relationship_building": "task-focused with personal touch"
            },
            CulturalContext.ASIAN_INDIRECT: {
                "communication_style": "gentle and respectful",
                "emotional_expression": "subtle acknowledgment",
                "solution_approach": "patient and methodical",
                "relationship_building": "relationship-first approach"
            },
            CulturalContext.LATIN_EXPRESSIVE: {
                "communication_style": "warm and personal",
                "emotional_expression": "full emotional validation",
                "solution_approach": "collaborative and inclusive",
                "relationship_building": "family-oriented and community-focused"
            },
            CulturalContext.NORTHERN_RESERVED: {
                "communication_style": "professional and measured",
                "emotional_expression": "respectful recognition",
                "solution_approach": "systematic and thorough",
                "relationship_building": "trust-building through competence"
            }
        }
    
    def setup_de_escalation_strategies(self):
        """Setup conflict de-escalation strategies"""
        
        self.de_escalation_strategies = {
            ConflictLevel.LOW: [
                "Acknowledge the concern and provide clear information",
                "Offer alternative solutions or perspectives",
                "Schedule follow-up to ensure satisfaction"
            ],
            ConflictLevel.MODERATE: [
                "Provide empathetic acknowledgment of frustration",
                "Take ownership of any service issues",
                "Offer concrete resolution steps with timeline",
                "Escalate to specialist if needed"
            ],
            ConflictLevel.HIGH: [
                "Immediate supervisor involvement",
                "Comprehensive service recovery plan",
                "Personal relationship manager assignment",
                "Compensation or service credits consideration"
            ],
            ConflictLevel.CRITICAL: [
                "Executive leadership involvement",
                "Full service audit and remediation",
                "Dedicated resolution team assignment",
                "Comprehensive make-good package",
                "Long-term relationship recovery plan"
            ]
        }
    
    async def analyze_sentiment(self, text: str, customer_id: Optional[str] = None, 
                               context: Optional[Dict[str, Any]] = None) -> SentimentAnalysis:
        """Perform comprehensive sentiment analysis on text"""
        
        text_lower = text.lower()
        
        # Calculate overall sentiment
        sentiment_score = 0.0
        sentiment_count = 0
        
        # Check sentiment keywords
        for sentiment_level, keywords in self.sentiment_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    sentiment_score += sentiment_level.value
                    sentiment_count += 1
        
        # Apply intensity modifiers
        for modifier, multiplier in self.intensity_modifiers.items():
            if modifier in text_lower:
                sentiment_score *= multiplier
        
        # Normalize sentiment score
        if sentiment_count > 0:
            sentiment_score /= sentiment_count
        
        # Determine overall sentiment state
        if sentiment_score >= 1.5:
            overall_sentiment = EmotionalState.VERY_POSITIVE
        elif sentiment_score >= 0.5:
            overall_sentiment = EmotionalState.POSITIVE
        elif sentiment_score <= -1.5:
            overall_sentiment = EmotionalState.VERY_NEGATIVE
        elif sentiment_score <= -0.5:
            overall_sentiment = EmotionalState.NEGATIVE
        else:
            overall_sentiment = EmotionalState.NEUTRAL
        
        # Analyze specific emotions
        emotion_scores = {}
        for emotion, patterns in self.emotion_patterns.items():
            score = 0.0
            
            # Check keywords
            for keyword in patterns["keywords"]:
                if keyword in text_lower:
                    score += 0.3
            
            # Check phrases  
            for phrase in patterns.get("phrases", []):
                if phrase in text_lower:
                    score += 0.5
            
            # Apply intensifiers
            for intensifier in patterns.get("intensifiers", []):
                if intensifier in text_lower:
                    score *= 1.2
            
            emotion_scores[emotion] = min(1.0, score)
        
        # Extract key phrases
        key_phrases = await self.extract_key_phrases(text)
        
        # Calculate intensity and subjectivity
        intensity_level = min(1.0, abs(sentiment_score) / 2.0)
        subjectivity_level = await self.calculate_subjectivity(text)
        
        # Detect intent
        detected_intent = await self.detect_intent(text)
        
        # Identify emotional triggers
        emotional_triggers = await self.identify_emotional_triggers(text, customer_id)
        
        # Calculate confidence score
        confidence_score = await self.calculate_confidence(text, sentiment_score, emotion_scores)
        
        analysis = SentimentAnalysis(
            text=text,
            overall_sentiment=overall_sentiment,
            confidence_score=confidence_score,
            emotion_scores=emotion_scores,
            key_phrases=key_phrases,
            intensity_level=intensity_level,
            subjectivity_level=subjectivity_level,
            detected_intent=detected_intent,
            emotional_triggers=emotional_triggers,
            timestamp=datetime.now()
        )
        
        # Store in history
        if customer_id:
            if customer_id not in self.sentiment_history:
                self.sentiment_history[customer_id] = []
            self.sentiment_history[customer_id].append(analysis)
        
        return analysis
    
    async def extract_key_phrases(self, text: str) -> List[str]:
        """Extract key emotional phrases from text"""
        
        key_phrase_patterns = [
            r'\b(really|very|extremely) (happy|sad|frustrated|excited|worried|pleased)\b',
            r'\b(can\'t|cannot) (believe|stand|wait|understand)\b',
            r'\b(so|such) (disappointed|excited|frustrated|happy|pleased)\b',
            r'\b(having trouble|struggling with|difficulty with)\b',
            r'\b(absolutely|completely|totally) (love|hate|disappointed|satisfied)\b'
        ]
        
        key_phrases = []
        for pattern in key_phrase_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            key_phrases.extend([' '.join(match) if isinstance(match, tuple) else match for match in matches])
        
        return key_phrases[:5]  # Return top 5 key phrases
    
    async def calculate_subjectivity(self, text: str) -> float:
        """Calculate how subjective vs objective the text is"""
        
        subjective_indicators = [
            "i think", "i feel", "i believe", "in my opinion", "personally",
            "i love", "i hate", "i like", "i dislike", "seems to me"
        ]
        
        objective_indicators = [
            "the fact is", "according to", "data shows", "research indicates",
            "it is clear that", "obviously", "certainly"
        ]
        
        text_lower = text.lower()
        subjective_count = sum(1 for indicator in subjective_indicators if indicator in text_lower)
        objective_count = sum(1 for indicator in objective_indicators if indicator in text_lower)
        
        if subjective_count + objective_count == 0:
            return 0.5  # Neutral subjectivity
        
        return subjective_count / (subjective_count + objective_count)
    
    async def detect_intent(self, text: str) -> str:
        """Detect the primary intent behind the message"""
        
        intent_patterns = {
            "complaint": [r'\b(complain|complaint|dissatisfied|unhappy|problem|issue|wrong)\b'],
            "question": [r'\b(how|what|when|where|why|can you|could you|would you)\b', r'\?'],
            "request": [r'\b(please|can you|could you|would you|i need|i want|help me)\b'],
            "feedback": [r'\b(feedback|suggestion|recommend|improve|better)\b'],
            "compliment": [r'\b(great|excellent|amazing|wonderful|thank you|appreciate)\b'],
            "concern": [r'\b(worried|concerned|anxious|nervous|afraid)\b'],
            "frustration": [r'\b(frustrated|annoyed|irritated|fed up)\b']
        }
        
        text_lower = text.lower()
        intent_scores = {}
        
        for intent, patterns in intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches
            intent_scores[intent] = score
        
        if intent_scores and max(intent_scores.values()) > 0:
            return max(intent_scores, key=intent_scores.get)
        else:
            return "general"
    
    async def identify_emotional_triggers(self, text: str, customer_id: Optional[str]) -> List[str]:
        """Identify potential emotional triggers in the text"""
        
        common_triggers = {
            "time_pressure": [r'\b(urgent|asap|immediately|deadline|late|delay)\b'],
            "cost_concern": [r'\b(expensive|cost|price|money|cheap|affordable)\b'],
            "quality_issue": [r'\b(quality|poor|bad|broken|defective|substandard)\b'],
            "service_failure": [r'\b(service|support|help|assistance|response|waiting)\b'],
            "communication_gap": [r'\b(didn\'t know|not informed|surprised|unexpected)\b'],
            "expectation_mismatch": [r'\b(expected|thought|assumed|supposed|promised)\b']
        }
        
        text_lower = text.lower()
        identified_triggers = []
        
        for trigger, patterns in common_triggers.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    identified_triggers.append(trigger)
                    break
        
        # Check customer-specific triggers if profile exists
        if customer_id and customer_id in self.emotional_profiles:
            profile = self.emotional_profiles[customer_id]
            for trigger in profile.emotional_triggers:
                if trigger.lower() in text_lower:
                    identified_triggers.append(f"personal_trigger_{trigger}")
        
        return list(set(identified_triggers))
    
    async def calculate_confidence(self, text: str, sentiment_score: float, 
                                 emotion_scores: Dict[EmotionCategory, float]) -> float:
        """Calculate confidence score for sentiment analysis"""
        
        # Base confidence on text length and clarity
        text_length_factor = min(1.0, len(text.split()) / 20)  # Optimal around 20 words
        
        # Confidence based on emotional clarity
        emotion_clarity = max(emotion_scores.values()) if emotion_scores else 0.0
        
        # Confidence based on sentiment strength
        sentiment_strength = min(1.0, abs(sentiment_score) / 2.0)
        
        # Combined confidence score
        confidence = (text_length_factor * 0.3 + emotion_clarity * 0.4 + sentiment_strength * 0.3)
        
        return round(confidence, 3)
    
    async def generate_empathetic_response(self, customer_message: str, customer_id: str,
                                         context: Optional[Dict[str, Any]] = None) -> EmpatheticResponse:
        """Generate empathetic response based on sentiment analysis"""
        
        # Analyze sentiment
        sentiment = await self.analyze_sentiment(customer_message, customer_id, context)
        
        # Get or create customer emotional profile
        profile = await self.get_emotional_profile(customer_id)
        
        # Determine response strategy
        response_strategy = await self.select_response_strategy(sentiment, profile)
        
        # Generate acknowledgment
        acknowledgment = await self.generate_acknowledgment(sentiment, profile)
        
        # Generate supportive content
        supportive_content = await self.generate_supportive_content(sentiment, response_strategy, profile)
        
        # Generate solution component
        solution_component = await self.generate_solution_component(sentiment, context)
        
        # Generate follow-up questions
        follow_up_questions = await self.generate_follow_up_questions(sentiment, profile)
        
        # Apply tone adjustments
        tone_adjustments = await self.apply_tone_adjustments(response_strategy, profile)
        
        # Apply cultural adaptations
        cultural_adaptations = await self.apply_cultural_adaptations(profile)
        
        # Predict effectiveness
        predicted_effectiveness = await self.predict_response_effectiveness(
            sentiment, response_strategy, profile
        )
        
        response = EmpatheticResponse(
            original_message=customer_message,
            emotional_context=sentiment,
            response_strategy=response_strategy,
            empathetic_acknowledgment=acknowledgment,
            supportive_content=supportive_content,
            solution_component=solution_component,
            follow_up_questions=follow_up_questions,
            tone_adjustments=tone_adjustments,
            cultural_adaptations=cultural_adaptations,
            predicted_effectiveness=predicted_effectiveness
        )
        
        return response
    
    async def get_emotional_profile(self, customer_id: str) -> EmotionalProfile:
        """Get or create emotional profile for customer"""
        
        if customer_id in self.emotional_profiles:
            return self.emotional_profiles[customer_id]
        
        # Create default profile
        profile = EmotionalProfile(
            customer_id=customer_id,
            dominant_emotions=[EmotionCategory.CONFIDENCE, EmotionCategory.TRUST],
            emotional_volatility=0.3,
            sensitivity_level=0.5,
            preferred_communication_style=CommunicationStyle.EMPATHETIC,
            cultural_context=CulturalContext.UNIVERSAL,
            emotional_triggers=["time_pressure", "quality_issue"],
            positive_motivators=["achievement", "recognition", "progress"],
            stress_indicators=["short_responses", "multiple_exclamation_marks", "ALL_CAPS"],
            recovery_patterns={"acknowledgment": 0.8, "solution_focus": 0.7, "personal_attention": 0.9},
            last_updated=datetime.now()
        )
        
        self.emotional_profiles[customer_id] = profile
        return profile
    
    async def select_response_strategy(self, sentiment: SentimentAnalysis, 
                                     profile: EmotionalProfile) -> CommunicationStyle:
        """Select appropriate response strategy based on sentiment and profile"""
        
        # High-intensity negative emotions need empathetic approach
        if sentiment.overall_sentiment in [EmotionalState.VERY_NEGATIVE, EmotionalState.NEGATIVE] and sentiment.intensity_level > 0.7:
            return CommunicationStyle.EMPATHETIC
        
        # Anxiety and fear need reassurance
        if EmotionCategory.ANXIETY in sentiment.emotion_scores and sentiment.emotion_scores[EmotionCategory.ANXIETY] > 0.6:
            return CommunicationStyle.REASSURING
        
        # Joy and excitement can be celebrated
        if sentiment.overall_sentiment == EmotionalState.VERY_POSITIVE:
            return CommunicationStyle.CELEBRATORY
        
        # Frustration needs solution focus
        if EmotionCategory.FRUSTRATION in sentiment.emotion_scores and sentiment.emotion_scores[EmotionCategory.FRUSTRATION] > 0.5:
            return CommunicationStyle.SOLUTION_FOCUSED
        
        # Default to customer's preferred style
        return profile.preferred_communication_style
    
    async def generate_acknowledgment(self, sentiment: SentimentAnalysis, 
                                    profile: EmotionalProfile) -> str:
        """Generate appropriate emotional acknowledgment"""
        
        templates = self.acknowledgment_templates.get(sentiment.overall_sentiment, [])
        
        if templates:
            base_acknowledgment = templates[0]  # Use first template for simplicity
        else:
            base_acknowledgment = "I understand what you're sharing with me."
        
        # Add emotional specificity
        dominant_emotion = max(sentiment.emotion_scores, key=sentiment.emotion_scores.get) if sentiment.emotion_scores else None
        
        if dominant_emotion and sentiment.emotion_scores[dominant_emotion] > 0.6:
            emotion_specific = {
                EmotionCategory.FRUSTRATION: "I can sense your frustration with this situation.",
                EmotionCategory.EXCITEMENT: "I can feel your enthusiasm and excitement!",
                EmotionCategory.ANXIETY: "I understand this is causing you some worry.",
                EmotionCategory.JOY: "I'm so happy to hear about your positive experience!"
            }.get(dominant_emotion, base_acknowledgment)
            
            return emotion_specific
        
        return base_acknowledgment
    
    async def generate_supportive_content(self, sentiment: SentimentAnalysis, 
                                        strategy: CommunicationStyle,
                                        profile: EmotionalProfile) -> str:
        """Generate supportive content based on strategy"""
        
        if strategy == CommunicationStyle.EMPATHETIC:
            if sentiment.overall_sentiment in [EmotionalState.NEGATIVE, EmotionalState.VERY_NEGATIVE]:
                return "Your feelings are completely valid, and it's important that you expressed them. I want to help make this right for you."
            else:
                return "I appreciate you sharing your thoughts with me. Your experience matters to us."
        
        elif strategy == CommunicationStyle.REASSURING:
            return "I want to assure you that we're here to support you through this. You're not alone in dealing with this situation."
        
        elif strategy == CommunicationStyle.CELEBRATORY:
            return "This is wonderful news! Your success and happiness mean so much to us. You should be proud of this achievement."
        
        elif strategy == CommunicationStyle.SOLUTION_FOCUSED:
            return "I understand this is challenging, and I'm committed to finding a solution that works for you. Let's work together to resolve this."
        
        elif strategy == CommunicationStyle.MOTIVATIONAL:
            return "I believe in your ability to overcome this challenge. You've shown great strength, and I'm here to support your continued progress."
        
        else:  # SUPPORTIVE
            return "I'm here to support you in whatever way I can. Your success and satisfaction are important to me."
    
    async def generate_solution_component(self, sentiment: SentimentAnalysis, 
                                        context: Optional[Dict[str, Any]]) -> str:
        """Generate solution-focused component of response"""
        
        if sentiment.detected_intent == "complaint":
            return "Let me look into this issue immediately and provide you with a clear resolution plan within the next few hours."
        
        elif sentiment.detected_intent == "question":
            return "I'll make sure to give you a comprehensive answer and any additional resources that might be helpful."
        
        elif sentiment.detected_intent == "request":
            return "I'll take care of this request for you right away and keep you updated on the progress."
        
        elif sentiment.detected_intent == "concern":
            return "Let me address your concerns directly and provide you with the information you need to feel confident moving forward."
        
        else:
            return "I'm here to help with whatever you need. Please let me know how I can best support you."
    
    async def generate_follow_up_questions(self, sentiment: SentimentAnalysis,
                                         profile: EmotionalProfile) -> List[str]:
        """Generate appropriate follow-up questions"""
        
        questions = []
        
        if sentiment.overall_sentiment in [EmotionalState.NEGATIVE, EmotionalState.VERY_NEGATIVE]:
            questions.extend([
                "What would be the most helpful way for me to assist you right now?",
                "Is there anything specific you'd like me to prioritize in resolving this?"
            ])
        
        if EmotionCategory.FRUSTRATION in sentiment.emotion_scores:
            questions.append("What part of this situation is causing you the most difficulty?")
        
        if EmotionCategory.ANXIETY in sentiment.emotion_scores:
            questions.append("What information would help you feel more confident about moving forward?")
        
        if sentiment.overall_sentiment == EmotionalState.POSITIVE:
            questions.append("Is there anything else I can help you with to build on this positive experience?")
        
        # Limit to 3 most relevant questions
        return questions[:3]
    
    async def apply_tone_adjustments(self, strategy: CommunicationStyle,
                                   profile: EmotionalProfile) -> Dict[str, str]:
        """Apply tone adjustments based on strategy and profile"""
        
        adjustments = {
            "formality_level": "balanced",
            "emotional_intensity": "moderate",
            "directness": "clear_but_gentle",
            "personal_touch": "personalized"
        }
        
        if strategy == CommunicationStyle.EMPATHETIC:
            adjustments.update({
                "emotional_intensity": "high",
                "personal_touch": "very_personalized",
                "directness": "gentle_and_understanding"
            })
        
        elif strategy == CommunicationStyle.PROFESSIONAL:
            adjustments.update({
                "formality_level": "formal",
                "emotional_intensity": "low",
                "directness": "clear_and_direct"
            })
        
        elif strategy == CommunicationStyle.CELEBRATORY:
            adjustments.update({
                "emotional_intensity": "high_positive",
                "personal_touch": "celebratory",
                "directness": "enthusiastic"
            })
        
        return adjustments
    
    async def apply_cultural_adaptations(self, profile: EmotionalProfile) -> Dict[str, str]:
        """Apply cultural context adaptations"""
        
        if profile.cultural_context == CulturalContext.UNIVERSAL:
            return {"adaptation": "none_required"}
        
        return self.cultural_adaptations.get(profile.cultural_context, {})
    
    async def predict_response_effectiveness(self, sentiment: SentimentAnalysis,
                                           strategy: CommunicationStyle,
                                           profile: EmotionalProfile) -> float:
        """Predict how effective the response will be"""
        
        effectiveness_score = 0.7  # Base effectiveness
        
        # Strategy alignment with sentiment
        if sentiment.overall_sentiment in [EmotionalState.NEGATIVE, EmotionalState.VERY_NEGATIVE]:
            if strategy == CommunicationStyle.EMPATHETIC:
                effectiveness_score += 0.2
        
        if EmotionCategory.FRUSTRATION in sentiment.emotion_scores:
            if strategy == CommunicationStyle.SOLUTION_FOCUSED:
                effectiveness_score += 0.15
        
        # Customer profile alignment
        if strategy == profile.preferred_communication_style:
            effectiveness_score += 0.1
        
        # Emotional sensitivity adjustment
        if profile.sensitivity_level > 0.7 and strategy == CommunicationStyle.EMPATHETIC:
            effectiveness_score += 0.1
        
        # Confidence in sentiment analysis
        effectiveness_score *= sentiment.confidence_score
        
        return min(1.0, effectiveness_score)
    
    async def assess_conflict_level(self, customer_message: str, customer_id: str,
                                  interaction_history: List[str] = None) -> ConflictAssessment:
        """Assess conflict level and recommend de-escalation strategies"""
        
        sentiment = await self.analyze_sentiment(customer_message, customer_id)
        
        # Calculate conflict indicators
        conflict_indicators = []
        conflict_score = 0.0
        
        # Sentiment-based indicators
        if sentiment.overall_sentiment == EmotionalState.VERY_NEGATIVE:
            conflict_score += 2.0
            conflict_indicators.append("Very negative sentiment")
        elif sentiment.overall_sentiment == EmotionalState.NEGATIVE:
            conflict_score += 1.0
            conflict_indicators.append("Negative sentiment")
        
        # Emotion-based indicators
        if EmotionCategory.ANGER in sentiment.emotion_scores and sentiment.emotion_scores[EmotionCategory.ANGER] > 0.6:
            conflict_score += 1.5
            conflict_indicators.append("High anger levels")
        
        if EmotionCategory.FRUSTRATION in sentiment.emotion_scores and sentiment.emotion_scores[EmotionCategory.FRUSTRATION] > 0.7:
            conflict_score += 1.0
            conflict_indicators.append("High frustration levels")
        
        # Language escalation indicators
        escalation_keywords = ["unacceptable", "demand", "immediately", "supervisor", "cancel", "refund", "lawsuit", "complaint"]
        escalation_count = sum(1 for keyword in escalation_keywords if keyword in customer_message.lower())
        if escalation_count > 0:
            conflict_score += escalation_count * 0.5
            conflict_indicators.append(f"Escalation language used ({escalation_count} instances)")
        
        # Determine conflict level
        if conflict_score >= 3.0:
            conflict_level = ConflictLevel.CRITICAL
        elif conflict_score >= 2.0:
            conflict_level = ConflictLevel.HIGH
        elif conflict_score >= 1.0:
            conflict_level = ConflictLevel.MODERATE
        elif conflict_score > 0:
            conflict_level = ConflictLevel.LOW
        else:
            conflict_level = ConflictLevel.NONE
        
        # Root cause analysis
        root_causes = await self.analyze_root_causes(customer_message, sentiment)
        
        # Select de-escalation strategies
        strategies = self.de_escalation_strategies.get(conflict_level, [])
        
        # Generate resolution approaches
        resolution_approaches = await self.generate_resolution_approaches(conflict_level, root_causes)
        
        # Calculate success probability
        success_probability = await self.calculate_resolution_probability(conflict_level, sentiment, customer_id)
        
        # Estimate resolution time
        resolution_time = {
            ConflictLevel.NONE: 5,
            ConflictLevel.LOW: 15,
            ConflictLevel.MODERATE: 30,
            ConflictLevel.HIGH: 60,
            ConflictLevel.CRITICAL: 120
        }.get(conflict_level, 30)
        
        assessment = ConflictAssessment(
            interaction_id=f"INT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{customer_id}",
            customer_id=customer_id,
            conflict_level=conflict_level,
            escalation_indicators=conflict_indicators,
            root_cause_analysis=root_causes,
            de_escalation_strategies=strategies,
            resolution_approaches=resolution_approaches,
            success_probability=success_probability,
            estimated_resolution_time=resolution_time,
            follow_up_requirements=await self.generate_follow_up_requirements(conflict_level)
        )
        
        self.conflict_assessments[assessment.interaction_id] = assessment
        return assessment
    
    async def analyze_root_causes(self, message: str, sentiment: SentimentAnalysis) -> Dict[str, float]:
        """Analyze potential root causes of conflict"""
        
        root_cause_patterns = {
            "service_quality": [r'\b(poor|bad|terrible|awful|quality|service)\b', 0.3],
            "communication_failure": [r'\b(not informed|didn\'t know|surprised|no response|ignored)\b', 0.3],
            "expectation_mismatch": [r'\b(expected|promised|told|thought|supposed to)\b', 0.25],
            "time_delays": [r'\b(late|delay|waiting|slow|behind schedule)\b', 0.25],
            "billing_issues": [r'\b(charge|bill|payment|money|refund|cost)\b', 0.2],
            "technical_problems": [r'\b(broken|not working|error|bug|technical|system)\b', 0.2]
        }
        
        message_lower = message.lower()
        root_causes = {}
        
        for cause, (pattern, base_weight) in root_cause_patterns.items():
            matches = len(re.findall(pattern, message_lower))
            if matches > 0:
                # Weight by sentiment intensity and match count
                weight = base_weight * matches * (sentiment.intensity_level + 0.5)
                root_causes[cause] = min(1.0, weight)
        
        return root_causes
    
    async def generate_resolution_approaches(self, conflict_level: ConflictLevel, 
                                           root_causes: Dict[str, float]) -> List[str]:
        """Generate specific resolution approaches based on conflict level and causes"""
        
        approaches = []
        
        # Add general approaches based on conflict level
        if conflict_level == ConflictLevel.CRITICAL:
            approaches.extend([
                "Immediate executive intervention",
                "Comprehensive service audit",
                "Dedicated resolution team",
                "Full compensation package"
            ])
        
        # Add specific approaches based on root causes
        top_causes = sorted(root_causes.items(), key=lambda x: x[1], reverse=True)[:2]
        
        for cause, weight in top_causes:
            if cause == "service_quality":
                approaches.append("Service quality improvement plan with specific milestones")
            elif cause == "communication_failure":
                approaches.append("Enhanced communication protocol with regular updates")
            elif cause == "expectation_mismatch":
                approaches.append("Clear expectation reset with documented agreements")
            elif cause == "time_delays":
                approaches.append("Priority processing with accelerated timeline")
            elif cause == "billing_issues":
                approaches.append("Billing audit and correction with compensation")
            elif cause == "technical_problems":
                approaches.append("Technical resolution with system improvements")
        
        return approaches[:5]  # Return top 5 approaches
    
    async def calculate_resolution_probability(self, conflict_level: ConflictLevel,
                                             sentiment: SentimentAnalysis, 
                                             customer_id: str) -> float:
        """Calculate probability of successful resolution"""
        
        base_probability = {
            ConflictLevel.NONE: 0.95,
            ConflictLevel.LOW: 0.85,
            ConflictLevel.MODERATE: 0.70,
            ConflictLevel.HIGH: 0.50,
            ConflictLevel.CRITICAL: 0.30
        }.get(conflict_level, 0.50)
        
        # Adjust based on customer history
        if customer_id in self.sentiment_history:
            history = self.sentiment_history[customer_id]
            recent_sentiment_avg = statistics.mean([s.overall_sentiment.value for s in history[-5:]])
            
            # Positive history increases probability
            if recent_sentiment_avg > 0:
                base_probability += 0.1
            # Negative history decreases probability
            elif recent_sentiment_avg < -0.5:
                base_probability -= 0.1
        
        # Adjust based on sentiment confidence
        base_probability *= sentiment.confidence_score
        
        return max(0.1, min(0.95, base_probability))
    
    async def generate_follow_up_requirements(self, conflict_level: ConflictLevel) -> List[str]:
        """Generate follow-up requirements based on conflict level"""
        
        requirements = {
            ConflictLevel.NONE: ["Standard satisfaction check within 48 hours"],
            ConflictLevel.LOW: [
                "Follow-up within 24 hours",
                "Satisfaction confirmation within 48 hours"
            ],
            ConflictLevel.MODERATE: [
                "Progress update within 12 hours",
                "Resolution confirmation within 24 hours",
                "Satisfaction survey within 48 hours"
            ],
            ConflictLevel.HIGH: [
                "Immediate supervisor follow-up",
                "Progress updates every 6 hours",
                "Personal relationship manager assignment",
                "30-day relationship recovery check"
            ],
            ConflictLevel.CRITICAL: [
                "Executive team notification",
                "Hourly progress updates until resolved",
                "Dedicated relationship manager",
                "60-day relationship recovery program",
                "Monthly executive check-ins for 6 months"
            ]
        }
        
        return requirements.get(conflict_level, requirements[ConflictLevel.MODERATE])
    
    async def update_emotional_profile(self, customer_id: str, interaction_data: Dict[str, Any]):
        """Update customer emotional profile based on interaction data"""
        
        profile = await self.get_emotional_profile(customer_id)
        
        # Update based on sentiment history
        if customer_id in self.sentiment_history:
            recent_sentiments = self.sentiment_history[customer_id][-10:]  # Last 10 interactions
            
            # Calculate emotional volatility
            sentiment_values = [s.overall_sentiment.value for s in recent_sentiments]
            if len(sentiment_values) > 1:
                profile.emotional_volatility = statistics.stdev(sentiment_values) / 2.0
            
            # Update dominant emotions
            emotion_counts = {}
            for sentiment in recent_sentiments:
                for emotion, score in sentiment.emotion_scores.items():
                    if score > 0.5:
                        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + score
            
            if emotion_counts:
                top_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:3]
                profile.dominant_emotions = [emotion for emotion, count in top_emotions]
        
        # Update triggers based on recent conflicts
        recent_triggers = []
        for assessment in self.conflict_assessments.values():
            if assessment.customer_id == customer_id:
                recent_triggers.extend(assessment.escalation_indicators)
        
        if recent_triggers:
            profile.emotional_triggers = list(set(profile.emotional_triggers + recent_triggers))[:5]
        
        profile.last_updated = datetime.now()

# Example usage and testing
async def main():
    """Example usage of the Emotional Intelligence System"""
    
    # Initialize the system
    ei_system = EmotionalIntelligenceSystem()
    
    print("=== Emotional Intelligence System Demo ===\n")
    
    # Test messages with different emotional states
    test_messages = [
        {
            "customer_id": "CUST001",
            "message": "I'm absolutely thrilled with my coaching progress! This program has exceeded all my expectations and I can't wait for our next session.",
            "expected_sentiment": "Very Positive"
        },
        {
            "customer_id": "CUST002",
            "message": "I'm really frustrated with this situation. I've been waiting for weeks and nothing has been resolved. This is completely unacceptable!",
            "expected_sentiment": "Very Negative"
        },
        {
            "customer_id": "CUST003",
            "message": "I'm a bit worried about whether I'm making enough progress in the program. Am I on the right track?",
            "expected_sentiment": "Neutral/Anxious"
        },
        {
            "customer_id": "CUST004",
            "message": "The coaching session was okay, nothing special. I guess it's helping somewhat.",
            "expected_sentiment": "Neutral"
        },
        {
            "customer_id": "CUST005",
            "message": "I'm extremely disappointed with the service. This is the worst experience I've ever had and I demand an immediate refund!",
            "expected_sentiment": "Very Negative/Angry"
        }
    ]
    
    # Process each test message
    for test_case in test_messages:
        customer_id = test_case["customer_id"]
        message = test_case["message"]
        
        print(f"Customer {customer_id}:")
        print(f"Message: {message}")
        print(f"Expected: {test_case['expected_sentiment']}")
        
        # Analyze sentiment
        sentiment = await ei_system.analyze_sentiment(message, customer_id)
        print(f"Detected Sentiment: {sentiment.overall_sentiment.name}")
        print(f"Confidence: {sentiment.confidence_score:.2f}")
        print(f"Intensity: {sentiment.intensity_level:.2f}")
        
        # Show top emotions
        if sentiment.emotion_scores:
            top_emotions = sorted(sentiment.emotion_scores.items(), key=lambda x: x[1], reverse=True)[:2]
            print(f"Top Emotions: {[(e.name, f'{s:.2f}') for e, s in top_emotions]}")
        
        # Generate empathetic response
        empathetic_response = await ei_system.generate_empathetic_response(message, customer_id)
        print(f"Response Strategy: {empathetic_response.response_strategy.name}")
        print(f"Acknowledgment: {empathetic_response.empathetic_acknowledgment}")
        print(f"Predicted Effectiveness: {empathetic_response.predicted_effectiveness:.2f}")
        
        # Assess conflict level
        conflict_assessment = await ei_system.assess_conflict_level(message, customer_id)
        print(f"Conflict Level: {conflict_assessment.conflict_level.name}")
        if conflict_assessment.escalation_indicators:
            print(f"Escalation Indicators: {conflict_assessment.escalation_indicators}")
        
        print("-" * 80)
    
    # Show system insights
    print("\n=== System Insights ===")
    print(f"Total customers analyzed: {len(ei_system.sentiment_history)}")
    print(f"Total emotional profiles: {len(ei_system.emotional_profiles)}")
    print(f"Total conflict assessments: {len(ei_system.conflict_assessments)}")
    
    # Show conflict distribution
    conflict_levels = [assessment.conflict_level for assessment in ei_system.conflict_assessments.values()]
    if conflict_levels:
        from collections import Counter
        conflict_distribution = Counter(level.name for level in conflict_levels)
        print(f"Conflict Distribution: {dict(conflict_distribution)}")

if __name__ == "__main__":
    asyncio.run(main())