import os
import traceback
import allure

from utils.driver_utils import DriverUtils
from utils.property_reader import PropertyReader
from utils.ai_analyzer import analyze_failure


def before_scenario(context, scenario):
    try:
        PropertyReader.init_property()

        scenario_tags = set(scenario.tags) if hasattr(scenario, "tags") else set()
        feature_tags = set(scenario.feature.tags) if hasattr(scenario.feature, "tags") else set()
        all_tags = scenario_tags.union(feature_tags)

        if "api" in all_tags or "db" in all_tags:
            context.driver = None
            return

        DriverUtils.create_driver()
        context.driver = DriverUtils.get_driver()

    except Exception as setup_err:
        # Hook içinde patlama Allure'ın senaryo açma/kapama eşleşmesini bozuyor.
        # Bu yüzden burada asla raise etmiyoruz; senaryoyu güvenli şekilde
        # "driver yok" durumuna düşürüp devam ediyoruz. Step'ler zaten
        # driver'a ihtiyaç duyduğunda kendi hatasını verecek.
        print(f"[BEFORE_SCENARIO HATASI]: {setup_err}")
        traceback.print_exc()
        context.driver = None


def after_scenario(context, scenario):
    driver = getattr(context, "driver", None)

    try:
        if scenario.status == "failed":
            print(f"\n[AI OTOMASYON BILGISI] '{scenario.name}' senaryosu patladı. AI analizi başlatılıyor...")

            failed_step = next((step for step in scenario.steps if step.status == "failed"), None)
            error_msg = "Bilinmeyen Hata"
            stack_trace = ""

            if failed_step and failed_step.exception:
                error_msg = str(failed_step.exception)
                stack_trace = "".join(
                    traceback.format_exception(
                        type(failed_step.exception),
                        failed_step.exception,
                        failed_step.exception.__traceback__
                    )
                )

            screenshot_path = None
            if driver:
                try:
                    os.makedirs("reports/screenshots", exist_ok=True)
                    safe_name = scenario.name.replace(" ", "_").replace("/", "_")
                    screenshot_path = f"reports/screenshots/{safe_name}.png"
                    driver.save_screenshot(screenshot_path)

                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name="Ekran Görüntüsü",
                        attachment_type=allure.attachment_type.PNG
                    )
                except Exception as img_err:
                    print(f"[EKRAN GÖRÜNTÜSÜ HATASI]: {img_err}")

            try:
                ai_report = analyze_failure(scenario.name, error_msg, stack_trace, screenshot_path)
            except Exception as ai_err:
                ai_report = f"[AI ANALİZ ÇAĞRISI BAŞARISIZ]: {ai_err}"

            print("\n================ 🤖 AI HATA ANALIZ RAPORU ================")
            print(ai_report)
            print("=======================================================\n")

            try:
                allure.attach(
                    body=ai_report,
                    name="🤖 AI Hata Analizi",
                    attachment_type=allure.attachment_type.TEXT,
                )
            except Exception as attach_err:
                print(f"[ALLURE ATTACH HATASI]: {attach_err}")

    except Exception as after_err:
        # after_scenario içindeki hiçbir hata dışarı sızmamalı.
        print(f"[AFTER_SCENARIO GENEL HATASI]: {after_err}")
        traceback.print_exc()

    finally:
        # Driver her durumda kapatılmalı - try/finally ile garanti altına alıyoruz.
        if driver:
            try:
                DriverUtils.quit_driver()
            except Exception as quit_err:
                print(f"[DRIVER QUIT HATASI]: {quit_err}")
            finally:
                context.driver = None