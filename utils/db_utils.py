import pymysql
# Sizin yazdiğiniz PropertyReader sinifini içeri aliyoruz
from utils.property_reader import PropertyReader

class DatabaseUtils:
    connection = None
    cursor = None

    @classmethod
    def connect_data_base(cls):
        """Sizin PropertyReader sinifinizla verileri okuyarak veri tabanina bağlanir."""
        try:
            # 1. KRİTİK ADIM: Önce config.properties dosyasini hafizaya yüklüyoruz
            PropertyReader.init_property()

            # 2. Sizin get_property metodunuzla verileri çekiyoruz
            db_host = PropertyReader.get_property("db.host")
            db_user = PropertyReader.get_property("db.user")
            db_password = PropertyReader.get_property("db.password")
            db_name = PropertyReader.get_property("db.name")

            # 3. Bağlantiyi kuruyoruz
            cls.connection = pymysql.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name,
                port=3306
            )
            cls.cursor = cls.connection.cursor()
            print("Database connection successfully established using your PropertyReader!")
        except Exception as e:
            print(f"Connection failed: {e}")

    # get_result_set ve close_data_base_connection metotlari daha önce yazdiğimiz gibi kalacak...
    @classmethod
    def get_result_set(cls, query: str):
        try:
            cls.cursor.execute(query)
            return cls.cursor.fetchall()
        except Exception as e:
            print(f"Query execution failed: {e}")
            return None

    @classmethod
    def close_data_base_connection(cls):
        try:
            if cls.cursor:
                cls.cursor.close()
            if cls.connection:
                cls.connection.close()
            print("Database connection successfully closed.")
        except Exception as e:
            print(f"Failed to close connection: {e}")
