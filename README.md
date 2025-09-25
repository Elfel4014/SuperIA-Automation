# SuperIA: Automação de PC com Controle Total (Windows/Linux)

## Visão Geral

A SuperIA é uma solução de automação robusta e multiplataforma projetada para gerenciar e automatizar tarefas complexas em ambientes Windows e Linux. Desenvolvida com foco em modularidade, extensibilidade e independência de serviços externos, a SuperIA oferece controle total sobre operações de sistema, manipulação de registro, execução de scripts avançados e automação de aplicativos Office.

## Arquitetura

A arquitetura da SuperIA é dividida em módulos principais, cada um responsável por uma área específica de automação. O **Core Automation Engine** orquestra as tarefas e a comunicação entre os módulos. Os módulos específicos incluem:

*   **Módulo de Automação Windows:** Gerencia o Registro do Windows, processos e integrações de API do sistema.
*   **Módulo de Automação Linux:** Lida com shell scripting avançado, gerenciamento de processos e integração de API do sistema.
*   **Módulo de Automação Office:** Automatiza tarefas em aplicativos como Word, Excel e PowerPoint.
*   **Módulo de Cenários Empresariais:** Implementa fluxos de trabalho complexos para casos de uso reais.

Para uma visão detalhada da arquitetura, consulte o arquivo `arquitetura_superia.md`.

## Funcionalidades Principais

*   **Manipulação do Registro do Windows:** Criação, leitura, modificação e exclusão de chaves e valores de registro.
*   **Shell Scripting Linux Avançado:** Execução e gerenciamento de scripts Bash complexos para administração de sistema.
*   **Gerenciamento de Processos:** Iniciar, parar, monitorar e obter informações detalhadas sobre processos em ambos os sistemas operacionais.
*   **Automação Office:** Criação, leitura e modificação de documentos Word, planilhas Excel e apresentações PowerPoint.
*   **Integração de APIs do Sistema:** Acesso a funcionalidades de baixo nível do sistema operacional para informações e controle avançados.

## Cenários de Uso

A SuperIA pode ser aplicada em diversos cenários empresariais, incluindo:

*   **Provisionamento e Configuração de Servidores:** Automatização da instalação e configuração de novos servidores.
*   **Monitoramento e Resposta a Incidentes:** Detecção e resposta automática a problemas de sistema.
*   **Geração Automatizada de Relatórios:** Criação de relatórios periódicos de saúde do sistema e auditoria.
*   **Gerenciamento de Usuários e Permissões:** Automação da gestão de contas e permissões.
*   **Orquestração de Aplicações:** Gerenciamento do ciclo de vida de aplicações, desde a implantação até a atualização.

Para uma descrição detalhada dos cenários e casos de uso, consulte o arquivo `use_cases/business_scenarios.md`.

## Estrutura do Projeto

```
SuperIA/
├── windows_automation/
│   ├── registry_manager.py
│   ├── registry_manager.ps1
│   ├── process_manager.py
│   ├── process_manager.ps1
│   ├── system_api_integrator.py
│   └── main_windows_automation.py
├── linux_automation/
│   ├── process_manager.py
│   ├── shell_script_executor.py
│   ├── system_api_integrator.py
│   └── main_linux_automation.py
├── office_automation/
│   ├── word_automator.py
│   ├── excel_automator.py
│   ├── powerpoint_automator.py
│   └── main_office_automation.py
├── use_cases/
│   └── business_scenarios.md
├── arquitetura_superia.md
├── arquitetura_superia.png
└── README.md
```

## Instalação e Uso

**Pré-requisitos:**

*   Python 3.x
*   `pip` (gerenciador de pacotes Python)
*   Para automação Windows: PowerShell, `pywin32` (para `system_api_integrator.py` e `process_manager.ps1`, `registry_manager.ps1`)

**Instalação de Dependências Python:**

```bash
pip install psutil python-docx openpyxl python-pptx Pillow
```

**Como Executar os Exemplos:**

Cada módulo possui um arquivo `main_*.py` que demonstra suas funcionalidades. Para executá-los:

```bash
# Para automação Windows (em um ambiente Windows)
python SuperIA/windows_automation/main_windows_automation.py

# Para automação Linux
python SuperIA/linux_automation/main_linux_automation.py

# Para automação Office
python SuperIA/office_automation/main_office_automation.py
```

**Nota:** Os scripts de automação Windows que dependem de `winreg` ou `pywin32` foram desenvolvidos para serem executados em um ambiente Windows. Mocks foram implementados para permitir a execução parcial em ambientes Linux para fins de demonstração da estrutura do código. Os scripts PowerShell (`.ps1`) também devem ser executados em um ambiente Windows.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para melhorias, correções de bugs ou novas funcionalidades.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. (A ser criado)

