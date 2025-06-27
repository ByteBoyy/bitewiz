# import re
# from typing import Set, List
# import string

# class RelevanceFilter:
#     def __init__(self):
#         self.food_keywords = {
#             # Food types
#             'food', 'eat', 'eating', 'meal', 'lunch', 'dinner', 'breakfast', 'brunch', 'snack',
#             'pizza', 'burger', 'sandwich', 'salad', 'soup', 'pasta', 'rice', 'noodles', 'bread',
#             'chicken', 'beef', 'fish', 'seafood', 'vegetarian', 'vegan', 'meat', 'cheese',
            
#             # Cuisines
#             'chinese', 'italian', 'mexican', 'japanese', 'indian', 'thai', 'american', 'french',
#             'korean', 'vietnamese', 'mediterranean', 'greek', 'spanish', 'lebanese', 'turkish',
            
#             # Restaurant related
#             'restaurant', 'cafe', 'diner', 'bistro', 'bar', 'grill', 'kitchen', 'place',
#             'menu', 'order', 'ordering', 'delivery', 'takeout', 'pickup',
            
#             # Dietary preferences
#             'halal', 'kosher', 'gluten', 'dairy', 'allergic', 'allergy', 'spicy', 'mild',
#             'organic', 'fresh', 'healthy', 'diet', 'keto', 'paleo',
            
#             # Actions/intents
#             'hungry', 'craving', 'want', 'need', 'looking', 'find', 'search', 'recommend',
#             'suggest', 'show', 'tell', 'help', 'choose', 'pick', 'decide', 'taste', 'try',
            
#             # Descriptors
#             'delicious', 'tasty', 'yummy', 'good', 'best', 'favorite', 'love', 'like',
#             'hot', 'cold', 'sweet', 'sour', 'bitter', 'salty', 'spicy', 'bland'
#         }
        
#         self.activation_phrases = {
#             'hey bitewise', 'hello bitewise', 'hi bitewise', 'bitewise',
#             'excuse me', 'can you help', 'help me', 'i want to', 'i need to',
#             'i want', 'i need', 'i would like', "i'd like", 'looking for',
#             'find me', 'show me', 'tell me about', 'what about', 'how about',
#             'where can i', 'do you have', 'any suggestions', 'recommend me',
#             'i am hungry', "i'm hungry", 'feeling hungry', 'want to eat',
#             'something to eat', 'place to eat', 'good food', 'best food'
#         }
        
#         # Question words that often indicate genuine queries
#         self.question_words = {
#             'what', 'where', 'when', 'how', 'which', 'who', 'why', 'can', 'could',
#             'would', 'should', 'do', 'does', 'is', 'are', 'will', 'any'
#         }
        
#         # Background conversation indicators (things people say to each other)
#         self.background_indicators = {
#             'he said', 'she said', 'they said', 'we should', 'you should',
#             'remember when', 'last time', 'yesterday', 'tomorrow', 'next week',
#             'my friend', 'my family', 'at work', 'at home', 'at school',
#             'did you see', 'have you heard', 'by the way', 'oh yeah',
#             'anyway', 'so basically', 'you know what', 'speaking of'
#         }
        
#         # Ignore patterns (regex)
#         self.ignore_patterns = [
#             r'^(um|uh|hmm|okay|yeah|yes|no|sure|right|oh|ah|well)+[.,!?]*$',  # Filler words only
#             r'^.{1,2}$',  # Too short (1-2 chars)
#             r'^\w+[.,!?]*$',  # Single word with optional punctuation
#             r'^(hey|hi|hello)[.,!?]*$',  # Just greetings without context
#             r'^\d+[.,!?]*$',  # Just numbers
#             r'^[^\w\s]+$',  # Only punctuation/symbols
#             r'^(test|testing|check)[.,!?]*$',  # Test words
#         ]
        
#         # Conversation enders that suggest background talk
#         self.conversation_enders = {
#             'see you later', 'talk to you later', 'bye', 'goodbye', 'catch you later',
#             'have a good day', 'take care', 'see ya', 'later', 'gotta go'
#         }

#     def clean_text(self, text: str) -> str:
#         """Clean and normalize text for analysis"""
#         # Remove extra whitespace and convert to lowercase
#         text = re.sub(r'\s+', ' ', text.strip().lower())
        
