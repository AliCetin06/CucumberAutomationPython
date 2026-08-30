from behave import given, then
# utils klasöründeki DatabaseUtils sinifini koda dahil ediyoruz
from utils.db_utils import DatabaseUtils


@given('The database connection is established')
def step_connect_db(context):
    # Java'daki static metot çağrisi gibi direkt bağlantiyi başlatiyoruz
    DatabaseUtils.connect_data_base()


@then('The system should verify that a customer named "{customer_name}" exists in the database')
def step_verify_customer(context, customer_name):
    # Sizin mevcut 'customers' tablonuz için dinamik SQL sorgusu hazirliyoruz
    query = f"SELECT customerName FROM customers WHERE customerName = '{customer_name}'"

    # Java'daki getResultSet mantiğiyla sorguyu gönderip tüm sonuçlari aliyoruz
    results = DatabaseUtils.get_result_set(query)

    # İşimiz bittiği için veri tabani bağlantisini güvenle kapatiyoruz
    DatabaseUtils.close_data_base_connection()

    # 1. Doğrulama: Veri tabanindan boş değer (None) veya boş liste dönmediğini kontrol et
    assert results is not None and len(results) > 0, f"Customer '{customer_name}' was not found in the database!"

    # Python'da fetchall() sonucu list içinde tuple döner -> (('Atelier graphique',),)
    # Bu yüzden gelen ilk satirin ilk elemanini alip test ediyoruz
    actual_name = results[0][0]
    assert actual_name == customer_name, f"Expected customer name '{customer_name}', but found '{actual_name}'"
