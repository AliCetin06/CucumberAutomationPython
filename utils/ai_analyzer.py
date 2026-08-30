"""
ai_analyzer.py
--------------
Test senaryosu FAILED oldugunda cagrilir (bkz. environment.py -> after_scenario).
Hata mesajini, stack trace'i ve varsa ekran goruntusunu Google Gemini API'ye
gonderip kok neden analizi + oneri raporu dondurur.

Kurulum:
    pip install google-genai

Ortam degiskeni (zorunlu):
    export GEMINI_API_KEY="AIza..."
    (PyCharm'da Run/Debug Configuration -> Environment variables kismina da eklenebilir)
    Key'i https://aistudio.google.com/apikey adresinden ucretsiz alabilirsiniz.

Ortam degiskeni (opsiyonel):
    export GEMINI_MODEL_NAME="gemini-3.6-flash"
    Google modelleri sik sik deprecate ediyor (bkz. gemini-2.5-flash, beklenenden
    erken kapatildi). Model adini koda hardcode etmek yerine burada .env / secret
    uzerinden yonetmek, ileride benzer 404 NOT_FOUND surprizlerini onler.
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
MAX_STACK_TRACE_CHARS = 4000  # token limitini sisirmemek icin stack trace'i kirpiyoruz


def _build_prompt(scenario_name, error_msg, stack_trace):
    trimmed_trace = stack_trace[-MAX_STACK_TRACE_CHARS:] if stack_trace else "Stack trace yok."

    return f"""Sen bir Selenium/Behave (BDD) test otomasyon uzmanisin. Asagida basarisiz olan
bir Cucumber/Behave test senaryosunun bilgileri var. Gorevin:

1. Hatanin KOK NEDENINI kisaca acikla (1-2 cumle).
2. Bu hatanin kategori tipini belirt: [Locator/Element Hatasi, Zamanlama (Timing/Wait) Hatasi,
   Uygulama/Backend Hatasi, Test Data Hatasi, Framework/Ortam Hatasi, Diger]
3. Somut, uygulanabilir bir DUZELTME ONERISI ver (kod ornegiyle destekle, kisa tut).
4. Bu hatanin "flaky" (kararsiz/ara sira olusan) bir test mi yoksa gercek bir bug mu
   olduguna dair bir tahminde bulun.

Senaryo adi: {scenario_name}

Hata mesaji:
{error_msg}

Stack trace (son kismi):
{trimmed_trace}

Cevabini Turkce, kisa ve maddeler halinde ver. Gereksiz giris/ozet cumlesi yazma,
dogrudan analize basla."""


def _load_screenshot_bytes(screenshot_path):
    if not screenshot_path or not os.path.exists(screenshot_path):
        return None
    try:
        with open(screenshot_path, "rb") as f:
            return f.read()
    except Exception as e:
        print(f"[AI_ANALYZER] Ekran goruntusu okunamadi: {e}")
        return None


def analyze_failure(scenario_name, error_msg, stack_trace, screenshot_path=None):
    """
    Basarisiz senaryoyu analiz edip okunabilir bir metin raporu dondurur.
    Bu fonksiyon HICBIR ZAMAN exception firlatmamali; framework'un akisini
    bozmamak icin tum hatalar yakalanip mesaj olarak dondurulur.
    """
    if genai is None:
        return (
            "[AI ANALIZ ATLANDI] 'google-genai' paketi kurulu degil.\n"
            "Kurulum icin: pip install google-genai"
        )

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return (
            "[AI ANALIZ ATLANDI] GEMINI_API_KEY ortam degiskeni bulunamadi.\n"
            "Terminalde 'export GEMINI_API_KEY=...' ile ayarlayin ya da "
            "PyCharm Run Configuration'a ekleyin.\n"
            "Ucretsiz key: https://aistudio.google.com/apikey"
        )

    try:
        client = genai.Client(api_key=api_key)

        prompt_text = _build_prompt(scenario_name, error_msg, stack_trace)
        contents = [prompt_text]

        image_bytes = _load_screenshot_bytes(screenshot_path)
        if image_bytes:
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type="image/png"))
            contents[0] += "\n\nEkteki ekran goruntusunu de goz onunde bulundurarak analiz et."

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
        )

        result = (response.text or "").strip()
        return result if result else "[AI ANALIZ] Model bos cevap dondurdu."

    except Exception as e:
        error_detail = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        print(f"[AI_ANALYZER HATASI]\n{error_detail}")
        return f"[AI ANALIZ HATASI] Analiz sirasinda bir hata olustu: {e}"