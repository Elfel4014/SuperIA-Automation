try:
    import winreg
except ImportError:
    # Mock winreg para ambientes não-Windows
    class MockWinreg:
        HKEY_CURRENT_USER = "HKEY_CURRENT_USER"
        HKEY_LOCAL_MACHINE = "HKEY_LOCAL_MACHINE"
        KEY_SET_VALUE = 0x0002
        KEY_READ = 0x20019
        KEY_ALL_ACCESS = 0xF003F
        REG_SZ = 1
        REG_DWORD = 4

        def OpenKey(self, hive, subkey, reserved, access):
            print(f"Mock: Abrindo chave {subkey} em {hive}")
            return self

        def CreateKey(self, hive, subkey):
            print(f"Mock: Criando chave {subkey} em {hive}")
            return self

        def SetValueEx(self, key, name, reserved, type, value):
            print(f"Mock: Definindo valor {name}={value} (tipo {type})")

        def QueryValueEx(self, key, name):
            print(f"Mock: Lendo valor {name}")
            if name == "TestString": return ("Mock String Value", self.REG_SZ)
            if name == "TestDword": return (12345, self.REG_DWORD)
            raise FileNotFoundError

        def DeleteValue(self, key, name):
            print(f"Mock: Excluindo valor {name}")

        def DeleteKey(self, hive, subkey):
            print(f"Mock: Excluindo chave {subkey} em {hive}")

        def CloseKey(self, key):
            print("Mock: Fechando chave")

    winreg = MockWinreg()

class RegistryManager:
    def __init__(self):
        pass

    def _open_key(self, hive, subkey, access):
        try:
            return winreg.OpenKey(hive, subkey, 0, access)
        except FileNotFoundError:
            return None

    def create_key(self, hive, subkey):
        try:
            key = winreg.CreateKey(hive, subkey)
            winreg.CloseKey(key)
            print(f"Chave \'{subkey}\' criada com sucesso em {hive}.")
            return True
        except Exception as e:
            print(f"Erro ao criar chave \'{subkey}\' em {hive}: {e}")
            return False

    def set_value(self, hive, subkey, name, value, value_type=winreg.REG_SZ):
        try:
            key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, name, 0, value_type, value)
            winreg.CloseKey(key)
            print(f"Valor \'{name}\' definido com sucesso em \'{subkey}\'.")
            return True
        except Exception as e:
            print(f"Erro ao definir valor \'{name}\' em \'{subkey}\': {e}")
            return False

    def get_value(self, hive, subkey, name):
        try:
            key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, name)
            winreg.CloseKey(key)
            print(f"Valor \'{name}\' lido de \'{subkey}\': {value}")
            return value
        except FileNotFoundError:
            print(f"Chave ou valor \'{name}\' não encontrado em \'{subkey}\'.")
            return None
        except Exception as e:
            print(f"Erro ao ler valor \'{name}\' de \'{subkey}\': {e}")
            return None

    def delete_value(self, hive, subkey, name):
        try:
            key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, name)
            winreg.CloseKey(key)
            print(f"Valor \'{name}\' excluído com sucesso de \'{subkey}\'.")
            return True
        except FileNotFoundError:
            print(f"Chave ou valor \'{name}\' não encontrado em \'{subkey}\'.")
            return False
        except Exception as e:
            print(f"Erro ao excluir valor \'{name}\' de \'{subkey}\': {e}")
            return False

    def delete_key(self, hive, subkey):
        try:
            winreg.DeleteKey(hive, subkey)
            print(f"Chave \'{subkey}\' excluída com sucesso de {hive}.")
            return True
        except FileNotFoundError:
            print(f"Chave \'{subkey}\' não encontrada em {hive}.")
            return False
        except Exception as e:
            print(f"Erro ao excluir chave \'{subkey}\' em {hive}: {e}")
            return False

if __name__ == "__main__":
    manager = RegistryManager()

    # Exemplo de uso
    test_hive = winreg.HKEY_CURRENT_USER
    test_subkey = r"Software\\SuperIA_Test"

    print("\n--- Testando criação de chave e valores ---")
    manager.create_key(test_hive, test_subkey)
    manager.set_value(test_hive, test_subkey, "TestString", "Hello SuperIA Registry")
    manager.set_value(test_hive, test_subkey, "TestDword", 12345, winreg.REG_DWORD)

    print("\n--- Testando leitura de valores ---")
    string_value = manager.get_value(test_hive, test_subkey, "TestString")
    dword_value = manager.get_value(test_hive, test_subkey, "TestDword")
    non_existent_value = manager.get_value(test_hive, test_subkey, "NonExistent")

    print("\n--- Testando exclusão de valores ---")
    manager.delete_value(test_hive, test_subkey, "TestString")
    manager.delete_value(test_hive, test_subkey, "TestDword")

    print("\n--- Testando exclusão de chave ---")
    manager.delete_key(test_hive, test_subkey)
    manager.delete_key(test_hive, r"Software\\NonExistentKey")

