import os
import sys

# Adicionar o diretório atual ao PATH para que os módulos possam ser importados
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from word_automator import WordAutomator
from excel_automator import ExcelAutomator
from powerpoint_automator import PowerPointAutomator

def main():
    print("\n=== Testando Módulos de Automação Office ===\n")

    # --- Testando WordAutomator ---
    print("\n--- Testando WordAutomator ---")
    word_automator = WordAutomator()
    test_doc = "test_superia_word.docx"

    word_automator.create_document(test_doc, "Relatório de Teste SuperIA", "Este é o relatório inicial.")
    word_automator.add_paragraph_to_document(test_doc, "Um novo parágrafo com informações adicionais.")
    word_automator.add_heading_to_document(test_doc, "Seção 2: Dados Importantes")

    headers = ["Item", "Quantidade", "Preço"]
    data = [
        ["Produto A", 10, 25.50],
        ["Produto B", 5, 100.00]
    ]
    word_automator.add_table_to_document(test_doc, headers, data)
    print(f"Verifique o arquivo \'{test_doc}\' para ver o resultado.\n")

    # --- Testando ExcelAutomator ---
    print("\n--- Testando ExcelAutomator ---")
    excel_automator = ExcelAutomator()
    test_excel = "test_superia_excel.xlsx"
    test_sheet = "Relatório"

    excel_automator.create_workbook(test_excel, test_sheet)
    data_with_headers = [
        {"Produto": "Teclado", "Quantidade": 5, "PrecoUnitario": 150.00},
        {"Produto": "Mouse", "Quantidade": 10, "PrecoUnitario": 75.00},
        {"Produto": "Monitor", "Quantidade": 2, "PrecoUnitario": 1200.00}
    ]
    excel_automator.write_data_to_sheet(test_excel, test_sheet, data_with_headers, include_headers=True)
    excel_automator.add_formula(test_excel, test_sheet, "D1", "Total")
    excel_automator.add_formula(test_excel, test_sheet, "D2", "=B2*C2")
    excel_automator.add_formula(test_excel, test_sheet, "D3", "=B3*C3")
    excel_automator.add_formula(test_excel, test_sheet, "D4", "=B4*C4")
    excel_automator.add_formula(test_excel, test_sheet, "D5", "=SUM(D2:D4)")

    read_data = excel_automator.read_data_from_sheet(test_excel, test_sheet)
    if read_data:
        print("Dados lidos da planilha:")
        for row in read_data:
            print(row)
    print(f"Verifique o arquivo \'{test_excel}\' para ver o resultado.\n")

    # --- Testando PowerPointAutomator ---
    print("\n--- Testando PowerPointAutomator ---")
    powerpoint_automator = PowerPointAutomator()
    test_pptx = "test_superia_presentation.pptx"

    powerpoint_automator.create_presentation(test_pptx, "Demonstração SuperIA", "Capacidades de Automação")
    content = [
        "Manipulação do Registro do Windows",
        "Shell Scripting Linux Avançado",
        "Automação Office Completa",
        "Gerenciamento de Processos do Sistema",
        "Integração de APIs do Sistema"
    ]
    powerpoint_automator.add_title_and_content_slide(test_pptx, "Funcionalidades Principais", content)

    # Criar imagem dummy para teste
    try:
        from PIL import Image
        img = Image.new('RGB', (60, 30), color = 'blue')
        img.save("dummy_image.png")
        print("Imagem dummy criada: dummy_image.png")
        powerpoint_automator.add_picture_slide(test_pptx, "Exemplo de Imagem", "dummy_image.png")
        os.remove("dummy_image.png")
        print("Imagem dummy removida.")
    except Exception as e:
        print(f"Erro ao criar ou adicionar imagem dummy: {e}")

    print(f"Verifique o arquivo \'{test_pptx}\' para ver o resultado.\n")

if __name__ == "__main__":
    main()
