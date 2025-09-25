import os
import sys
import time

# Adicionar o diretório atual ao PATH para que os módulos possam ser importados
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from process_manager import ProcessManager
from shell_script_executor import ShellScriptExecutor
from system_api_integrator import SystemAPIIntegrator

def main():
    print("\n=== Testando Módulos de Automação Linux ===\n")

    # --- Testando ProcessManager ---
    print("\n--- Testando ProcessManager ---")
    proc_manager = ProcessManager()

    print("Listando os 5 primeiros processos:")
    all_processes = proc_manager.list_processes()
    for p in all_processes[:5]:
        print(p)

    print("Procurando por processos \'bash\':")
    bash_processes = proc_manager.find_process_by_name("bash")
    for p in bash_processes[:5]:
        print(p)

    print("Iniciando \'sleep 5\' em segundo plano...")
    pid, _ = proc_manager.start_process("sleep 5")
    if pid:
        print(f"Processo sleep iniciado com PID: {pid}")
        time.sleep(2)
        print(f"Tentando parar processo com PID: {pid}")
        proc_manager.stop_process(pid)

    print("Obtendo informações do processo com PID 1:")
    process_info = proc_manager.get_process_info(1)
    if process_info:
        print(process_info)

    print(f"Uso de CPU do sistema: {proc_manager.get_system_cpu_usage()}% ")
    print(f"Uso de Memória do sistema: {proc_manager.get_system_memory_usage()}% ")

    # --- Testando ShellScriptExecutor ---
    print("\n--- Testando ShellScriptExecutor ---")
    script_executor = ShellScriptExecutor()

    print("Executando script simples:")
    script_content_simple = """
#!/bin/bash
echo "Hello from SuperIA Linux Shell!"
ls -l /tmp
"""
    try:
        result = script_executor.execute_script(script_content_simple)
        print("Saída:\n", result.stdout)
    except Exception as e:
        print(f"Erro ao executar script simples: {e}")

    print("Executando comando direto:")
    try:
        result = script_executor.execute_command(["echo", "Comando direto executado!"])
        print("Saída:\n", result.stdout)
    except Exception as e:
        print(f"Erro ao executar comando direto: {e}")

    # --- Testando SystemAPIIntegrator ---
    print("\n--- Testando SystemAPIIntegrator ---")
    api_integrator = SystemAPIIntegrator()

    api_integrator.get_kernel_version()
    api_integrator.get_uptime()
    api_integrator.get_cpu_info()
    api_integrator.get_memory_info()
    api_integrator.get_disk_usage("/")
    api_integrator.get_network_interfaces()

if __name__ == "__main__":
    main()
