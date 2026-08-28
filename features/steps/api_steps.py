from behave import given, when, then  # Gherkin adımlarını (Given/When/Then) Python fonksiyonlarına bağlayan decorator'lar
from utils.api_utils import ApiUtils  # Bir önceki dosyada yazdığımız API çağrı sınıfı

@given('The API endpoint is available')
def step_check_api(context):
    # Bu adım şu an sadece BASE_URL'i context'e kaydediyor
    # İleride burada gerçek bir "API ayakta mı" kontrolü (health check) de yapılabilir
    context.api_base_url = ApiUtils.BASE_URL

@when('I create a new user named "{user_name}" with job "{job}"')
def step_create_user(context, user_name, job):
    # Feature dosyasındaki "{user_name}" ve "{job}" kısımları buraya parametre olarak otomatik geliyor
    # ApiUtils'teki create_user metodunu çağırıp dönen response'u context'e kaydediyoruz
    # Böylece bu response'a sonraki (Then) adımlarında erişebiliyoruz
    context.response = ApiUtils.create_user(user_name, job)

@when('I get the user with id {user_id:d}')
def step_get_user(context, user_id):
    # {user_id:d} -> ":d" burada gelen değerin integer (sayı) olarak parse edilmesini sağlıyor
    # Yoksa user_id string ("2") olarak gelirdi, :d sayesinde int (2) olarak gelir
    context.response = ApiUtils.get_user(user_id)

@then('The response status code should be {status_code:d}')
def step_check_status(context, status_code):
    # context.response -> bir önceki When adımında kaydettiğimiz response nesnesi
    # .status_code -> HTTP durum kodunu verir (200, 201, 404, 500 vb.)
    # assert -> beklenen ile gerçek değeri karşılaştırır, eşleşmezse test FAIL olur ve hata mesajı basar
    assert context.response.status_code == status_code, \
        f"Beklenen {status_code}, gelen {context.response.status_code}"

@then('The response should contain user name "{expected_name}"')
def step_check_body(context, expected_name):
    # .json() -> response body'sini (JSON string) Python dictionary'sine çevirir
    body = context.response.json()

    # body["name"] -> API'nin döndürdüğü JSON içindeki "name" alanını okuyoruz
    # Bunu feature dosyasındaki beklenen isimle karşılaştırıyoruz
    assert body["name"] == expected_name, \
        f"Beklenen isim {expected_name}, gelen {body.get('name')}"