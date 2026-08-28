# Feature: Bu dosya kullanıcı (user) API'sinin CRUD işlemlerini doğrular
Feature: User API Validation

  # Senaryo 1: API üzerinden yeni bir kullanıcı oluşturmayı test ediyoruz
  Scenario: Verify a new user can be created via API
    Given The API endpoint is available
    # "Ali Cetin" isminde, "QA Engineer" işiyle yeni kullanıcı oluşturma isteği atıyoruz
    When I create a new user named "Ali Cetin" with job "QA Engineer"
    # Başarılı bir "oluşturma" işleminde HTTP standardına göre 201 (Created) dönmeli
    Then The response status code should be 201
    # Response body'sinin içinde gönderdiğimiz isim doğru şekilde dönmüş mü kontrol ediyoruz
    And The response should contain user name "Ali Cetin"

  # Senaryo 2: Var olan bir kullanıcıyı ID ile çekmeyi test ediyoruz
  Scenario: Verify an existing user can be retrieved via API
    Given The API endpoint is available
    # ID'si 2 olan kullanıcıyı GET isteğiyle çekiyoruz
    When I get the user with id 2
    # Başarılı bir "getirme" işleminde HTTP standardına göre 200 (OK) dönmeli
    Then The response status code should be 200