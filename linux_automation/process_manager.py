import psutil
import subprocess
import os

class ProcessManager:
    def __init__(self):
        pass

    def list_processes(self):
        processes = []
        for proc in psutil.process_iter(["pid", "name", "username", "status"]):
            processes.append(proc.info)
        return processes

    def find_process_by_name(self, name):
        processes = []
        for proc in psutil.process_iter(["pid", "name", "username", "status"]):
            if name.lower() in proc.info["name"].lower():
                processes.append(proc.info)
        return processes

    def get_process_info(self, pid):
        try:
            process = psutil.Process(pid)
            return process.as_dict(attrs=["pid", "name", "username", "status", "cpu_percent", "memory_percent", "cmdline", "create_time"])
        except psutil.NoSuchProcess:
            return None
        except Exception as e:
            print(f"Erro ao obter informações do processo com PID {pid}: {e}")
            return None

    def start_process(self, command, shell=False, wait=False):
        try:
            if shell:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            else:
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            print(f"Processo \'{command}\' iniciado com PID: {process.pid}")
            if wait:
                stdout, stderr = process.communicate()
                print(f"Saída do processo (PID {process.pid}):\n{stdout}")
                if stderr:
                    print(f"Erro do processo (PID {process.pid}):\n{stderr}")
                return process.pid, process.returncode
            return process.pid, None
        except Exception as e:
            print(f"Erro ao iniciar processo \'{command}\' : {e}")
            return None, None

    def stop_process(self, pid):
        try:
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=5) # Espera o processo terminar por até 5 segundos
            print(f"Processo com PID {pid} terminado.")
            return True
        except psutil.NoSuchProcess:
            print(f"Processo com PID {pid} não encontrado.")
            return False
        except psutil.TimeoutExpired:
            print(f"Processo com PID {pid} não terminou, forçando o encerramento.")
            process.kill()
            process.wait()
            return True
        except Exception as e:
            print(f"Erro ao terminar processo com PID {pid}: {e}")
            return False

    def get_system_cpu_usage(self, interval=1):
        return psutil.cpu_percent(interval=interval)

    def get_system_memory_usage(self):
        return psutil.virtual_memory().percent

if __name__ == "__main__":
    manager = ProcessManager()

    print("\n--- Listando alguns processos ---")
    all_processes = manager.list_processes()
    for p in all_processes[:5]:
        print(p)

    print("\n--- Encontrando processos por nome (ex: \'bash\') ---")
    bash_processes = manager.find_process_by_name("bash")
    for p in bash_processes[:5]:
        print(p)

    print("\n--- Iniciando e parando um processo (ex: sleep) ---")
    print("Iniciando 'sleep 10' em segundo plano...")
    pid, _ = manager.start_process("sleep 10")
    if pid:
        print(f"Processo sleep iniciado com PID: {pid}")
        import time
        time.sleep(2)
        print(f"Tentando parar processo com PID: {pid}")
        manager.stop_process(pid)

    print("\n--- Obtendo informações de um processo (ex: PID 1) ---")
    process_info = manager.get_process_info(1)
    if process_info:
        print(f"Informações do PID 1: {process_info}")
    else:
        print("Não foi possível obter informações do PID 1.")

    print("\n--- Uso de CPU e Memória do Sistema ---")
    print(f"Uso de CPU: {manager.get_system_cpu_usage()}% ")
    print(f"Uso de Memória: {manager.get_system_memory_usage()}% ")

