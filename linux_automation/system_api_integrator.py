import subprocess
import os

class SystemAPIIntegrator:
    def __init__(self):
        pass

    def _read_file(self, path):
        try:
            with open(path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"Erro ao ler arquivo {path}: {e}")
            return None

    def get_kernel_version(self):
        try:
            version_info = self._read_file('/proc/version')
            if version_info:
                print(f"Versão do Kernel: {version_info.strip().split('(')[0]}")
                return version_info.strip().split('(')[0]
            return None
        except Exception as e:
            print(f"Erro ao obter versão do kernel: {e}")
            return None

    def get_uptime(self):
        try:
            uptime_info = self._read_file('/proc/uptime')
            if uptime_info:
                total_seconds = float(uptime_info.split()[0])
                days = int(total_seconds // (24 * 3600))
                hours = int((total_seconds % (24 * 3600)) // 3600)
                minutes = int((total_seconds % 3600) // 60)
                seconds = int(total_seconds % 60)
                uptime_str = f"{days} dias, {hours} horas, {minutes} minutos, {seconds} segundos"
                print(f"Tempo de atividade do sistema: {uptime_str}")
                return uptime_str
            return None
        except Exception as e:
            print(f"Erro ao obter tempo de atividade do sistema: {e}")
            return None

    def get_cpu_info(self):
        try:
            cpu_info_raw = self._read_file('/proc/cpuinfo')
            if cpu_info_raw:
                cpu_model = "N/A"
                num_cores = 0
                for line in cpu_info_raw.splitlines():
                    if "model name" in line:
                        cpu_model = line.split(":")[1].strip()
                    if "cpu cores" in line:
                        num_cores = int(line.split(":")[1].strip())
                print(f"Modelo da CPU: {cpu_model}, Núcleos: {num_cores}")
                return {"model": cpu_model, "cores": num_cores}
            return None
        except Exception as e:
            print(f"Erro ao obter informações da CPU: {e}")
            return None

    def get_memory_info(self):
        try:
            mem_info_raw = self._read_file('/proc/meminfo')
            if mem_info_raw:
                mem_total = "N/A"
                mem_free = "N/A"
                for line in mem_info_raw.splitlines():
                    if "MemTotal:" in line:
                        mem_total = line.split(":")[1].strip()
                    if "MemFree:" in line:
                        mem_free = line.split(":")[1].strip()
                print(f"Memória Total: {mem_total}, Memória Livre: {mem_free}")
                return {"total": mem_total, "free": mem_free}
            return None
        except Exception as e:
            print(f"Erro ao obter informações da memória: {e}")
            return None

    def get_disk_usage(self, path="/"):
        try:
            result = subprocess.run(["df", "-h", path], capture_output=True, text=True, check=True)
            output_lines = result.stdout.strip().split('\n')
            if len(output_lines) > 1:
                header = output_lines[0].split()
                data = output_lines[1].split()
                disk_info = dict(zip(header, data))
                print(f"Uso de disco para {path}: {disk_info}")
                return disk_info
            return None
        except subprocess.CalledProcessError as e:
            print(f"Erro ao obter uso de disco para {path}: {e.stderr}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao obter uso de disco: {e}")
            return None

    def get_network_interfaces(self):
        try:
            result = subprocess.run(["ip", "-brief", "addr"], capture_output=True, text=True, check=True)
            interfaces = []
            for line in result.stdout.strip().split('\n'):
                parts = line.split()
                if len(parts) >= 3:
                    interface_name = parts[0]
                    state = parts[1]
                    ip_addresses = parts[2:]
                    interfaces.append({"name": interface_name, "state": state, "ips": ip_addresses})
            print(f"Interfaces de rede: {interfaces}")
            return interfaces
        except subprocess.CalledProcessError as e:
            print(f"Erro ao obter interfaces de rede: {e.stderr}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao obter interfaces de rede: {e}")
            return None

if __name__ == "__main__":
    integrator = SystemAPIIntegrator()

    print("\n--- Testando informações do Kernel ---")
    integrator.get_kernel_version()

    print("\n--- Testando tempo de atividade do sistema ---")
    integrator.get_uptime()

    print("\n--- Testando informações da CPU ---")
    integrator.get_cpu_info()

    print("\n--- Testando informações da Memória ---")
    integrator.get_memory_info()

    print("\n--- Testando uso de disco ---")
    integrator.get_disk_usage("/")

    print("\n--- Testando interfaces de rede ---")
    integrator.get_network_interfaces()

