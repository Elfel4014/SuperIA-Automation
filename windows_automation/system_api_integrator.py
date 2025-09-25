import ctypes

try:
    import win32com.client
except ImportError:
    # Mock win32com.client para ambientes não-Windows
    class MockWMIObject:
        def ExecQuery(self, query):
            print(f"Mock: Executando query WMI: {query}")
            # Retorna um objeto mock para simular resultados
            class MockOSInfo:
                Caption = "Mock OS"
                Version = "Mock Version"
                BuildNumber = "Mock Build"
                OSArchitecture = "Mock Arch"
                FreePhysicalMemory = 1024 * 1024 * 2 # 2GB
                TotalPhysicalMemory = 1024 * 1024 * 4 # 4GB
            class MockCPUInfo:
                Name = "Mock CPU"
                NumberOfCores = 2
                NumberOfLogicalProcessors = 4
                MaxClockSpeed = 2500

            if "Win32_OperatingSystem" in query:
                return [MockOSInfo()]
            elif "Win32_Processor" in query:
                return [MockCPUInfo()]
            return []

    class MockWin32ComClient:
        def GetObject(self, moniker):
            print(f"Mock: Obtendo objeto COM: {moniker}")
            return MockWMIObject()

    win32com = type("module", (object,), {"client": MockWin32ComClient()})

class SystemAPIIntegrator:
    def __init__(self):
        pass

    def get_windows_version_ctypes(self):
        # Exemplo de uso de ctypes para chamar uma função da API do Windows
        # GetVersionEx é uma função mais antiga, mas demonstra o uso de ctypes
        # Para versões modernas do Windows, GetVersionEx pode retornar informações de compatibilidade
        # Para informações mais precisas, WMI é geralmente preferível.
        try:
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            # Define a estrutura OSVERSIONINFOEXW
            class OSVERSIONINFOEXW(ctypes.Structure):
                _fields_ = [
                    ("dwOSVersionInfoSize", ctypes.c_ulong),
                    ("dwMajorVersion", ctypes.c_ulong),
                    ("dwMinorVersion", ctypes.c_ulong),
                    ("dwBuildNumber", ctypes.c_ulong),
                    ("dwPlatformId", ctypes.c_ulong),
                    ("szCSDVersion", ctypes.c_wchar * 128),
                    ("wServicePackMajor", ctypes.c_ushort),
                    ("wServicePackMinor", ctypes.c_ushort),
                    ("wSuiteMask", ctypes.c_ushort),
                    ("wProductType", ctypes.c_ubyte),
                    ("wReserved", ctypes.c_ubyte)
                ]

            os_version_info = OSVERSIONINFOEXW()
            os_version_info.dwOSVersionInfoSize = ctypes.sizeof(OSVERSIONINFOEXW)

            # Mock GetVersionExW para Linux
            if sys.platform != "win32":
                print("Mock: Chamada ctypes.GetVersionExW (apenas para Windows)")
                return "Mock Windows Version: 10.0 Build 19041"

            if kernel32.GetVersionExW(ctypes.byref(os_version_info)):
                version_str = f"Windows Version: {os_version_info.dwMajorVersion}.{os_version_info.dwMinorVersion} Build {os_version_info.dwBuildNumber}"
                print(version_str)
                return version_str
            else:
                print("Erro ao obter informações da versão do Windows via ctypes.")
                return None
        except Exception as e:
            print(f"Erro ao usar ctypes para GetVersionEx: {e}")
            return None

    def get_system_info_wmi(self):
        # Exemplo de uso de pywin32 (win32com) para interagir com WMI
        try:
            wmi = win32com.client.GetObject("winmgmts:")
            # Obter informações do sistema operacional
            os_info = wmi.ExecQuery("SELECT * FROM Win32_OperatingSystem")
            for os in os_info:
                system_info = {
                    "Caption": os.Caption,
                    "Version": os.Version,
                    "BuildNumber": os.BuildNumber,
                    "OSArchitecture": "Mock Architecture", # Mocked
                    "FreePhysicalMemory": f"{int(os.FreePhysicalMemory) / 1024 / 1024:.2f} GB",
                    "TotalPhysicalMemory": f"{int(os.TotalPhysicalMemory) / 1024 / 1024:.2f} GB"
                }
                print("\n--- Informações do Sistema (WMI) ---")
                for key, value in system_info.items():
                    print(f"{key}: {value}")
                return system_info
            return None
        except Exception as e:
            print(f"Erro ao obter informações do sistema via WMI: {e}")
            return None

    def get_cpu_info_wmi(self):
        try:
            wmi = win32com.client.GetObject("winmgmts:")
            cpu_info = wmi.ExecQuery("SELECT * FROM Win32_Processor")
            processors = []
            for cpu in cpu_info:
                processor_details = {
                    "Name": cpu.Name,
                    "NumberOfCores": cpu.NumberOfCores,
                    "NumberOfLogicalProcessors": cpu.NumberOfLogicalProcessors,
                    "MaxClockSpeed": f"{cpu.MaxClockSpeed} MHz"
                }
                processors.append(processor_details)
            print("\n--- Informações da CPU (WMI) ---")
            for i, proc in enumerate(processors):
                print(f"Processor {i+1}:")
                for key, value in proc.items():
                    print(f"  {key}: {value}")
            return processors
        except Exception as e:
            print(f"Erro ao obter informações da CPU via WMI: {e}")
            return None

if __name__ == "__main__":
    import sys
    integrator = SystemAPIIntegrator()

    # Testar ctypes (pode não funcionar corretamente em todas as VMs ou ambientes)
    print("\n--- Testando GetVersionEx via ctypes ---")
    integrator.get_windows_version_ctypes()

    # Testar WMI via pywin32 (requer pywin32 instalado e ambiente Windows)
    print("\n--- Testando informações do sistema via WMI ---")
    integrator.get_system_info_wmi()

    print("\n--- Testando informações da CPU via WMI ---")
    integrator.get_cpu_info_wmi()

    print("\n--- Exemplo de uso de ctypes para MessageBox (apenas para Windows) ---")
    # ctypes.windll.user32.MessageBoxW(0, "Hello SuperIA!", "Windows API Test", 0)

