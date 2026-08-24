import os
import configparser


class PropertyReader:
    _prop = configparser.ConfigParser()

    # Bu dosyanın (property_reader.py) bulunduğu klasörden proje kök dizinine göre yol hesapla.
    # Kendi proje yapına göre .. sayısını ayarlaman gerekebilir (örnekte utils/ altında olduğu varsayıldı).
    _DEFAULT_CONFIG_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "resources", "config", "config.properties"
    )

    @classmethod
    def init_property(cls, file_path: str = None) -> None:
        """
        config.properties dosyasını yükler.
        configparser varsayılan olarak [section] başlıkları bekler.
        Section başlığı olmayan standart Java .properties dosyalarını
        okuyabilmek için dummy bir [DEFAULT] başlığı ekleyerek okuma yapar.
        """
        if file_path is None:
            file_path = cls._DEFAULT_CONFIG_PATH

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Config dosyası bulunamadı: {file_path}")

        # Standart Java properties dosyalarını desteklemek için:
        with open(file_path, "r", encoding="utf-8") as file:
            config_string = "[DEFAULT]\n" + file.read()
            cls._prop.read_string(config_string)

    @classmethod
    def get_property(cls, key: str) -> str:
        """
        Verilen key'e karşılık gelen değeri döndürür.
        Key bulunamazsa None döner.
        """
        return cls._prop.get("DEFAULT", key, fallback=None)