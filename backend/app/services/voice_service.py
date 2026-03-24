"""
Voice Service — Bhashini API integration for Indian language TTS/ASR.
Phase 2 feature.
"""


class VoiceService:
    """
    Handles voice input/output via the Bhashini API.

    ASR: Converts student's spoken regional language to text
    TTS: Converts AI response text to spoken regional language audio

    Supported languages (Phase 2):
    Hindi, Kannada, Tamil, Telugu, Marathi, Bengali, Gujarati, Odia, Punjabi, Malayalam

    TODO (Phase 2): Implement Bhashini API calls.
    """

    SUPPORTED_LANGUAGES = [
        "Hindi", "Kannada", "Tamil", "Telugu", "Marathi",
        "Bengali", "Gujarati", "Odia", "Punjabi", "Malayalam",
    ]

    async def speech_to_text(self, audio_bytes: bytes, language: str) -> str:
        """
        Convert audio bytes to text using Bhashini ASR.

        TODO (Phase 2): Implement Bhashini ASR API call.
        """
        raise NotImplementedError("Voice service not yet implemented — Phase 2")

    async def text_to_speech(self, text: str, language: str) -> bytes:
        """
        Convert text to audio bytes using Bhashini TTS.

        TODO (Phase 2): Implement Bhashini TTS API call.
        """
        raise NotImplementedError("Voice service not yet implemented — Phase 2")


voice_service = VoiceService()
