# # translate_api.py  (exact copy of the “alternative solution” you posted)
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import uvicorn
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = FastAPI(title='IndicTrans2 Translation API')
# translator = None

# LANGUAGE_MAP = {
#     'en': 'eng_Latn',
#     'hi': 'hin_Deva',
#     'kn': 'kan_Knda',
#     'ml': 'mal_Mlym',
#     'ta': 'tam_Taml',
#     'te': 'tel_Telu'
# }

# class TranslateRequest(BaseModel):
#     q: str
#     source: str
#     target: str
#     format: str = 'text'

# class TranslateResponse(BaseModel):
#     translatedText: str

# def initialize_translator():
#     global translator
#     try:
#         logger.info('Initializing IndicTrans2...')
#         from IndicTransToolkit import IndicProcessor
#         translator = IndicProcessor(inference='cpu')
#         logger.info('IndicTrans2 ready')
#         return True
#     except Exception as e:
#         logger.error(f'Init failed: {e}')
#         return False

# @app.on_event('startup')
# async def startup_event():
#     initialize_translator()

# @app.get('/health')
# async def health_check():
#     return {'status': 'healthy' if translator else 'degraded'}

# @app.post('/translate')
# async def translate(request: TranslateRequest) -> TranslateResponse:
#     try:
#         if not request.q or request.source == request.target:
#             return TranslateResponse(translatedText=request.q)

#         if not translator:
#             return TranslateResponse(translatedText=request.q)

#         translations = translator.translate_paragraph(
#             input_sentences=[request.q],
#             src_lang=LANGUAGE_MAP[request.source],
#             tgt_lang=LANGUAGE_MAP[request.target]
#         )

#         return TranslateResponse(translatedText=translations[0] if translations else request.q)
#     except Exception as e:
#         logger.error(f'Error: {e}')
#         return TranslateResponse(translatedText=request.q)

# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=5000, log_level='info')








from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import logging
import ctranslate2
import sentencepiece as spm
from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
from indicnlp.tokenize import indic_tokenize

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title='IndicTrans2 Translation API')

# Model paths (will be downloaded on first run)
MODEL_DIR = "/app/models/indictrans2-indic-en-1B"
SP_MODEL_PATH = f"{MODEL_DIR}/spm.model"

translator = None
sp_processor = None
normalizers = {}

LANGUAGE_MAP = {
    'en': 'eng_Latn',
    'hi': 'hin_Deva',
    'kn': 'kan_Knda',
    'ml': 'mal_Mlym',
    'ta': 'tam_Taml',
    'te': 'tel_Telu'
}

class TranslateRequest(BaseModel):
    q: str
    source: str
    target: str

class TranslateResponse(BaseModel):
    translatedText: str

def download_model():
    import os
    import urllib.request
    import zipfile

    if os.path.exists(MODEL_DIR):
        return

    logger.info("Downloading IndicTrans2 model (~1.2 GB)...")
    url = "https://huggingface.co/ai4bharat/indictrans2-indic-en-1B/resolve/main/model.zip"
    zip_path = "/tmp/model.zip"
    urllib.request.urlretrieve(url, zip_path)

    os.makedirs(MODEL_DIR, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(MODEL_DIR)
    os.remove(zip_path)
    logger.info("Model downloaded and extracted.")

def initialize():
    global translator, sp_processor, normalizers

    download_model()

    if not translator:
        logger.info("Loading CTranslate2 model...")
        translator = ctranslate2.Translator(MODEL_DIR, device="cpu")

    if not sp_processor:
        logger.info("Loading SentencePiece model...")
        sp_processor = spm.SentencePieceProcessor(SP_MODEL_PATH)

    # Initialize normalizers
    for lang in ['hi', 'kn', 'ml', 'ta', 'te']:
        if lang not in normalizers:
            factory = IndicNormalizerFactory()
            normalizer = factory.get_normalizer(lang)
            normalizers[lang] = normalizer

    logger.info("IndicTrans2 ready")

def normalize_text(text: str, lang: str) -> str:
    if lang == 'en':
        return text
    normalizer = normalizers.get(lang)
    if normalizer:
        return normalizer.normalize(text)
    return text

def preprocess(text: str, lang: str) -> str:
    text = normalize_text(text, lang)
    tokens = indic_tokenize.trivial_tokenize(text, lang)
    return " ".join(tokens)

def postprocess(text: str) -> str:
    return text.replace(" ", "").replace("▁", " ").strip()

@app.on_event("startup")
async def startup():
    initialize()

@app.get("/health")
async def health():
    return {"status": "healthy" if translator else "loading"}

@app.post("/translate")
async def translate(req: TranslateRequest) -> TranslateResponse:
    try:
        if not req.q.strip() or req.source == req.target:
            return TranslateResponse(translatedText=req.q)

        if req.source not in LANGUAGE_MAP or req.target not in LANGUAGE_MAP:
            raise HTTPException(400, "Unsupported language")

        if not translator:
            return TranslateResponse(translatedText=req.q)

        src_lang = LANGUAGE_MAP[req.source]
        tgt_lang = LANGUAGE_MAP[req.target]

        # Preprocess
        processed = preprocess(req.q, req.source)
        tokenized = sp_processor.encode_as_pieces(processed)
        input_text = " ".join(tokenized)

        # Translate
        source = ctranslate2.StorageView.from_array(
            [sp_processor.encode_as_ids(input_text)]
        )
        results = translator.translate_batch(
            [source],
            beam_size=4,
            max_decoding_length=200,
            target_prefix=[[tgt_lang]]
        )
        output_tokens = results[0].hypotheses[0]
        output_text = sp_processor.decode(output_tokens)

        # Postprocess
        final = postprocess(output_text)

        return TranslateResponse(translatedText=final)

    except Exception as e:
        logger.error(f"Translation error: {e}")
        return TranslateResponse(translatedText=req.q)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)