import configparser
import os


class PropertyReader:
    _prop = configparser.ConfigParser()

    @classmethod
    def init_property(cls, file_path: str = "/Users/alicetin/Desktop/eclipse/CucumberAutomation/src/test/resources/config/config.properties") -> None:
        """
        config.properties dosyasını yükler.
        configparser varsayılan olarak [section] başlıkları bekler.
        Section başlığı olmayan standart Java .properties dosyalarını
        okuyabilmek için dummy bir [DEFAULT] başlığı ekleyerek okuma yapar.
        """
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