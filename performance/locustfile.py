from locust import HttpUser, task, between
# Gerekli 3 araç: sanal kullanıcı sınıfı, görev etiketi, bekleme fonksiyonu

class APIUser(HttpUser):
    # Sanal kullanıcıyı tanımlayan sınıf

    wait_time = between(1, 2)
    # Her istek arasında 1-2 saniye bekle (gerçekçi olsun diye)

    host = "https://jsonplaceholder.typicode.com"
    # Test edilecek sitenin ana adresi

    @task
    # Bu fonksiyon bir "görev" (Locust bunu tekrar tekrar çalıştırır)
    def get_post(self):
        self.client.get("/posts/1")
        # host + "/posts/1" adresine GET isteği gönder

        #localhost:8089  = Kumanda (elindeki cihaz)
        #          → butona basıyorsun (Start swarm)
         #         → ekranda sonucu görüyorsun (kaç istek, kaç hata)

        # host (locustfile.py içinde) = Televizyon (asıl hedef)
                #  → kumandayla yönettiğin şey
                #  → gerçek "yayın" (yük) buraya gidiyor