#         # Remove common speech disfluencies
#         text = re.sub(r'\b(uh|um|er|ah)+\b', '', text)
        
#         # Remove excessive punctuation
#         text = re.sub(r'[.!?]{2,}', '.', text)
        
#         return text.strip()

#     def has_question_structure(self, text: str) -> bool:
#         """Check if text has question-like structure"""
#         words = text.split()
#         if not words:
#             return False
            
#         # Starts with question word
#         if words[0] in self.question_words:
#             return True
            
#         # Contains question words
#         if any(word in self.question_words for word in words[:3]):
#             return True
            
#         # Ends with question mark
#         if text.endswith('?'):
#             return True
            
#         return False

#     def has_food_context(self, text: str) -> bool:
#         """Check for food/restaurant context"""
#         words = set(text.split())
#         return bool(words.intersection(self.food_keywords))

#     def has_activation_phrase(self, text: str) -> bool:
#         """Check for strong activation phrases"""
#         return any(phrase in text for phrase in self.activation_phrases)

#     def seems_like_background_conversation(self, text: str) -> bool:
#         """Detect if this seems like background conversation"""
#         # Check for background conversation indicators
#         if any(indicator in text for indicator in self.background_indicators):
#             return True
            
#         # Check for conversation enders
#         if any(ender in text for ender in self.conversation_enders):
#             return True
            
#         # Third person references (talking about someone else)
#         third_person_patterns = [
#             r'\bhe\s+(is|was|will|should|would|can|could)',
#             r'\bshe\s+(is|was|will|should|would|can|could)',
#             r'\bthey\s+(are|were|will|should|would|can|could)',
#             r'\b(his|her|their)\s+\w+',
#             r'\bthem\b',
#             r'\bhim\b',
#         ]
        
#         for pattern in third_person_patterns:
#             if re.search(pattern, text):
#                 return True
                
#         return False

#     def calculate_relevance_score(self, text: str) -> float:
#         """Calculate a relevance score from 0.0 to 1.0"""
#         score = 0.0
#         words = text.split()
#         word_count = len(words)
        
#         # Strong activation phrases get high score
#         if self.has_activation_phrase(text):
#             score += 0.8
            
#         # Food context adds score
#         food_word_count = sum(1 for word in words if word in self.food_keywords)
#         if food_word_count > 0:
#             score += min(0.6, food_word_count * 0.2)
            
#         # Question structure adds score
#         if self.has_question_structure(text):
#             score += 0.3
            
#         # Proper length adds score
#         if 3 <= word_count <= 20:
#             score += 0.2
#         elif word_count > 20:
#             score -= 0.1  # Too long might be background conversation
            
#         # Contains "I" suggests direct communication
#         if ' i ' in f' {text} ' or text.startswith('i '):
#             score += 0.3
            
#         # Background conversation reduces score
#         if self.seems_like_background_conversation(text):
#             score -= 0.7
            
#         return max(0.0, min(1.0, score))

#     def is_relevant(self, text: str, threshold: float = 0.4) -> bool:
#         """
#         Main method to determine if text is relevant.
        
#         Args:
#             text: Input text to analyze
#             threshold: Minimum score needed to be considered relevant (0.0-1.0)
        
#         Returns:
#             bool: True if text seems relevant to food/restaurant assistance
#         """
#         if not text or not text.strip():
#             return False
            
#         # Clean the text
#         cleaned_text = self.clean_text(text)
        
#         if not cleaned_text:
#             return False
            
#         # Check ignore patterns first (quick rejection)
#         for pattern in self.ignore_patterns:
#             if re.match(pattern, cleaned_text):
#                 return False
        
#         # Calculate relevance score
#         score = self.calculate_relevance_score(cleaned_text)
        
#         # Debug logging (remove in production)
#         print(f"Relevance check: '{text}' -> Score: {score:.2f} -> {'ACCEPT' if score >= threshold else 'REJECT'}")
        
#         return score >= threshold

#     def is_relevant_with_context(self, text: str, previous_messages: List[str] = None, threshold: float = 0.4) -> bool:
#         """
#         Enhanced relevance check that considers conversation context.
        
#         Args:
#             text: Current text to analyze
#             previous_messages: List of recent messages for context
#             threshold: Minimum score needed
            
