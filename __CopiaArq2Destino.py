import os
import shutil

def copiar_pdf_para_diretorio(origem_pdf, destino_diretorio, especializada):
    """
    Copia um arquivo PDF para um diretório específico, acrescentando um tipo ao nome do arquivo.

    Argumentos:
    origem_pdf (str): Caminho do arquivo PDF de origem.
    destino_diretorio (str): Caminho do diretório de destino.
    tipo (str): Tipo a ser acrescentado ao nome do arquivo.
    """
    # Verifica se o arquivo PDF de origem existe
    if not os.path.isfile(origem_pdf):
        print(f"O arquivo {origem_pdf} não existe.")
        return
    
    # Verifica se o destino é um diretório válido
    if not os.path.isdir(destino_diretorio):
        print(f"O diretório {destino_diretorio} não existe.")
        return

    try:
        # Extrai o nome do arquivo PDF
        nome_arquivo, extensao = os.path.splitext(os.path.basename(origem_pdf))
        
        # Novo nome do arquivo com o tipo acrescentado
        novo_nome_arquivo = f"{especializada}_{nome_arquivo}{extensao}"
        
        # Copia o arquivo PDF para o diretório de destino com o novo nome
        shutil.copy(origem_pdf, os.path.join(destino_diretorio, novo_nome_arquivo))
        print(f"Arquivo PDF copiado com sucesso para {os.path.join(destino_diretorio, novo_nome_arquivo)}")
    except Exception as e:
        print(f"Ocorreu um erro ao copiar o arquivo PDF: {str(e)}")

# Exemplo de uso da função
#if __name__ == "__main__":
#     # Caminho do arquivo PDF de origem
#     origem_pdf = "XPTO.pdf"
#     
#     # Diretório de destino
#     destino_diretorio = "DirTrein"
#     
#     # Tipo a ser acrescentado ao nome do arquivo
#     especializada = "PPE"
    
    # Chama a função para copiar o PDF para o diretório específico com o tipo acrescentado
copiar_pdf_para_diretorio(origem_pdf, "DirTrein", especializada)

    #origem pdf= input de pdf, input de string especializada
    #'PAS'
    # 'PDA' 
    # 'PPE' 
    # 'PSE' 
    # 'PTR' 
    # 'PUMA'
    # 'PTA' 