"""
AI Handler - Cultural Chronicles

This module handles AI-powered language detection and story classification
using pattern-based algorithms with graceful fallback mechanisms.
"""

import re
import logging
from typing import Optional, Dict, List

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import transformers for advanced AI features
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    TRANSFORMERS_AVAILABLE = True
    logger.info("Transformers library available - advanced AI features enabled")
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.info("Transformers library not available - using pattern-based AI")

# Language detection patterns using Unicode ranges
LANGUAGE_PATTERNS = {
    'Hindi': re.compile(r'[\u0900-\u097F]+'),  # Devanagari script
    'Telugu': re.compile(r'[\u0C00-\u0C7F]+'),  # Telugu script
    'Tamil': re.compile(r'[\u0B80-\u0BFF]+'),  # Tamil script
    'Malayalam': re.compile(r'[\u0D00-\u0D7F]+'),  # Malayalam script
    'Kannada': re.compile(r'[\u0C80-\u0CFF]+'),  # Kannada script
    'Gujarati': re.compile(r'[\u0A80-\u0AFF]+'),  # Gujarati script
    'Punjabi': re.compile(r'[\u0A00-\u0A7F]+'),  # Gurmukhi script
    'Bengali': re.compile(r'[\u0980-\u09FF]+'),  # Bengali script
    'Odia': re.compile(r'[\u0B00-\u0B7F]+'),  # Odia script
    'English': re.compile(r'[a-zA-Z]+'),  # Latin script
}

# Story classification keywords
CATEGORY_KEYWORDS = {
    'Folk Tale': ['tale', 'story', 'once upon', 'long ago', 'village', 'forest', 'moral', 'lesson', 'wise', 'clever'],
    'Legend': ['legend', 'hero', 'brave', 'warrior', 'king', 'queen', 'battle', 'victory', 'ancient', 'mythical'],
    'Tradition': ['tradition', 'custom', 'practice', 'ritual', 'ceremony', 'family', 'ancestors', 'generations'],
    'Festival': ['festival', 'celebration', 'feast', 'dance', 'music', 'holiday', 'gathering', 'community', 'joy'],
    'Recipe': ['recipe', 'cook', 'ingredients', 'preparation', 'dish', 'food', 'spices', 'traditional', 'flavor'],
    'Historical Account': ['history', 'historical', 'past', 'events', 'rulers', 'empire', 'war', 'peace', 'monument'],
    'Religious Story': ['god', 'goddess', 'temple', 'prayer', 'devotion', 'faith', 'sacred', 'holy', 'divine', 'worship'],
    'Song': ['song', 'music', 'melody', 'lyrics', 'sing', 'chorus', 'verse', 'rhythm', 'tune', 'folk song']
}

class AdvancedAIHandler:
    """Advanced AI handler using transformers when available"""
    
    def __init__(self):
        """Initialize advanced AI models"""
        self.language_detector = None
        self.classifier = None
        
        if TRANSFORMERS_AVAILABLE:
            try:
                # Initialize language detection model
                self.language_detector = pipeline(
                    "text-classification",
                    model="papluca/xlm-roberta-base-language-detection",
                    device=-1  # Use CPU
                )
                
                # Initialize text classification model
                self.classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli",
                    device=-1  # Use CPU
                )
                
                logger.info("Advanced AI models loaded successfully")
                
            except Exception as e:
                logger.warning(f"Failed to load advanced AI models: {str(e)}")
                self.language_detector = None
                self.classifier = None
    
    def detect_language_advanced(self, text: str) -> str:
        """
        Detect language using advanced transformer model
        
        Args:
            text: Input text to analyze
            
        Returns:
            str: Detected language
        """
        try:
            if self.language_detector and len(text.strip()) > 10:
                result = self.language_detector(text[:500])  # Limit text length
                
                # Map model output to our language names
                detected = result[0]['label'].lower()
                language_mapping = {
                    'hi': 'Hindi',
                    'te': 'Telugu',
                    'ta': 'Tamil',
                    'ml': 'Malayalam',
                    'kn': 'Kannada',
                    'gu': 'Gujarati',
                    'pa': 'Punjabi',
                    'bn': 'Bengali',
                    'or': 'Odia',
                    'en': 'English'
                }
                
                return language_mapping.get(detected, detected.title())
            
        except Exception as e:
            logger.error(f"Advanced language detection failed: {str(e)}")
        
        return None
    
    def classify_story_advanced(self, text: str, title: str) -> str:
        """
        Classify story using advanced transformer model
        
        Args:
            text: Story content
            title: Story title
            
        Returns:
            str: Story category
        """
        try:
            if self.classifier:
                # Combine title and text for classification
                combined_text = f"{title}. {text[:500]}"  # Limit text length
                
                candidate_labels = list(CATEGORY_KEYWORDS.keys())
                
                result = self.classifier(combined_text, candidate_labels)
                return result['labels'][0]  # Return top prediction
                
        except Exception as e:
            logger.error(f"Advanced story classification failed: {str(e)}")
        
        return None

# Initialize advanced AI handler
_advanced_ai = AdvancedAIHandler()