#         Returns:
#             bool: True if relevant considering context
#         """
#         base_relevance = self.is_relevant(text, threshold)
        
#         # If clearly relevant, no need for context
#         if base_relevance and self.calculate_relevance_score(self.clean_text(text)) > 0.7:
#             return True
            
#         # If we have recent food-related context, be more lenient
#         if previous_messages:
#             recent_context = ' '.join(previous_messages[-3:])  # Last 3 messages
#             if self.has_food_context(recent_context):
#                 # Lower threshold if we're in a food conversation
#                 return self.calculate_relevance_score(self.clean_text(text)) >= (threshold - 0.2)
        
#         return base_relevance


# # Example usage and testing
# if __name__ == "__main__":
#     filter = RelevanceFilter()
    
#     # Test cases
#     test_cases = [
#         # Should ACCEPT
#         ("I'm hungry, what restaurants do you recommend?", True),
#         ("hey bitewise, show me some pizza places", True),
#         ("looking for good chinese food", True),
#         ("what's on the menu?", True),
#         ("any vegetarian options?", True),
#         ("i want something spicy", True),
#         ("where can i get a burger?", True),
        
#         # Should REJECT
#         ("hey john, how was your day?", False),
#         ("um", False),
#         ("okay", False),
#         ("he said he's coming later", False),
#         ("did you see the game yesterday?", False),
#         ("talking to my friend about work", False),
#         ("123", False),
#         ("test", False),
#         ("we should meet tomorrow", False),
        
#         # Edge cases
#         ("i think pizza is good", True),  # Food context
#         ("tell me about italian", True),  # Cuisine + question structure
#         ("they have good food there", False),  # Third person, background-ish
#     ]
    
#     print("Testing Relevance Filter:")
#     print("-" * 50)
    
#     for text, expected in test_cases:
#         result = filter.is_relevant(text)
#         status = "✓" if result == expected else "✗"
#         print(f"{status} '{text}' -> {result} (expected {expected})")

import re
from typing import Set, List
import string
import time

