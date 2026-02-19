"""
PDF Extractor – Ferramenta de extração de texto de PDFs
DocuMaster Solutions
Autor: Seu Nome
"""
 
import argparse
import os
from pypdf import PdfReader
 
 
def validar_arquivo(caminho):
    """Verifica se o arquivo existe."""
    if not os.path.exists(caminho):
        raise FileNotFoundError("Arquivo inexistente.")
 
 
def obter_paginas(paginas_str, total_paginas):
    """
    Converte string como '1-3,5' em lista de índices válidos.
    """
    paginas = set()
 
    try:
        partes = paginas_str.split(",")
 
        for parte in partes:
            if "-" in parte:
                inicio, fim = map(int, parte.split("-"))
                for p in range(inicio, fim + 1):
                    paginas.add(p - 1)
            else:
                paginas.add(int(parte) - 1)
 
        for p in paginas:
            if p < 0 or p >= total_paginas:
                raise ValueError("Página fora do intervalo válido.")
 
        return sorted(paginas)
 
    except ValueError:
        raise ValueError("Formato inválido. Use exemplo: 1-3,5")
 
 
def extrair_texto(caminho_pdf, paginas=None):
    """
    Extrai texto do PDF.
    """
    reader = PdfReader(caminho_pdf)
 
    if reader.is_encrypted:
        raise Exception("PDF criptografado.")
 
    total_paginas = len(reader.pages)
 
    if paginas is None:
        paginas = range(total_paginas)
 
    texto_final = ""
 
    for numero in paginas:
        pagina = reader.pages[numero]
        texto = pagina.extract_text()
 
        if texto:
            texto_final += f"\n--- Página {numero + 1} ---\n"
            texto_final += texto
        else:
            print(f"Aviso: Página {numero + 1} sem texto extraível.")
 
    if not texto_final.strip():
        raise Exception("PDF não contém texto extraível.")
 
    return texto_final
 
 
def salvar_arquivo(texto, nome_saida):
    """Salva texto em arquivo UTF-8."""
    with open(nome_saida, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)
 
 
def main():
    parser = argparse.ArgumentParser(
        description="PDF Extractor – DocuMaster Solutions"
    )
 
    parser.add_argument("--input", required=True, help="Arquivo PDF de entrada")
    parser.add_argument("--pages", help="Páginas específicas (ex: 1-3,5)")
    parser.add_argument("--output", help="Arquivo .txt de saída")
 
    args = parser.parse_args()
 
    try:
        validar_arquivo(args.input)
 
        reader_temp = PdfReader(args.input)
        total_paginas = len(reader_temp.pages)
 
        if args.pages:
            lista_paginas = obter_paginas(args.pages, total_paginas)
        else:
            lista_paginas = None
 
        texto = extrair_texto(args.input, lista_paginas)
 
        if args.output:
            salvar_arquivo(texto, args.output)
            print(f"Texto salvo em {args.output}")
        else:
            print(texto)
 
    except Exception as erro:
        print(f"Erro: {erro}")
 
 
if __name__ == "__main__":
    main()
 