def detect_language(text: str, hint: Optional[str] = None) -> str:
    """
    Detect the language of the input text
    
    Args:
        text: Input text to analyze
        hint: Optional language hint from user
        
    Returns:
        str: Detected language name
    """
    try:
        # If hint is provided and it's in our supported languages, use it
        if hint and hint in LANGUAGE_PATTERNS:
            logger.info(f"Using language hint: {hint}")
            return hint
        
        # Try advanced AI detection first
        if TRANSFORMERS_AVAILABLE and _advanced_ai.language_detector:
            advanced_result = _advanced_ai.detect_language_advanced(text)
            if advanced_result:
                logger.info(f"Advanced AI detected language: {advanced_result}")
                return advanced_result
        
        # Fallback to pattern-based detection
        logger.info("Using pattern-based language detection")
        
        # Clean text for analysis
        clean_text = text.strip()
        
        if not clean_text:
            return "Unknown"
        
        # Score each language based on character matches
        language_scores = {}
        
        for language, pattern in LANGUAGE_PATTERNS.items():
            matches = pattern.findall(clean_text)
            if matches:
                # Calculate score based on total characters matched
                total_chars = sum(len(match) for match in matches)
                language_scores[language] = total_chars
        
        if language_scores:
            # Return language with highest score
            detected_language = max(language_scores, key=language_scores.get)
            logger.info(f"Pattern-based detection result: {detected_language}")
            return detected_language
        
        # If no patterns match, default to English
        logger.info("No language patterns matched, defaulting to English")
        return "English"
        
    except Exception as e:
        logger.error(f"Language detection failed: {str(e)}")
        return "Unknown"

def classify_story(content: str, title: str = "") -> str:
    """
    Classify the story into a cultural category
    
    Args:
        content: Story content
        title: Story title
        
    Returns:
        str: Story category
    """
    try:
        # Try advanced AI classification first
        if TRANSFORMERS_AVAILABLE and _advanced_ai.classifier:
            advanced_result = _advanced_ai.classify_story_advanced(content, title)
            if advanced_result:
                logger.info(f"Advanced AI classified story as: {advanced_result}")
                return advanced_result
        
        # Fallback to keyword-based classification
        logger.info("Using keyword-based story classification")
        
        # Combine title and content for analysis
        combined_text = f"{title} {content}".lower()
        
        # Score each category based on keyword matches
        category_scores = {}
        
        for category, keywords in CATEGORY_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                # Count occurrences of each keyword
                score += combined_text.count(keyword.lower())
            
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            # Return category with highest score
            classified_category = max(category_scores, key=category_scores.get)
            logger.info(f"Keyword-based classification result: {classified_category}")
            return classified_category
        
        # Default classification based on content analysis
        if any(word in combined_text for word in ['cook', 'ingredient', 'recipe', 'dish']):
            return "Recipe"
        elif any(word in combined_text for word in ['festival', 'celebration', 'feast']):
            return "Festival"
        elif any(word in combined_text for word in ['story', 'tale', 'once upon']):
            return "Folk Tale"
        else:
            return "Tradition"
            
    except Exception as e:
        logger.error(f"Story classification failed: {str(e)}")
        return "Unknown"

def get_supported_languages() -> List[str]:
    """
    Get list of supported languages for detection
    
    Returns:
        list: List of supported language names
    """
    return list(LANGUAGE_PATTERNS.keys())

def get_available_categories() -> List[str]:
    """
    Get list of available story categories
    
    Returns:
        list: List of story categories
    """
    return list(CATEGORY_KEYWORDS.keys())

def analyze_text_features(text: str) -> Dict[str, any]:
    """
    Analyze various features of the input text
    
    Args:
        text: Input text to analyze
        
    Returns:
        dict: Dictionary containing text features
    """
    try:
        features = {
            'length': len(text),
            'word_count': len(text.split()),
            'sentence_count': len([s for s in text.split('.') if s.strip()]),
            'detected_language': detect_language(text),
            'has_english': bool(LANGUAGE_PATTERNS['English'].search(text)),
            'script_diversity': len([lang for lang, pattern in LANGUAGE_PATTERNS.items() 
                                   if pattern.search(text)])
        }
        
        return features
        
    except Exception as e:
        logger.error(f"Text feature analysis failed: {str(e)}")
        return {}

def translate_text(text: str, target_language: str = "English") -> Optional[str]:
    """
    Placeholder for text translation functionality
    
    Args:
        text: Text to translate
        target_language: Target language for translation
        
    Returns:
        str or None: Translated text if successful, None otherwise
    """
    # TODO: Implement translation using Google Translate API or similar
    logger.info(f"Translation requested: {text[:50]}... -> {target_language}")
    
    # For now, return None to indicate translation is not available
    return None

# Model health check
def check_ai_health() -> Dict[str, any]:
    """
    Check the health and availability of AI models
    
    Returns:
        dict: Health status of AI components
    """
    health_status = {
        'transformers_available': TRANSFORMERS_AVAILABLE,
        'language_detection': 'pattern-based',
        'story_classification': 'keyword-based',
        'supported_languages': len(get_supported_languages()),
        'supported_categories': len(get_available_categories())
    }
    
    if TRANSFORMERS_AVAILABLE and _advanced_ai.language_detector:
        health_status['language_detection'] = 'transformer-based'
    
    if TRANSFORMERS_AVAILABLE and _advanced_ai.classifier:
        health_status['story_classification'] = 'transformer-based'
    
    return health_status