class RelevanceFilter:
    def __init__(self, conversation_timeout=30.0):
        # Core food and restaurant keywords
        self.food_keywords = {
            # Food types
            'food', 'eat', 'eating', 'meal', 'lunch', 'dinner', 'breakfast', 'brunch', 'snack',
            'pizza', 'burger', 'sandwich', 'salad', 'soup', 'pasta', 'rice', 'noodles', 'bread',
            'chicken', 'beef', 'fish', 'seafood', 'vegetarian', 'vegan', 'meat', 'cheese',
            
            # Cuisines
            'chinese', 'italian', 'mexican', 'japanese', 'indian', 'thai', 'american', 'french',
            'korean', 'vietnamese', 'mediterranean', 'greek', 'spanish', 'lebanese', 'turkish',
            
            # Restaurant related
            'restaurant', 'cafe', 'diner', 'bistro', 'bar', 'grill', 'kitchen', 'place',
            'menu', 'order', 'ordering', 'delivery', 'takeout', 'pickup',
            
            # Dietary preferences
            'halal', 'kosher', 'gluten', 'dairy', 'allergic', 'allergy', 'spicy', 'mild',
            'organic', 'fresh', 'healthy', 'diet', 'keto', 'paleo',
            
            # Actions/intents
            'hungry', 'craving', 'want', 'need', 'looking', 'find', 'search', 'recommend',
            'suggest', 'show', 'tell', 'help', 'choose', 'pick', 'decide', 'taste', 'try',
            
            # Descriptors
            'delicious', 'tasty', 'yummy', 'good', 'best', 'favorite', 'love', 'like',
            'hot', 'cold', 'sweet', 'sour', 'bitter', 'salty', 'spicy', 'bland'
        }
        
        # Wake words for activation
        self.wake_words = ['bitewise', 'bite wise', 'hey bitewise', 'hi bitewise', 'hello bitewise']
        
        # Strong activation phrases
        self.activation_phrases = {
            'hey bitewise', 'hello bitewise', 'hi bitewise', 'bitewise',
            'excuse me', 'can you help', 'help me', 'i want to', 'i need to',
            'i want', 'i need', 'i would like', "i'd like", 'looking for',
            'find me', 'show me', 'tell me about', 'what about', 'how about',
            'where can i', 'do you have', 'any suggestions', 'recommend me',
            'i am hungry', "i'm hungry", 'feeling hungry', 'want to eat',
            'something to eat', 'place to eat', 'good food', 'best food'
        }
        
        # Simple greetings that should be accepted
        self.simple_greetings = {
            'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
            'hello?', 'hi?', 'hey?', 'anyone there', 'anyone here'
        }
        
        # Question words
        self.question_words = {
            'what', 'where', 'when', 'how', 'which', 'who', 'why', 'can', 'could',
            'would', 'should', 'do', 'does', 'is', 'are', 'will', 'any'
        }
        
        # Person references
        self.person_references = {
            'friend', 'friends', 'buddy', 'colleague', 'coworker', 'family',
            'mom', 'dad', 'brother', 'sister', 'wife', 'husband', 'girlfriend', 'boyfriend'
        }
        
        # Recommendation/suggestion phrases that include others
        self.recommendation_phrases = {
            'recommends', 'recommended', 'suggests', 'suggested', 'told me about',
            'says it\'s good', 'says it\'s great', 'mentioned', 'heard about',
            'friend said', 'family loves', 'everyone says', 'people say'
        }
        
        # Background conversation indicators
        self.background_indicators = {
            'he said', 'she said', 'they said', 'we should', 'you should',
            'remember when', 'last time', 'yesterday', 'tomorrow', 'next week',
            'my friend', 'my family', 'at work', 'at home', 'at school',
            'did you see', 'have you heard', 'by the way', 'oh yeah',
            'anyway', 'so basically', 'you know what', 'speaking of',
            'keeps talking', 'won\'t stop', 'doesn\'t stop', 'very annoying',
            'stop talking', 'be quiet', 'shut up', 'just doesn\'t stop',
            'this is just', 'this just', 'it just', 'never stops',
            'so annoying', 'really annoying', 'getting annoying'
        }
        
        # Conversation enders
        self.conversation_enders = {
            'see you later', 'talk to you later', 'bye', 'goodbye', 'catch you later',
            'have a good day', 'take care', 'see ya', 'later', 'gotta go',
            'thank you', 'thanks', 'that\'s all', 'nevermind', 'cancel', 'stop', 'exit'
        }
        
        # Transliterated food words
        self.transliterated_food = {
            'khana', 'restaurant', 'hotel', 'chinese', 'desi', 'biryani', 
            'karahi', 'kebab', 'roti', 'naan', 'chai', 'lassi', 'tikka',
            'tandoor', 'curry', 'masala', 'dal', 'sabzi'
        }
        
        # Ignore patterns
        self.ignore_patterns = [
            r'^(um|uh|hmm|okay|yeah|yes|no|sure|right|oh|ah|well)+[.,!?]*$',
            r'^.{1,2}$',  # Too short (1-2 chars)
            r'^[^\w\s]+$',  # Only punctuation/symbols
            r'^(test|testing|check)[.,!?]*$',
            r'^(la)+[.,!?]*$',  # Repeated sounds
            r'^(na)+[.,!?]*$',
            r'^(.)\1{4,}',  # Repeated character 5+ times
        ]
        
        # Complaint patterns (regex)
        self.complaint_patterns = [
            r'\b(doesn\'t|does not|won\'t|will not)\s+(stop|shut up|quit)',
            r'\b(keeps?|keep)\s+(talking|going|saying)',
            r'\b(so|very|really|getting)\s+(annoying|irritating)',
            r'\bthis\s+(is\s+)?just\s+(doesn\'t|does not)',
            r'\bjust\s+(doesn\'t|does not)\s+stop',
            r'\bnever\s+stops?',
        ]
        
        # Conversation state
        self.conversation_active = False
        self.conversation_timeout = conversation_timeout
        self.last_relevant_speech_time = time.time()

    def contains_wake_word(self, text: str) -> bool:
        """Check if text contains wake word"""
        text_lower = text.lower().strip()
        return any(wake_word in text_lower for wake_word in self.wake_words)

    def clean_text(self, text: str) -> str:
        """Clean and normalize text for analysis"""
        text = re.sub(r'\s+', ' ', text.strip().lower())
        text = re.sub(r'\b(uh|um|er|ah)+\b', '', text)
        text = re.sub(r'[.!?]{2,}', '.', text)
        return text.strip()

    def has_question_structure(self, text: str) -> bool:
        """Check if text has question-like structure"""
        words = text.split()
        if not words:
            return False
            
        if words[0] in self.question_words:
            return True
        if any(word in self.question_words for word in words[:3]):
            return True
        if text.endswith('?'):
            return True
        return False

    def has_food_context(self, text: str) -> bool:
        """Check for food/restaurant context"""
        words = set(text.split())
        return bool(words.intersection(self.food_keywords))

    def has_activation_phrase(self, text: str) -> bool:
        """Check for strong activation phrases"""
        return any(phrase in text for phrase in self.activation_phrases)

    def is_simple_greeting(self, text: str) -> bool:
        """Check if this is a simple greeting"""
        cleaned = self.clean_text(text)
        return cleaned in self.simple_greetings


    def analyze_context_intent(self, text: str) -> dict:
        """Analyze the intent and context of the message"""
        text_lower = text.lower()
        
        return {
            'has_food_context': self.has_food_context(text),
            'has_person_reference': any(person in text_lower for person in self.person_references),
            'has_recommendation_context': any(phrase in text_lower for phrase in self.recommendation_phrases),
            'is_first_person': (' i ' in f' {text_lower} ' or text_lower.startswith('i ')),
            'is_seeking_help': any(word in text_lower for word in ['help', 'recommend', 'suggest', 'find', 'looking']),
            'is_complaint': self.seems_like_background_conversation(text),
        }

    def seems_like_background_conversation(self, text: str) -> bool:
        """Detect if this seems like background conversation"""
        # Check background indicators
        if any(indicator in text for indicator in self.background_indicators):
            return True
            
        # Check conversation enders
        if any(ender in text for ender in self.conversation_enders):
            return True
        
        # Check complaint patterns
        for pattern in self.complaint_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        # Third person references
        third_person_patterns = [
            r'\bhe\s+(is|was|will|should|would|can|could)',
            r'\bshe\s+(is|was|will|should|would|can|could)',
            r'\bthey\s+(are|were|will|should|would|can|could)',
            r'\b(his|her|their)\s+\w+',
            r'\bthem\b', r'\bhim\b',
        ]
        
        return any(re.search(pattern, text) for pattern in third_person_patterns)

    def calculate_relevance_score(self, text: str, recent_messages: List[str] = None) -> float:
        """Calculate a relevance score from 0.0 to 1.0"""
        score = 0.0
        words = text.split()
        word_count = len(words)
        
        # Get context analysis
        context = self.analyze_context_intent(text)
        
        # Wake word gets highest priority
        if self.contains_wake_word(text):
            score += 0.9
            self.conversation_active = True
            self.last_relevant_speech_time = time.time()
            return max(0.0, min(1.0, score))
            
        # Handle "I + person + food" pattern (first-person recommendations)
        if (context['is_first_person'] and 
            context['has_person_reference'] and 
            context['has_food_context']):
            
            if context['has_recommendation_context']:
                score += 0.8
            else:
                score += 0.6
        
        # ADD THIS: Handle third-person recommendations (the missing case!)
        elif (context['has_person_reference'] and 
            context['has_food_context'] and 
            context['has_recommendation_context']):
            # "My friend also said the Mexican is good"
            # "Someone recommended me Chinese"
            score += 0.7
        
        # Simple greetings
        elif self.is_simple_greeting(text):
            score += 0.7
            
        # Strong activation phrases
        elif self.has_activation_phrase(text):
            score += 0.8
            
        # Pure food context without person reference
        elif context['has_food_context'] and not context['has_person_reference']:
            food_word_count = sum(1 for word in words if word in self.food_keywords)
            score += min(0.7, food_word_count * 0.2)
            
        # Food context WITH person reference - be more careful
        elif context['has_food_context'] and context['has_person_reference']:
            if context['is_first_person'] or context['is_seeking_help']:
                score += 0.6
            else:
                score += 0.4  # INCREASE from 0.3 to 0.4
        
        # Question structure adds score
        if self.has_question_structure(text):
            score += 0.3
            
        # Proper length adds score
        if 3 <= word_count <= 20:
            score += 0.2
        elif word_count > 20:
            score -= 0.1
            
        # Strong penalty for background conversation
        if context['is_complaint']:
            score -= 0.8
            
        return max(0.0, min(1.0, score))

    def should_process_speech(self, text: str, recent_messages: List[str] = None) -> bool:
        """Main decision function - determines if speech should be processed"""
        current_time = time.time()
        
        # Check for gibberish/noise first
        cleaned_text = self.clean_text(text)
        if not cleaned_text:
            return False
            
        for pattern in self.ignore_patterns:
            if re.match(pattern, cleaned_text):
                print(f"[FILTERED] Ignoring noise: '{text}'")
                return False
        
        # Always process wake words
        if self.contains_wake_word(text):
            self.conversation_active = True
            self.last_relevant_speech_time = current_time
            print(f"[WAKE WORD] Activating conversation: '{text}'")
            return True
        
        # Check conversation timeout
        if current_time - self.last_relevant_speech_time > self.conversation_timeout:
            self.conversation_active = False
            print(f"[TIMEOUT] Conversation timed out, going dormant")
            return False
        
        # Calculate relevance
        score = self.calculate_relevance_score(text, recent_messages)
        threshold = 0.3 if self.conversation_active else 0.35
        
        is_relevant = score >= threshold
        
        print(f"Relevance check: '{text}' -> Score: {score:.2f} -> {'ACCEPT' if is_relevant else 'REJECT'}")
        
        if is_relevant:
            self.last_relevant_speech_time = current_time
            return True
        else:
            print(f"[FILTERED] Ignoring irrelevant speech: '{text}'")
            return False

    def clean_wake_word_from_text(self, text: str) -> str:
        """Remove wake words from text before sending to LLM"""
        clean_text = text
        for wake_word in self.wake_words:
            clean_text = re.sub(re.escape(wake_word), "", clean_text, flags=re.IGNORECASE).strip()
        
        # If only wake word was said, return a greeting
        if not clean_text or len(clean_text.split()) < 1:
            return "Hello"
        
        return clean_text

    def end_conversation_check(self, text: str) -> bool:
        """Check if user wants to end the conversation"""
        text_lower = text.lower()
        if any(phrase in text_lower for phrase in self.conversation_enders):
            self.conversation_active = False
            print(f"[END] Conversation ended by user: '{text}'")
            return True
        return False

    def reset_conversation(self):
        """Manually reset conversation state"""
        self.conversation_active = False
        self.last_relevant_speech_time = time.time()
        print("[RESET] Conversation state reset")

    def get_conversation_status(self):
        """Get current conversation status for debugging"""
        current_time = time.time()
        time_since_last = current_time - self.last_relevant_speech_time
        return {
            "active": self.conversation_active,
            "time_since_last_relevant": time_since_last,
            "will_timeout_in": max(0, self.conversation_timeout - time_since_last)
        }

    # For backward compatibility with your existing code
    def is_relevant(self, text: str, threshold: float = 0.35) -> bool:
        """Backward compatibility method"""
        return self.should_process_speech(text)

    def is_relevant_with_context(self, text: str, previous_messages: List[str] = None, threshold: float = 0.35) -> bool:
        """Backward compatibility method with context"""
        return self.should_process_speech(text, previous_messages)


# Example usage and testing
if __name__ == "__main__":
    filter = RelevanceFilter()
    
    test_cases = [
        # Should ACCEPT
        ("Hello?", True),
        ("I'm hungry, what restaurants do you recommend?", True),
        ("hey bitewise, show me some pizza places", True),
        ("I have a friend, she recommends me some chinese", True),
        ("looking for good chinese food", True),
        ("what's on the menu?", True),
        ("any vegetarian options?", True),
        ("Chinese restaurant mein jana hai", True),  # Mixed language
        
        # Should REJECT  
        ("She keeps talking. She keeps talking. It's very annoying.", False),
        ("See, this is just doesn't stop.", False),
        ("hey john, how was your day?", False),
        ("um", False),
        ("he said he's coming later", False),
        ("کیا حال ہے", False),  # Pure Urdu
        ("talking to my friend about work", False),
    ]
    
    print("Testing Enhanced Relevance Filter:")
    print("-" * 60)
    
    for text, expected in test_cases:
        result = filter.should_process_speech(text)
        status = "✓" if result == expected else "✗"
        print(f"{status} Expected: {expected}")
        print()