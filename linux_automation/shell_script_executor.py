import subprocess
import os

class ShellScriptExecutor:
    def __init__(self):
        pass

    def execute_script(self, script_content, shell_name="bash", capture_output=True, check_errors=True):
        """
        Executa um shell script e retorna sua saída.

        Args:
            script_content (str): O conteúdo do script a ser executado.
            shell_name (str): O shell a ser usado (ex: "bash", "sh").
            capture_output (bool): Se a saída (stdout e stderr) deve ser capturada.
            check_errors (bool): Se deve levantar uma exceção CalledProcessError para códigos de saída não-zero.

        Returns:
            subprocess.CompletedProcess: Objeto contendo stdout, stderr e returncode.
        """
        try:
            # Salva o script em um arquivo temporário
            temp_script_path = "/tmp/temp_superia_script.sh"
            with open(temp_script_path, "w") as f:
                f.write(script_content)
            os.chmod(temp_script_path, 0o755) # Torna o script executável

            command = [shell_name, temp_script_path]

            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                check=check_errors,
                encoding="utf-8"
            )
            os.remove(temp_script_path) # Remove o arquivo temporário
            return result
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar script: {e}")
            print(f"Saída padrão: {e.stdout}")
            print(f"Saída de erro: {e.stderr}")
            os.remove(temp_script_path) # Remove o arquivo temporário
            raise
        except FileNotFoundError:
            print(f"Shell '{shell_name}' não encontrado. Certifique-se de que está instalado e no PATH.")
            os.remove(temp_script_path) # Remove o arquivo temporário
            raise
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            os.remove(temp_script_path) # Remove o arquivo temporário
            raise

    def execute_command(self, command, shell=False, capture_output=True, check_errors=True):
        """
        Executa um comando diretamente.

        Args:
            command (str or list): O comando a ser executado. Pode ser uma string (com shell=True) ou uma lista de argumentos.
            shell (bool): Se o comando deve ser executado através do shell.
            capture_output (bool): Se a saída (stdout e stderr) deve ser capturada.
            check_errors (bool): Se deve levantar uma exceção CalledProcessError para códigos de saída não-zero.

        Returns:
            subprocess.CompletedProcess: Objeto contendo stdout, stderr e returncode.
        """
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=capture_output,
                text=True,
                check=check_errors,
                encoding="utf-8"
            )
            return result
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar comando: {e}")
            print(f"Saída padrão: {e.stdout}")
            print(f"Saída de erro: {e.stderr}")
            raise
        except FileNotFoundError:
            print(f"Comando não encontrado: {command}")
            raise
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            raise

if __name__ == "__main__":
    executor = ShellScriptExecutor()

    print("\n--- Testando execução de script simples ---")
    script_content_simple = """
#!/bin/bash
echo "Hello from SuperIA Linux Shell!"
ls -l /tmp
"""
    try:
        result = executor.execute_script(script_content_simple)
        print("Saída do script simples:")
        print(result.stdout)
    except Exception:
        print("Falha no teste de script simples.")

    print("\n--- Testando execução de script com erro ---")
    script_content_error = """
#!/bin/bash
echo "Este script vai falhar."
exit 1
"""
    try:
        result = executor.execute_script(script_content_error)
        print("Saída do script com erro (não deveria ser vista se check_errors=True):")
        print(result.stdout)
    except subprocess.CalledProcessError:
        print("Capturado erro esperado na execução do script.")
    except Exception:
        print("Falha inesperada no teste de script com erro.")

    print("\n--- Testando execução de comando direto ---")
    try:
        result = executor.execute_command(["echo", "Comando direto executado!"])
        print("Saída do comando direto:")
        print(result.stdout)
    except Exception:
        print("Falha no teste de comando direto.")

    print("\n--- Testando execução de comando com shell=True ---")
    try:
        result = executor.execute_command("df -h | grep /dev/sd", shell=True)
        print("Saída do comando com shell=True:")
        print(result.stdout)
    except Exception:
        print("Falha no teste de comando com shell=True.")

