"""
ai_analyzer.py
--------------
Test senaryosu FAILED olduÄŸunda Ã§aÄŸrÄ±lÄ±r (bkz. environment.py -> after_scenario).
Hata mesajÄ±nÄ±, stack trace'i ve varsa ekran gÃ¶rÃ¼ntÃ¼sÃ¼nÃ¼ Google Gemini API'ye
gÃ¶nderip kÃ¶k neden analizi + Ã¶neri raporu dÃ¶ndÃ¼rÃ¼r.

Kurulum:
    pip install google-genai

Ortam deÄŸiÅŸkeni (zorunlu):
    export GEMINI_API_KEY="AIza..."
    (PyCharm'da Run/Debug Configuration -> Environment variables kÄ±smÄ±na da eklenebilir)
    Key'i https://aistudio.google.com/apikey adresinden Ã¼cretsiz alabilirsiniz.
"""

import os
import traceback

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-3.6-flash")
MAX_STACK_TRACE_CHARS = 4000  # token limitini ÅŸiÅŸirmemek iÃ§in stack trace'i kÄ±rpÄ±yoruz


def _build_prompt(scenario_name, error_msg, stack_trace):
    trimmed_trace = stack_trace[-MAX_STACK_TRACE_CHARS:] if stack_trace else "Stack trace yok."

    return f"""Sen bir Selenium/Behave (BDD) test otomasyon uzmanÄ±sÄ±n. AÅŸaÄŸÄ±da baÅŸarÄ±sÄ±z olan
bir Cucumber/Behave test senaryosunun bilgileri var. GÃ¶revin:

1. HatanÄ±n KÃ–K NEDENÄ°NÄ° kÄ±saca aÃ§Ä±kla (1-2 cÃ¼mle).
2. Bu hatanÄ±n kategori tipini belirt: [Locator/Element HatasÄ±, Zamanlama (Timing/Wait) HatasÄ±,
   Uygulama/Backend HatasÄ±, Test Data HatasÄ±, Framework/Ortam HatasÄ±, DiÄŸer]
3. Somut, uygulanabilir bir DÃœZELTME Ã–NERÄ°SÄ° ver (kod Ã¶rneÄŸiyle destekle, kÄ±sa tut).
4. Bu hatanÄ±n "flaky" (kararsÄ±z/ara sÄ±ra oluÅŸan) bir test mi yoksa gerÃ§ek bir bug mu
   olduÄŸuna dair bir tahminde bulun.

Senaryo adÄ±: {scenario_name}

Hata mesajÄ±:
{error_msg}

Stack trace (son kÄ±smÄ±):
{trimmed_trace}

CevabÄ±nÄ± TÃ¼rkÃ§e, kÄ±sa ve maddeler halinde ver. Gereksiz giriÅŸ/Ã¶zet cÃ¼mlesi yazma,
doÄŸrudan analize baÅŸla."""


def _load_screenshot_bytes(screenshot_path):
    if not screenshot_path or not os.path.exists(screenshot_path):
        return None
    try:
        with open(screenshot_path, "rb") as f:
            return f.read()
    except Exception as e:
        print(f"[AI_ANALYZER] Ekran gÃ¶rÃ¼ntÃ¼sÃ¼ okunamadÄ±: {e}")
        return None


def analyze_failure(scenario_name, error_msg, stack_trace, screenshot_path=None):
    """
    BaÅŸarÄ±sÄ±z senaryoyu analiz edip okunabilir bir metin raporu dÃ¶ndÃ¼rÃ¼r.
    Bu fonksiyon HÄ°Ã‡BÄ°R ZAMAN exception fÄ±rlatmamalÄ±; framework'Ã¼n akÄ±ÅŸÄ±nÄ±
    bozmamak iÃ§in tÃ¼m hatalar yakalanÄ±p mesaj olarak dÃ¶ndÃ¼rÃ¼lÃ¼r.
    """
    if genai is None:
        return (
            "[AI ANALÄ°Z ATLANDI] 'google-genai' paketi kurulu deÄŸil.\n"
            "Kurulum iÃ§in: pip install google-genai"
        )

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return (
            "[AI ANALÄ°Z ATLANDI] GEMINI_API_KEY ortam deÄŸiÅŸkeni bulunamadÄ±.\n"
            "Terminalde 'export GEMINI_API_KEY=...' ile ayarlayÄ±n ya da "
            "PyCharm Run Configuration'a ekleyin.\n"
            "Ãœcretsiz key: https://aistudio.google.com/apikey"
        )

    try:
        client = genai.Client(api_key=api_key)

        prompt_text = _build_prompt(scenario_name, error_msg, stack_trace)
        contents = [prompt_text]

        image_bytes = _load_screenshot_bytes(screenshot_path)
        if image_bytes:
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type="image/png"))
            contents[0] += "\n\nEkteki ekran gÃ¶rÃ¼ntÃ¼sÃ¼nÃ¼ de gÃ¶z Ã¶nÃ¼nde bulundurarak analiz et."

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
        )

        result = (response.text or "").strip()
        return result if result else "[AI ANALÄ°Z] Model boÅŸ cevap dÃ¶ndÃ¼rdÃ¼."

    except Exception as e:
        error_detail = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        print(f"[AI_ANALYZER HATASI]\n{error_detail}")
        return f"[AI ANALÄ°Z HATASI] Analiz sÄ±rasÄ±nda bir hata oluÅŸtu: {e}"
