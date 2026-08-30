import requests  # HTTP istekleri (GET, POST, DELETE vb.) atmak için kullanilan kütüphane

class ApiUtils:
    # Test edeceğimiz API'nin ana adresi (base URL)
    # Kendi projenizde burayi gerçek API adresinizle değiştireceksiniz
    BASE_URL = "https://reqres.in/api"

    @staticmethod
    def create_user(name, job):
        # API'ye gönderilecek veri (JSON body) - Java'daki request body gibi düşünebilirsiniz
        payload = {"name": name, "job": job}

        # POST isteği atiyoruz: /users endpoint'ine payload'i JSON olarak gönderiyoruz
        # requests.post() otomatik olarak Content-Type: application/json ayarlar
        response = requests.post(f"{ApiUtils.BASE_URL}/users", json=payload)

        # Gelen response nesnesini (status code + body içeren) geri döndürüyoruz
        # Bu nesneyi step dosyasinda context.response içine kaydedip kullanacağiz
        return response

    @staticmethod
    def get_user(user_id):
        # GET isteği atiyoruz: belirli bir kullaniciyi ID'sine göre çekiyoruz
        # f-string ile URL'nin sonuna user_id'yi ekliyoruz -> /users/2 gibi
        response = requests.get(f"{ApiUtils.BASE_URL}/users/{user_id}")
        return response

    @staticmethod
    def delete_user(user_id):
        # DELETE isteği atiyoruz: belirli bir kullaniciyi siliyoruz
        response = requests.delete(f"{ApiUtils.BASE_URL}/users/{user_id}")
        return response