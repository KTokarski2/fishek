import os
import json
import requests
from pathlib import Path

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.1"))
PROMPTS_DIR = Path(os.getenv("PROMPTS_DIR", "prompts"))

def load_prompt(filename: str, placeholders: dict[str, str]) -> str:
    prompt_path = PROMPTS_DIR / filename
    template = prompt_path.read_text(encoding="utf-8")
    for tag, value in placeholders.items():
        template = template.replace(tag, value)
    return template

def call_ollama(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": OLLAMA_TEMPERATURE
        },
    }
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json=payload,
        timeout=60
    )
    response.raise_for_status()
    return response.json()["response"].strip()

def get_translation(word: str, language: str) -> str:
    prompt = load_prompt(
        "translate.txt",
        {
            "<Word>": word,
            "<Language>": language
        },
    )
    return call_ollama(prompt)

def evaluate_translation(original_sentence: str, translated_sentence: str) -> str:
    prompt = load_prompt(
        "evaluate.txt",
        {
            "<OriginalSentence>": original_sentence,
            "<TranslatedSentence>": translated_sentence
        },
    )
    raw = call_ollama(prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw_response": raw}