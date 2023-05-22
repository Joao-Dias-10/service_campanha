import os
import shutil
import subprocess
import time
import uuid
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import psutil
import pandas as pd
import mysql.connector
from  mysql.connector import Error
import win32com.client as client

dir = 'D:/service_campanha'
os.chdir(dir)

app = Flask(__name__)

@app.route('/')
def home_page():
    campanhas = []  
    try:
        con = mysql.connector.connect (host='localhost', database='qualipoints',
        user='root', password= 'devmis@1')
        consulta_sql ="SELECT * FROM campanha;"
        cursor = con.cursor()
        cursor.execute(consulta_sql)
        linhas= cursor.fetchall()
        print ("  ✔️  Número total de registros retornados:", cursor.rowcount)
        for linha in linhas:
            campanhas.append(linha[0])
    except Error as erro:
        print("Erro ao acessar tabela MysQL", erro)
    finally:
        if(con.is_connected()):
            con.close()
            cursor.close()
            print("  ✔️  Conexäo ao MysQL encerrada")

           
    return render_template('index.html', campanhas=campanhas)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():

    # gerar um UUID-4
    id_unico = uuid.uuid4()

    # converter para string
    id_unico_str = str(id_unico)

    retorno = 'Ocorreu um erro au fazer o upload  do arquivo!'
    if request.method == 'POST':
        campanha_id_ = request.form['campanha_id']
        Campanha_id_now = [campanha_id_]
        file = request.files['file']
        filename = secure_filename(file.filename)
        new_filename = campanha_id_ + '_' +'tabela_pontos_usuario' + id_unico_str +'.xlsx'
        file.save(os.path.join(rf'{dir}/uploads/verificacao', new_filename))
        try:
            df = pd.read_excel(rf'{dir}/uploads/verificacao/{ new_filename}')
            coluna = df['MATRICULA_OPERADOR']
            a = coluna.tolist()
            coluna = df['INDICADOR']
            b = coluna.tolist()
            coluna = df['META']
            c = coluna.tolist()
            a.clear()
            b.clear()
            c.clear()
            shutil.move(rf'{dir}/uploads/verificacao/{ new_filename}',rf'{dir}/uploads/upload_usuario/{ new_filename}')

            
            retorno = 'Tabela de pontos inserida!'
            # rota_robo = 'campanha.py'
            # processo =  subprocess.Popen(f'start cmd /k "cd {dir} && {rota_robo}"', shell=True)


            # #Aqui tem que bota todos os nomes das listas
            # lista_de_tuplas = list(zip(Campanha_id_now))
            # # converte uma lista de tuplas num DataFrame
            # df = pd.DataFrame(lista_de_tuplas, columns=['Campanha_id_now'])
            # df.to_excel(rf'uploads/Campanha_id_recebida.xlsx') 

        
        except:
            os.remove(rf'{dir}/uploads/verificacao/{ new_filename}')
            retorno = 'Tabela inserida, está fora do padrão permitido!'




       
    return render_template('index.html', retorno=retorno)

@app.route('/download')
def download_file():

    path = (os.path.join('uploads', 'base_modelo.xlsx'))
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True,host='10.64.146.74', port=5000)
