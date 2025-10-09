import obd
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
import sqlalchemy as sqla
import re
import psycopg2 as psy
import warnings
warnings.filterwarnings("ignore")


def conectar():

    conn = None
    try:
        load_dotenv()
        conn = psy.connect(
            # passando os parâmetros necessários pegos do .env
            host = os.getenv('HOSTTEST'),
            database = os.getenv('DATABASETESt'),
            user = os.getenv('USER'),
            password = os.getenv('PASSWORDTEST'),
            port = int(os.getenv('PORTTEST')),
        )
    except psy.Error as e:
        print("Erro !")
    finally:
        return conn

def conectarInsert():
    conn = None
    load_dotenv()

    try:
        conn = sqla.create_engine(f"postgresql+psycopg2://{os.getenv('USER')}:{os.getenv('PASSWORDTEST')}@{os.getenv('HOSTTEST')}:{os.getenv('PORTTEST')}/{os.getenv('DATABASETEST')}")
    except sqla.Error as e:
        print("Erro na conexão")
    finally:
        return conn.connect()
    
    
def desconectar(conn):
    if conn != None:
        conn.close()


def efetuarLogin():

    while True:
        while True:
            email=input("Digite o email do motorista: ")
            if re.match(r"^[A-Za-z0-9\.-]+@[a-zA-Z]+\.[A-Za-z\.]+$",email):
                break
            else:
                print("Formato de email ínvalido !")
        senhaDigitada=input("Digite a sua senha: ")

        conexaoBD = conectar().cursor()

        conexaoBD.execute(f"SELECT m.id,m.senha FROM motorista m WHERE m.email=%s",(email,))

        senhaEsperada= conexaoBD.fetchone()


        desconectar(conexaoBD)

        if senhaEsperada:
            if senhaDigitada == senhaEsperada[1]:
                break
            else:
                while True:
                    print("Senha incorreta, digite novamente !")
                    senhaDigitada=input("Digite a sua senha: ")
                    if senhaDigitada == senhaEsperada[1]:
                        break
                break    
        else:
            print("Conta não cadastrada !")

    print("Login realizado com sucesso !")
    return senhaEsperada[0]
       

def escolherVeiculo(idMotorista):
    conexaoBD = conectar()

    caminhoes = pd.read_sql_query(f"select c.id ,c.placa, c.modelo from caminhao_motorista cm join caminhao c on c.id = cm.id_caminhao where cm.id_motorista = {idMotorista}",conexaoBD)

    desconectar(conexaoBD)

    for i in range(caminhoes.shape[0]):
        print(f"{i+1} - Placa: {caminhoes.loc[i,'placa']}, Modelo: {caminhoes.loc[i,'modelo']}")  

    while True:
        escolha =int(input("Escolha um dos veículos acima: "))
        if escolha < 1 or escolha > caminhoes.shape[0]:
            print(f"Escolha um número entre 1 e {caminhoes.shape[0]}")
        else: 
            break
    
    return caminhoes.loc[escolha-1,"id"]


def main():
  
    idMotorista = efetuarLogin()

    idCaminhao = escolherVeiculo(idMotorista)

    conexaoOBD= obd.OBD()

    dt = pd.DataFrame([{
        'temp_ar_admissao': -1 if conexaoOBD.query(obd.commands.INTAKE_TEMP).is_null() else conexaoOBD.query(obd.commands.INTAKE_TEMP).value.magnitude,
        'posicao_acelerador': -1 if conexaoOBD.query(obd.commands.THROTTLE_POS).is_null() else conexaoOBD.query(obd.commands.THROTTLE_POS).value.magnitude,
        'tempo_motor_ligado':"00:00" if conexaoOBD.query(obd.commands.RUN_TIME).is_null() else conexaoOBD.query(obd.commands.RUN_TIME).value.magnitude,
        'carga_motor':-1 if conexaoOBD.query(obd.commands.ENGINE_LOAD).is_null() else conexaoOBD.query(obd.commands.ENGINE_LOAD).value.magnitude,
        'rpm_motor':-1 if conexaoOBD.query(obd.commands.RPM).is_null() else conexaoOBD.query(obd.commands.RPM).value.magnitude,
        'dt_hora_leitura':datetime.now(),
        'pressao_pneu':-1,
        'sensores_oxigenio':-1 if conexaoOBD.query(obd.commands.FUEL_LEVEL).is_null() else conexaoOBD.query(obd.commands.FUEL_LEVEL).value.magnitude,
        'qtd_combustivel':-1 if conexaoOBD.query(obd.commands.O2_B1S1).is_null() else conexaoOBD.query(obd.commands.O2_B1S1).value.magnitude,
        'temp_arrefecimento':-1 if conexaoOBD.query(obd.commands.COOLANT_TEMP).is_null() else conexaoOBD.query(obd.commands.COOLANT_TEMP).value.magnitude,
        'pressao_coletor_admissao':-1 if conexaoOBD.query(obd.commands.INTAKE_PRESSURE).is_null() else conexaoOBD.query(obd.commands.INTAKE_PRESSURE).value.magnitude,
        'id_caminhao':idCaminhao
    }])

    conexaoDB = conectarInsert()
    dt.to_sql("informacoes",conexaoDB,if_exists='append',index=False)

    desconectar(conexaoDB)
    


if __name__ == "__main__":
    main()
        