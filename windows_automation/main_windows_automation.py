import subprocess
import os
import sys

# winreg só está disponível no Windows, então precisamos de um mock para execução em Linux
try:
    import winreg
except ImportError:
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
            if name == "PythonString": return ("Mock String Value", self.REG_SZ)
            if name == "PythonDword": return (12345, self.REG_DWORD)
            raise FileNotFoundError

        def DeleteValue(self, key, name):
            print(f"Mock: Excluindo valor {name}")

        def DeleteKey(self, hive, subkey):
            print(f"Mock: Excluindo chave {subkey} em {hive}")

        def CloseKey(self, key):
            print("Mock: Fechando chave")

    winreg = MockWinreg()

# Adicionar o diretório atual ao PATH para que os módulos possam ser importados
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from registry_manager import RegistryManager
from process_manager import ProcessManager
from system_api_integrator import SystemAPIIntegrator

def run_powershell_script(script_path, *args):
    command = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", script_path]
    command.extend(args)
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("Erro PowerShell:", result.stderr)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar script PowerShell: {e}")
        print("Saída de erro:", e.stderr)
        return None
    except FileNotFoundError:
        print("PowerShell não encontrado. Certifique-se de que está instalado e no PATH.")
        return None

def main():
    print("\n=== Testando Módulos de Automação Windows ===\n")

    # --- Testando RegistryManager (Python) ---
    print("\n--- Testando RegistryManager (Python) ---")
    reg_manager = RegistryManager()
    test_hive = winreg.HKEY_CURRENT_USER
    test_subkey = r"Software\SuperIA_Test_Python"

    reg_manager.create_key(test_hive, test_subkey)
    reg_manager.set_value(test_hive, test_subkey, "PythonString", "Hello from Python")
    reg_manager.set_value(test_hive, test_subkey, "PythonDword", 98765, winreg.REG_DWORD)
    reg_manager.get_value(test_hive, test_subkey, "PythonString")
    reg_manager.delete_value(test_hive, test_subkey, "PythonString")
    reg_manager.delete_key(test_hive, test_subkey)

    # --- Testando RegistryManager (PowerShell) ---
    print("\n--- Testando RegistryManager (PowerShell) ---")
    # Este teste só pode ser executado em um ambiente Windows com PowerShell
    # run_powershell_script("registry_manager.ps1")
    print("Para testar o script PowerShell, execute registry_manager.ps1 manualmente em um ambiente Windows.")

    # --- Testando ProcessManager (Python) ---
    print("\n--- Testando ProcessManager (Python) ---")
    proc_manager = ProcessManager()
    print("Listando os 5 primeiros processos:")
    for p in proc_manager.list_processes()[:5]:
        print(p)
    print("Procurando por processos \'python\':")
    for p in proc_manager.find_process_by_name("python"):
        print(p)
    # Exemplo de iniciar/parar processo (descomentado para ambiente Windows)
    # pid = proc_manager.start_process("notepad.exe")
    # if pid:
    #     import time
    #     time.sleep(3)
    #     proc_manager.stop_process(pid)

    # --- Testando ProcessManager (PowerShell) ---
    print("\n--- Testando ProcessManager (PowerShell) ---")
    # Este teste só pode ser executado em um ambiente Windows com PowerShell
    # run_powershell_script("process_manager.ps1")
    print("Para testar o script PowerShell, execute process_manager.ps1 manualmente em um ambiente Windows.")

    # --- Testando SystemAPIIntegrator (Python) ---
    print("\n--- Testando SystemAPIIntegrator (Python) ---")
    api_integrator = SystemAPIIntegrator()
    # api_integrator.get_windows_version_ctypes() # Pode não funcionar em todas as VMs
    # api_integrator.get_system_info_wmi() # Requer pywin32 e ambiente Windows
    # api_integrator.get_cpu_info_wmi() # Requer pywin32 e ambiente Windows
    print("Os testes para SystemAPIIntegrator (Python) requerem pywin32 e um ambiente Windows real.")

if __name__ == "__main__":
    main()
