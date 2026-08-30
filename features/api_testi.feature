# Feature: Bu dosya kullanici (user) API'sinin CRUD işlemlerini doğrular
Feature: User API Validation

  # Senaryo 1: API üzerinden yeni bir kullanici oluşturmayi test ediyoruz
  Scenario: Verify a new user can be created via API
    Given The API endpoint is available
    # "Ali Cetin" isminde, "QA Engineer" işiyle yeni kullanici oluşturma isteği atiyoruz
    When I create a new user named "Ali Cetin" with job "QA Engineer"
    # Başarili bir "oluşturma" işleminde HTTP standardina göre 201 (Created) dönmeli
    Then The response status code should be 201
    # Response body'sinin içinde gönderdiğimiz isim doğru şekilde dönmüş mü kontrol ediyoruz
    And The response should contain user name "Ali Cetin"

  # Senaryo 2: Var olan bir kullaniciyi ID ile çekmeyi test ediyoruz
  Scenario: Verify an existing user can be retrieved via API
    Given The API endpoint is available
    # ID'si 2 olan kullaniciyi GET isteğiyle çekiyoruz
    When I get the user with id 2
    # Başarili bir "getirme" işleminde HTTP standardina göre 200 (OK) dönmeli
    Then The response status code should be 200