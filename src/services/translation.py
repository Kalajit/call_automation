import asyncio
from typing import List
from src.config.settings import translation_client, TRANSLATE_PARENT
from src.utils.logging_config import get_logger
from multilingual_service import translate_text_indictrans

logger = get_logger(__name__)


async def translate_batch(
    texts: List[str], 
    target_lang: str, 
    source_lang: str = 'en'
) -> List[str]:
    """
    Batch translation using Google Cloud Translation.
    """
    if target_lang == source_lang or not texts:
        return texts

    try:
        logger.info(f"🌐 Batch translating {len(texts)} texts: {source_lang} → {target_lang}")

        def _translate_batch():
            response = translation_client.translate_text(
                request={
                    "parent": TRANSLATE_PARENT,
                    "contents": texts,
                    "mime_type": "text/plain",
                    "source_language_code": source_lang,
                    "target_language_code": target_lang,
                }
            )
            return [t.translated_text for t in response.translations]

        translated_texts = await asyncio.get_event_loop().run_in_executor(
            None, 
            _translate_batch
        )

        if len(translated_texts) == len(texts):
            logger.info(f"✅ Batch translation complete: {len(texts)} texts")
            return translated_texts

        logger.warning("⚠️ Batch translation length mismatch, falling back to per‑item")
    except Exception as e:
        logger.error(f"❌ Batch translation error: {e}", exc_info=True)

    # Fallback: per‑item
    return await asyncio.gather(*[
        translate_text_indictrans(text, target_lang, source_lang)
        for text in texts
    ])