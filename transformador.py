# Importing required modules
import pandas as pd
import PyPDF2
import os

#função para achar o campo de ciclo do BM
def find_ciclo(text_param):
    patternline2 = text_param[0].split('\n')
    patternline3 = patternline2[1].split()
    ciclo = patternline3[13]
    
    return ciclo

#função para encontrar lista de valores por contrato
def find_contrato(text_param):
    patternline = text_param[3].split('\n')
    contratos = patternline[3]
    contratos_list = contratos.split()
    del(contratos_list[::2])
    del(contratos_list[-1])
    
    return contratos_list


#criando dataframe vazio
lista_colunas = ['nome','ciclo', 'contrato', 'valor']
df = pd.DataFrame(data=None, columns=lista_colunas)

#definindo pasta onde os arquivos irão ficar por padrão
pasta = './produção'
#rastreando todos os arquivos dentro da pasta padrão
for diretorio, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        
        #configurando a leitura linha por linha de cada pdf
        caminho = 'produção/' + arquivo
        pdfFileObj = open(caminho,'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pageObj = pdfReader.getPage(0)
        text = pageObj.extractText().split("  ")
        
        #separandoo dados das linhas dentro do df
        nome = arquivo[:-4]
        ciclo = find_ciclo(text)
        contratos_valor = find_contrato(text)
        contratos = ['Engenharia Industrial','Porto', 'Facilities', 'Arcadis', 'Equatorial', 'FLSMIDTH']
        
        #criando uma linha para cada 
        for i in range(len(contratos)):
            new_row = ([nome, ciclo, contratos[i], contratos_valor[i]])
            df.loc[len(df)] = new_row
            
            
df.to_excel('database.xlsx', index = False)       
        