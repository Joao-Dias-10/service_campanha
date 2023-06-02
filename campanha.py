import json
import shutil
import subprocess
import os
import time
import pandas as pd
import mysql.connector
from  mysql.connector import Error
import win32com.client as client
# pip install pyjwt
import jwt
import operator
import datetime



matricula_operador = []
pontos = []
ultima_atualizacao = []


id_campanha = []
variavel_json = []
ultimo_input = []
criado_por = []
prazo = []

decoded = 0


dir = 'D:\service_campanha'



def CAMPANHA_RECEBIDA():

    df = pd.read_excel(rf'{dir}\uploads\Campanha_id_recebida.xlsx')
    coluna = df['Campanha_id_now']
    Campanha_id_recebida = coluna.tolist()

    return int(Campanha_id_recebida[0])

def BUSCAR_DADOS_DO_BANCO_OPERADOSRES(matricula_operador,pontos,ultima_atualizacao):
    
    print("\n  ✔️  Buscando  no banco!")
    try:
        con = mysql.connector.connect (host='localhost', database='qualipoints',
        user='root', password= '')
        consulta_sql ="SELECT * FROM pontos;"
        cursor = con.cursor()
        cursor.execute(consulta_sql)
        linhas= cursor.fetchall()
        print ("  ✔️  Número total de registros retornados:", cursor.rowcount)
        for linha in linhas:
            matricula_operador.append(linha[0])
            pontos.append(linha[1])
            ultima_atualizacao.append(linha[2])
    except Error as erro:
        print("Erro ao acessar tabela MysQL", erro)
    finally:
        if(con.is_connected()):
            con.close()
            cursor.close()
            print("  ✔️  Conexäo ao MysQL encerrada")
    try:
      print(f'\n\n{matricula_operador}')
    except:
       pass

def BUSCAR_DADOS_DO_BANCO__INDICADORES(id_campanha,variavel_json,ultimo_input,criado_por,prazo):
     
    print("\n  ✔️  Buscando  no banco!")
    try:
        con = mysql.connector.connect (host='localhost', database='qualipoints',
        user='root', password= '')
        consulta_sql ="SELECT * FROM campanha;"
        cursor = con.cursor()
        cursor.execute(consulta_sql)
        linhas= cursor.fetchall()
        print ("  ✔️  Número total de registros retornados:", cursor.rowcount)
        for linha in linhas:
            id_campanha.append(linha[0])
            variavel_json.append(linha[1])
            ultimo_input.append(linha[2])
            criado_por.append(linha[3])
            prazo.append(linha[4])
    except Error as erro:
        print("Erro ao acessar tabela MysQL", erro)
    finally:
        if(con.is_connected()):
            con.close()
            cursor.close()
            print("  ✔️  Conexäo ao MysQL encerrada")
    try:
      print(f'\n\n{variavel_json}')
    except:
       pass
   
def GERAR_BASE_INDICADORES_E_OPERADORES(matricula_operador,pontos,ultima_atualizacao,     id_campanha,variavel_json,ultimo_input,criado_por,prazo):
    #Aqui tem que bota todos os nomes das listas
    lista_de_tuplas = list(zip(matricula_operador,pontos,ultima_atualizacao))
    # converte uma lista de tuplas num DataFrame
    df = pd.DataFrame(lista_de_tuplas, columns=['matricula_operador','pontos','ultima_atualizacao'])
    df.to_excel(rf'{dir}\uploads\tabela_pontos_banco.xlsx') 


    #Aqui tem que bota todos os nomes das listas
    lista_de_tuplas = list(zip(id_campanha,variavel_json,ultimo_input,criado_por,prazo))
    # converte uma lista de tuplas num DataFrame
    df = pd.DataFrame(lista_de_tuplas, columns=['id_campanha','variavel_json','ultimo_input','criado_por','prazo'])
    df.to_excel(rf'{dir}\uploads\tabela_campanha.xlsx') 

