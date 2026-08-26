"""
ai_analyzer.py
--------------
Test senaryosu FAILED olduğunda çağrılır (bkz. environment.py -> after_scenario).
Hata mesajını, stack trace'i ve varsa ekran görüntüsünü Google Gemini API'ye
gönderip kök neden analizi + öneri raporu döndürür.

Kurulum:
    pip install google-genai

Ortam değişkeni (zorunlu):
    export GEMINI_API_KEY="AIza..."
    (PyCharm'da Run/Debug Configuration -> Environment variables kısmına da eklenebilir)
    Key'i https://aistudio.google.com/apikey adresinden ücretsiz alabilirsiniz.
"""

import os
import traceback

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

MODEL_NAME = "gemini-2.5-flash"
MAX_STACK_TRACE_CHARS = 4000  # token limitini şişirmemek için stack trace'i kırpıyoruz


def _build_prompt(scenario_name, error_msg, stack_trace):
    trimmed_trace = stack_trace[-MAX_STACK_TRACE_CHARS:] if stack_trace else "Stack trace yok."

    return f"""Sen bir Selenium/Behave (BDD) test otomasyon uzmanısın. Aşağıda başarısız olan
bir Cucumber/Behave test senaryosunun bilgileri var. Görevin:

1. Hatanın KÖK NEDENİNİ kısaca açıkla (1-2 cümle).
2. Bu hatanın kategori tipini belirt: [Locator/Element Hatası, Zamanlama (Timing/Wait) Hatası,
   Uygulama/Backend Hatası, Test Data Hatası, Framework/Ortam Hatası, Diğer]
3. Somut, uygulanabilir bir DÜZELTME ÖNERİSİ ver (kod örneğiyle destekle, kısa tut).
4. Bu hatanın "flaky" (kararsız/ara sıra oluşan) bir test mi yoksa gerçek bir bug mu
   olduğuna dair bir tahminde bulun.

Senaryo adı: {scenario_name}

Hata mesajı:
{error_msg}

Stack trace (son kısmı):
{trimmed_trace}

Cevabını Türkçe, kısa ve maddeler halinde ver. Gereksiz giriş/özet cümlesi yazma,
doğrudan analize başla."""


def _load_screenshot_bytes(screenshot_path):
    if not screenshot_path or not os.path.exists(screenshot_path):
        return None
    try:
        with open(screenshot_path, "rb") as f:
            return f.read()
    except Exception as e:
        print(f"[AI_ANALYZER] Ekran görüntüsü okunamadı: {e}")
        return None


def analyze_failure(scenario_name, error_msg, stack_trace, screenshot_path=None):
    """
    Başarısız senaryoyu analiz edip okunabilir bir metin raporu döndürür.
    Bu fonksiyon HİÇBİR ZAMAN exception fırlatmamalı; framework'ün akışını
    bozmamak için tüm hatalar yakalanıp mesaj olarak döndürülür.
    """
    if genai is None:
        return (
            "[AI ANALİZ ATLANDI] 'google-genai' paketi kurulu değil.\n"
            "Kurulum için: pip install google-genai"
        )

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return (
            "[AI ANALİZ ATLANDI] GEMINI_API_KEY ortam değişkeni bulunamadı.\n"
            "Terminalde 'export GEMINI_API_KEY=...' ile ayarlayın ya da "
            "PyCharm Run Configuration'a ekleyin.\n"
            "Ücretsiz key: https://aistudio.google.com/apikey"
        )

    try:
        client = genai.Client(api_key=api_key)

        prompt_text = _build_prompt(scenario_name, error_msg, stack_trace)
        contents = [prompt_text]

        image_bytes = _load_screenshot_bytes(screenshot_path)
        if image_bytes:
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type="image/png"))
            contents[0] += "\n\nEkteki ekran görüntüsünü de göz önünde bulundurarak analiz et."

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
        )

        result = (response.text or "").strip()
        return result if result else "[AI ANALİZ] Model boş cevap döndürdü."

    except Exception as e:
        error_detail = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        print(f"[AI_ANALYZER HATASI]\n{error_detail}")
        return f"[AI ANALİZ HATASI] Analiz sırasında bir hata oluştu: {e}"