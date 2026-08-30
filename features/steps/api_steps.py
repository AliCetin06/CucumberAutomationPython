from behave import given, when, then  # Gherkin adimlarini (Given/When/Then) Python fonksiyonlarina bağlayan decorator'lar
from utils.api_utils import ApiUtils  # Bir önceki dosyada yazdiğimiz API çağri sinifi

@given('The API endpoint is available')
def step_check_api(context):
    # Bu adim şu an sadece BASE_URL'i context'e kaydediyor
    # İleride burada gerçek bir "API ayakta mi" kontrolü (health check) de yapilabilir
    context.api_base_url = ApiUtils.BASE_URL

@when('I create a new user named "{user_name}" with job "{job}"')
def step_create_user(context, user_name, job):
    # Feature dosyasindaki "{user_name}" ve "{job}" kisimlari buraya parametre olarak otomatik geliyor
    # ApiUtils'teki create_user metodunu çağirip dönen response'u context'e kaydediyoruz
    # Böylece bu response'a sonraki (Then) adimlarinda erişebiliyoruz
    context.response = ApiUtils.create_user(user_name, job)

@when('I get the user with id {user_id:d}')
def step_get_user(context, user_id):
    # {user_id:d} -> ":d" burada gelen değerin integer (sayi) olarak parse edilmesini sağliyor
    # Yoksa user_id string ("2") olarak gelirdi, :d sayesinde int (2) olarak gelir
    context.response = ApiUtils.get_user(user_id)

@then('The response status code should be {status_code:d}')
def step_check_status(context, status_code):
    # context.response -> bir önceki When adiminda kaydettiğimiz response nesnesi
    # .status_code -> HTTP durum kodunu verir (200, 201, 404, 500 vb.)
    # assert -> beklenen ile gerçek değeri karşilaştirir, eşleşmezse test FAIL olur ve hata mesaji basar
    assert context.response.status_code == status_code, \
        f"Beklenen {status_code}, gelen {context.response.status_code}"

@then('The response should contain user name "{expected_name}"')
def step_check_body(context, expected_name):
    # .json() -> response body'sini (JSON string) Python dictionary'sine çevirir
    body = context.response.json()

    # body["name"] -> API'nin döndürdüğü JSON içindeki "name" alanini okuyoruz
    # Bunu feature dosyasindaki beklenen isimle karşilaştiriyoruz
    assert body["name"] == expected_name, \
        f"Beklenen isim {expected_name}, gelen {body.get('name')}"