def SCORE_INDICADOR(id_campanha_user):



    df = pd.read_excel(rf'{dir}\uploads\tabela_campanha.xlsx')
    coluna = df['id_campanha']
    id_campanha_xlsx = coluna.tolist()

    coluna = df['variavel_json']
    json_xlsx = coluna.tolist()

    coluna = df['ultimo_input']
    ultimo_input_xlsx = coluna.tolist()

    coluna = df['criado_por']
    criado_por_xlsx = coluna.tolist()

    coluna = df['prazo']
    prazo_xlsx = coluna.tolist()

    if id_campanha_user in id_campanha_xlsx:

        index = id_campanha_xlsx.index(id_campanha_user)
        jwt_token = rf'{str(json_xlsx[index]).strip()}'
       
        decoded = jwt.decode(jwt_token, algorithms=["HS256"], options={"verify_signature": False})

        return decoded

def CALCULO_LINHA_TABELA_RECEBIDA(id_campanha_user):

    decoded = SCORE_INDICADOR(id_campanha_user)

    df = pd.read_excel(rf'{dir}\uploads\tabela_pontos_usuario.xlsx')

    coluna = df['MATRICULA_OPERADOR']
    matricula_operador_user = coluna.tolist()

    coluna = df['INDICADOR']
    indicador_operador_user = coluna.tolist()

    coluna = df['META']
    meta_operador_user = coluna.tolist()


    df = pd.read_excel(rf'{dir}\uploads\tabela_pontos_banco.xlsx')

    coluna = df['matricula_operador']
    matricula_operador_banco_xlsx = coluna.tolist()

    coluna = df['pontos']
    pontos_banco_xlsx = coluna.tolist()

    coluna = df['ultima_atualizacao']
    ultima_atualizacao_banco_xlsx = coluna.tolist()

    #Gera dic de valor 0 com as matrículas recebidas
    matricula_operador_user_unico = list(set(matricula_operador_user)) 
    dicionario_matriculas_pontos = dict.fromkeys(matricula_operador_user_unico, 0)
    print(dicionario_matriculas_pontos)
    #Preenche com os pontos já existenres no banco
    index0 = 0
    for matricula000 in matricula_operador_banco_xlsx:
        if matricula000 in dicionario_matriculas_pontos:
            dicionario_matriculas_pontos[matricula000] = pontos_banco_xlsx[index0]
        index0 = index0 + 1
    print(dicionario_matriculas_pontos)
    print('\n\n')


    index = 0
    print(decoded)
    print('\n\n')
    for i in matricula_operador_user:
        if (indicador_operador_user[index]) in decoded:

            indicador1_dict = json.loads(decoded[(indicador_operador_user[index])])
            indicador_meta = indicador1_dict["meta"]
            indicador_pontuacao = indicador1_dict["pontuacao"]
            indicador_comparacao = indicador1_dict["comparacao"]

            # Dicionário com as funções Python correspondentes a cada operador
            operadores = {'>': operator.gt, '<': operator.lt, '>=': operator.ge, '<=': operator.le, '==': operator.eq}

            # Selecionar a função correspondente ao operador desejado
            operador = operadores[indicador1_dict['comparacao']]
            # Fazer a comparação com o valor desejado

            if operador(meta_operador_user[index], indicador1_dict['meta']):
                print(rf'{matricula_operador_user[index]} - {indicador_operador_user[index]}: {indicador_pontuacao}')
                ponto_atual = dicionario_matriculas_pontos[(matricula_operador_user[index])]
                ponto_ganho = indicador_pontuacao
                dicionario_matriculas_pontos[(matricula_operador_user[index])] = ponto_atual + ponto_ganho

            else:
                print(rf'{matricula_operador_user[index]} - {indicador_operador_user[index]}: 0')

        else:
            print(f'A chave {indicador_operador_user[index]} não existe no dicionário "decoded".')
   
        index = index + 1

    print('\n\n')
    print(dicionario_matriculas_pontos)


    df = pd.DataFrame(list(dicionario_matriculas_pontos.items()), columns=['matricula_operador', 'pontos'])
    df['ultima_atualizacao'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Ajuste a ordem das colunas
    df = df[['matricula_operador', 'pontos', 'ultima_atualizacao']]

    # Salve o arquivo Excel
    df.to_excel(rf'{dir}\uploads\tabela_pontos_banco_atualizada.xlsx', index=False)
    print(f'\n\nExcel tabela_pontos_banco_atualizada gerado!')

def UPDATE_BANCO_OPERADOSRES(matricula_operador,pontos,ultima_atualizacao):
    

    df = pd.read_excel(rf'{dir}\uploads\tabela_pontos_banco_atualizada.xlsx')

    coluna = df['matricula_operador']
    matricula_operador_banco_atualizada_xlsx = coluna.tolist()

    coluna = df['pontos']
    pontos_banco_atualizada_xlsx = coluna.tolist()

    coluna = df['ultima_atualizacao']
    ultima_atualizacao_banco_atualizada_xlsx = coluna.tolist()

  
    print("\n  ✔️  Atualizando banco de pontos!")
    try:
        con = mysql.connector.connect (host='localhost', database='qualipoints',
        user='root', password= '')

        index_atualizado = 0
        for matricula_recebida in matricula_operador_banco_atualizada_xlsx:
            m = str(matricula_recebida)
            data000000 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if str(matricula_recebida) in matricula_operador:
                
                consulta_sql = rf"UPDATE `pontos` SET `pontos`='{int(pontos_banco_atualizada_xlsx[index_atualizado])}',`ultima_atualizacao`='{data000000}' WHERE matricula_operador = {m};"
                cursor = con.cursor()
                cursor.execute(consulta_sql) 
                con.commit()
                print(rf'Matrícula: {matricula_recebida} - Data: {ultima_atualizacao_banco_atualizada_xlsx[index_atualizado]} - Pontos: {pontos_banco_atualizada_xlsx[index_atualizado]} atualizada no banco! ')
            else:
                consulta_sql = rf"INSERT INTO `pontos`(`matricula_operador`, `pontos`, `ultima_atualizacao`) VALUES ('{m}','{int(pontos_banco_atualizada_xlsx[index_atualizado])}','{data000000}');"
                cursor = con.cursor()
                cursor.execute(consulta_sql)
                con.commit()
                print(rf'Matrícula: {matricula_recebida} - Data: {ultima_atualizacao_banco_atualizada_xlsx[index_atualizado]} - Pontos: {pontos_banco_atualizada_xlsx[index_atualizado]} inserida no banco!')

            index_atualizado = index_atualizado + 1 
        
    except Error as erro:
        print("Erro ao acessar tabela MysQL", erro)
    finally:
        if(con.is_connected()):
            con.close()
            cursor.close()
            print("  ✔️  Conexäo ao MysQL encerrada")


qtd_verificacao = 0
while True:

    
    qtd_verificacao = qtd_verificacao +1 
    pasta = rf'{dir}\uploads\upload_usuario'
    arquivos = os.listdir(pasta)

    if arquivos:
            primeiro_arquivo = min(arquivos, key=lambda x: os.path.getmtime(os.path.join(pasta, x)))
            print(primeiro_arquivo)
            id_campanha_user = int(primeiro_arquivo[0])
            shutil.move(rf'{pasta}\{primeiro_arquivo}',rf'{dir}\uploads\tabela_pontos_usuario.xlsx')
                        
            BUSCAR_DADOS_DO_BANCO_OPERADOSRES(matricula_operador,pontos,ultima_atualizacao)
            BUSCAR_DADOS_DO_BANCO__INDICADORES(id_campanha,variavel_json,ultimo_input,criado_por,prazo)
            GERAR_BASE_INDICADORES_E_OPERADORES(matricula_operador,pontos,ultima_atualizacao,     id_campanha,variavel_json,ultimo_input,criado_por,prazo)
            CALCULO_LINHA_TABELA_RECEBIDA(id_campanha_user)
            UPDATE_BANCO_OPERADOSRES(matricula_operador,pontos,ultima_atualizacao)
            
            qtd_verificacao = 0
    else:

        print(rf'{qtd_verificacao} - Não há arquivos na pasta.')

    time.sleep(20)


    
# fecha o terminal
os.system('taskkill /F /IM cmd.exe')