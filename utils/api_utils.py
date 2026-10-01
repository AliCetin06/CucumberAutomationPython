import os

import requests  # HTTP istekleri (GET, POST, PUT, PATCH, DELETE) atmak icin kullanilan kutuphane


class ApiUtils:
    # Test edilen API'nin ana adresi.
    # Baska bir proje icin degistir veya BASE_URL environment variable ile ver.
    BASE_URL = os.getenv("BASE_URL", "https://reqres.in/api")

    # Varsayilan zaman asimi (saniye). Olmazsa cevap vermeyen istek testi sonsuza kadar bekletir.
    TIMEOUT = 10

    # Her istekle gonderilen varsayilan header'lar.
    # Reqres x-api-key ister. Key'i koda gommek yerine environment variable'dan oku.
    # Lokalde:  export REQRES_API_KEY=your_key
    # CI'da:    secret olarak tanimla ve environment variable olarak ver
    HEADERS = {"x-api-key": os.getenv("REQRES_API_KEY", "")}

    # ------------------------------------------------------------------
    # Genel katman: baska API testlerinde de dogrudan kullanilabilir
    # ------------------------------------------------------------------
    @staticmethod
    def request(method, endpoint, payload=None, params=None, headers=None):
        """
        Herhangi bir HTTP istegi atar ve response nesnesini dondurur.

        method   : "GET", "POST", "PUT", "PATCH", "DELETE"
        endpoint : base URL'den sonraki yol, ornek: "/users/2"
        payload  : JSON body olarak gonderilecek dict (POST, PUT, PATCH)
        params   : query string olarak gonderilecek dict, ornek: {"page": 2}
        headers  : ek header'lar, varsayilan HEADERS ustune eklenir
        """
        url = f"{ApiUtils.BASE_URL}{endpoint}"
        merged_headers = {**ApiUtils.HEADERS, **(headers or {})}

        # json= kullanilinca requests Content-Type: application/json'i otomatik ayarlar
        return requests.request(
            method=method,
            url=url,
            json=payload,
            params=params,
            headers=merged_headers,
            timeout=ApiUtils.TIMEOUT,
        )

    @staticmethod
    def get(endpoint, params=None, headers=None):
        return ApiUtils.request("GET", endpoint, params=params, headers=headers)

    @staticmethod
    def post(endpoint, payload=None, headers=None):
        return ApiUtils.request("POST", endpoint, payload=payload, headers=headers)

    @staticmethod
    def put(endpoint, payload=None, headers=None):
        return ApiUtils.request("PUT", endpoint, payload=payload, headers=headers)

    @staticmethod
    def patch(endpoint, payload=None, headers=None):
        return ApiUtils.request("PATCH", endpoint, payload=payload, headers=headers)

    @staticmethod
    def delete(endpoint, headers=None):
        return ApiUtils.request("DELETE", endpoint, headers=headers)

    # ------------------------------------------------------------------
    # Reqres'e ozel metodlar (users kaynagi)
    # ------------------------------------------------------------------
    @staticmethod
    def create_user(name, job):
        # POST /users : yeni kullanici olusturur
        return ApiUtils.post("/users", payload={"name": name, "job": job})

    @staticmethod
    def get_user(user_id):
        # GET /users/{id} : tek bir kullaniciyi getirir, ornek: /users/2
        return ApiUtils.get(f"/users/{user_id}")

    @staticmethod
    def list_users(page=1):
        # GET /users?page=N : sayfalanmis kullanici listesini getirir
        return ApiUtils.get("/users", params={"page": page})

    @staticmethod
    def update_user(user_id, name, job):
        # PUT /users/{id} : komple guncelleme, tum alanlar gonderilir
        return ApiUtils.put(f"/users/{user_id}", payload={"name": name, "job": job})

    @staticmethod
    def patch_user(user_id, **fields):
        # PATCH /users/{id} : kismi guncelleme, sadece degisen alanlar gonderilir
        # Kullanim: ApiUtils.patch_user(2, job="QA Lead")
        return ApiUtils.patch(f"/users/{user_id}", payload=fields)

    @staticmethod
    def delete_user(user_id):
        # DELETE /users/{id} : kullaniciyi siler, Reqres 204 ve bos body doner
        return ApiUtils.delete(f"/users/{user_id}")