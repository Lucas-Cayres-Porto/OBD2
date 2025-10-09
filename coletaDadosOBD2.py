import obd, os, re, sqlalchemy as sqla, pandas as pd, warnings, psycopg2 as psy,logging
from datetime import datetime
from dotenv import load_dotenv
from time import sleep
import cores as c


#pip install sqlalchemy psycopg2 obd


logging.getLogger("obd.obd").setLevel(logging.CRITICAL)

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
    c.separador()
    print(f"{c.branco_negrito}Faça o Seu Login{c.reset}".center(70))
    c.separador()

    while True:
        while True:
            email=input("Digite o seu email: ")
            if re.match(r"^[A-Za-z0-9\.-]+@[a-zA-Z]+\.[A-Za-z\.]+$",email):
                break
            else:
                print(f"{c.vermelho}Formato de email ínvalido, digite um valido!{c.reset}")

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
                    print(f"{c.vermelho}Senha incorreta, digite novamente !{c.reset}")
                    senhaDigitada=input("Digite a sua senha: ")
                    if senhaDigitada == senhaEsperada[1]:
                        break
                break    
        else:
            print(f"{c.vermelho}Email não cadastrado !{c.reset}")
            c.separador()

    c.separador()        
    print(f"{c.verde_negrito}Login realizado com sucesso !{c.reset}".center(70))

    return senhaEsperada[0]
       

def escolherVeiculo(idMotorista):
    conexaoBD = conectar()

    caminhoes = pd.read_sql_query(f"select c.id ,c.placa, c.modelo from caminhao_motorista cm join caminhao c on c.id = cm.id_caminhao where cm.id_motorista = {idMotorista}",conexaoBD)

    desconectar(conexaoBD)

    c.separador()
    print(f"{c.branco_negrito}Veículos Disponíveis{c.reset}".center(70))
    for i in range(caminhoes.shape[0]):
        print(f"{c.branco_negrito}{i+1}{c.reset} - Placa: {c.amarelo}{caminhoes.loc[i,'placa']}{c.reset}, Modelo: {c.amarelo}{caminhoes.loc[i,'modelo']}{c.reset}")  

    while True:
        escolha =int(input("Escolha um dos veículos: "))
        if escolha < 1 or escolha > caminhoes.shape[0]:
            print(f"{c.vermelho}Escolha um número entre 1 e {caminhoes.shape[0]}{c.reset}")
        else: 
            break
    c.separador()
    print(f"{c.verde_negrito}Veículo escolhido com sucesso !{c.reset}".center(70))
    c.separador
    return caminhoes.loc[escolha-1,"id"]

def main():
    
    idMotorista = efetuarLogin()

    idCaminhao = escolherVeiculo(idMotorista)

    c.separador()
    print(f"{c.branco_negrito}Inciando Coleta de Dados{c.reset}".center(70))

    for i in range(10):

        sleep(10)

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
        
        conexaoOBD.close()

        conexaoDB = conectarInsert()
        dt.to_sql("informacoes",conexaoDB,if_exists='append',index=False)

        desconectar(conexaoDB)

        print(f"{c.ciano}Coleta de Dados: {i+1}/10{c.reset}")

    c.separador()    
    print(f"{c.verde_negrito}Coleta de Dados Realizada com Sucesso{c.reset}".center(70))
    c.separador()



        
    


if __name__ == "__main__":
    main()
        