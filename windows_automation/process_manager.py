import psutil
import subprocess

class ProcessManager:
    def __init__(self):
        pass

    def list_processes(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            processes.append(proc.info)
        return processes

    def find_process_by_name(self, name):
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            if name.lower() in proc.info['name'].lower():
                processes.append(proc.info)
        return processes

    def get_process_info(self, pid):
        try:
            process = psutil.Process(pid)
            return process.as_dict()
        except psutil.NoSuchProcess:
            return None

    def start_process(self, command):
        try:
            process = subprocess.Popen(command, shell=True)
            print(f"Processo '{command}' iniciado com PID: {process.pid}")
            return process.pid
        except Exception as e:
            print(f"Erro ao iniciar processo '{command}': {e}")
            return None

    def stop_process(self, pid):
        try:
            process = psutil.Process(pid)
            process.terminate()
            print(f"Processo com PID {pid} terminado.")
            return True
        except psutil.NoSuchProcess:
            print(f"Processo com PID {pid} não encontrado.")
            return False
        except Exception as e:
            print(f"Erro ao terminar processo com PID {pid}: {e}")
            return False

if __name__ == "__main__":
    manager = ProcessManager()

    print("\n--- Listando alguns processos ---")
    all_processes = manager.list_processes()
    for p in all_processes[:5]:
        print(p)

    print("\n--- Encontrando processos por nome (ex: 'svchost') ---")
    svchost_processes = manager.find_process_by_name("svchost")
    for p in svchost_processes[:5]:
        print(p)

    print("\n--- Iniciando e parando um processo (ex: notepad.exe) ---")
    # Este exemplo é mais aplicável em um ambiente Windows real
    # pid = manager.start_process("notepad.exe")
    # if pid:
    #     time.sleep(2)
    #     manager.stop_process(pid)

    print("\n--- Obtendo informações de um processo (ex: PID 1) ---")
    # PID 1 é diferente em Windows e Linux, este é um exemplo genérico
    try:
        process_info = manager.get_process_info(1)
        if process_info:
            print(f"Informações do PID 1: {process_info['name']}, {process_info['status']}")
    except Exception as e:
        print(f"Não foi possível obter informações do PID 1: {e}")

