"""
Production-Ready Multilingual Service
Uses Google Cloud Translation & TTS for legal, scalable multilingual support
"""

import os
import logging
from typing import Dict, Optional
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
from google.oauth2 import service_account
from functools import lru_cache

logger = logging.getLogger(__name__)

# Language mappings
SUPPORTED_LANGUAGES = {
    'en': {'name': 'English', 'deepgram': 'en', 'google_tts': 'en-US', 'voice': 'en-US-Neural2-J'},
    'hi': {'name': 'Hindi', 'deepgram': 'hi', 'google_tts': 'hi-IN', 'voice': 'hi-IN-Neural2-D'},
    'ta': {'name': 'Tamil', 'deepgram': 'ta', 'google_tts': 'ta-IN', 'voice': 'ta-IN-Standard-B'},
    'ml': {'name': 'Malayalam', 'deepgram': 'ml', 'google_tts': 'ml-IN', 'voice': 'ml-IN-Wavenet-D'},
    'kn': {'name': 'Kannada', 'deepgram': 'kn', 'google_tts': 'kn-IN', 'voice': 'kn-IN-Wavenet-B'},
    'te': {'name': 'Telugu', 'deepgram': 'te', 'google_tts': 'te-IN', 'voice': 'te-IN-Standard-B'}
}

# Language switch keywords
LANGUAGE_KEYWORDS = {
    'hi': ['hindi', 'hindi mein', 'हिंदी', 'hindi me bolo'],
    'ta': ['tamil', 'tamil la', 'தமிழ்', 'tamil paesu'],
    'ml': ['malayalam', 'malayalam il', 'മലയാളം'],
    'kn': ['kannada', 'kannada mein', 'ಕನ್ನಡ'],
    'te': ['telugu', 'telugu lo', 'తెలుగు'],
    'en': ['english', 'speak english']
}


class MultilingualService:
    """
    Production-ready multilingual service using Google Cloud APIs
    """
    
    def __init__(self, credentials_path: str = None):
        """
        Initialize Google Cloud clients
        
        Args:
            credentials_path: Path to Google Cloud service account JSON
        """
        self.credentials = None
        if credentials_path and os.path.exists(credentials_path):
            self.credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )
            logger.info(f"✅ Loaded Google Cloud credentials from {credentials_path}")
        else:
            # Will use GOOGLE_APPLICATION_CREDENTIALS env var
            logger.info("Using default Google Cloud credentials from environment")
        
        # Initialize clients
        self.translate_client = translate.Client(credentials=self.credentials)
        self.tts_client = texttospeech.TextToSpeechClient(credentials=self.credentials)
        
        logger.info("✅ Multilingual service initialized")
    
    def detect_language(self, text: str) -> str:
        """
        Detect language using Google Cloud Translation API
        
        Args:
            text: Text to detect language for
            
        Returns:
            Language code (e.g., 'hi', 'en')
        """
        if not text or len(text.strip()) < 3:
            return 'en'
        
        # Check for explicit language switch keywords first
        text_lower = text.lower()
        for lang_code, keywords in LANGUAGE_KEYWORDS.items():
            if any(keyword in text_lower for keyword in keywords):
                logger.info(f"🔍 Detected language via keyword: {lang_code}")
                return lang_code
        
        try:
            # Use Google Cloud Translation API
            result = self.translate_client.detect_language(text)
            detected_lang = result['language']
            confidence = result['confidence']
            
            # Map to our supported languages
            if detected_lang in SUPPORTED_LANGUAGES:
                logger.info(f"🔍 Detected language: {detected_lang} (confidence: {confidence:.2f})")
                return detected_lang
            else:
                logger.warning(f"⚠️ Unsupported language detected: {detected_lang}, defaulting to English")
                return 'en'
                
        except Exception as e:
            logger.error(f"❌ Language detection failed: {e}")
            return 'en'
    
    def translate_text(self, text: str, target_lang: str, source_lang: str = None) -> str:
        """
        Translate text using Google Cloud Translation API
        
        Args:
            text: Text to translate
            target_lang: Target language code
            source_lang: Source language code (auto-detected if None)
            
        Returns:
            Translated text
        """
        if not text or not text.strip():
            return text
        
        # No translation needed
        if source_lang == target_lang:
            return text
        
        try:
            result = self.translate_client.translate(
                text,
                target_language=target_lang,
                source_language=source_lang
            )
            
            translated = result['translatedText']
            logger.debug(f"✅ Translated: {text[:50]}... → {translated[:50]}...")
            return translated
            
        except Exception as e:
            logger.error(f"❌ Translation failed: {e}")
            return text
    
    @lru_cache(maxsize=1000)
    def translate_cached(self, text: str, target_lang: str, source_lang: str = 'en') -> str:
        """
        Cached translation for frequently used phrases
        """
        return self.translate_text(text, target_lang, source_lang)
    
    def get_tts_config(self, language: str, gender: str = 'FEMALE') -> Dict:
        """
        Get TTS configuration for a language
        
        Args:
            language: Language code
            gender: Voice gender ('MALE', 'FEMALE', 'NEUTRAL')
            
        Returns:
            TTS configuration dict
        """
        if language not in SUPPORTED_LANGUAGES:
            language = 'en'
        
        lang_config = SUPPORTED_LANGUAGES[language]
        
        return {
            'language_code': lang_config['google_tts'],
            'voice_name': lang_config['voice'],
            'ssml_gender': getattr(texttospeech.SsmlVoiceGender, gender)
        }
    
    def synthesize_speech(self, text: str, language: str = 'en') -> bytes:
        """
        Synthesize speech using Google Cloud TTS
        
        Args:
            text: Text to synthesize
            language: Language code
            
        Returns:
            Audio bytes (MP3)
        """
        try:
            tts_config = self.get_tts_config(language)
            
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice = texttospeech.VoiceSelectionParams(
                language_code=tts_config['language_code'],
                name=tts_config['voice_name'],
                ssml_gender=tts_config['ssml_gender']
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=1.0,
                pitch=0.0
            )
            
            response = self.tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            return response.audio_content
            
        except Exception as e:
            logger.error(f"❌ TTS synthesis failed: {e}")
            raise


# Global singleton instance
_multilingual_service = None


def get_multilingual_service(credentials_path: str = None) -> MultilingualService:
    """
    Get or create the global multilingual service instance
    """
    global _multilingual_service
    
    if _multilingual_service is None:
        _multilingual_service = MultilingualService(credentials_path)
    
    return _multilingual_service


# Convenience functions for backward compatibility
async def translate_text_indictrans(text: str, target_lang: str, source_lang: str = 'en') -> str:
    """
    Replace your existing translate_text_indictrans function with this
    """
    service = get_multilingual_service()
    return service.translate_text(text, target_lang, source_lang)


def detect_language_fasttext(text: str) -> str:
    """
    Replace your existing detect_language_fasttext function with this
    """
    service = get_multilingual_service()
    return service.detect_language(text)