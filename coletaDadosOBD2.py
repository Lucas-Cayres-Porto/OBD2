import obd
import pandas as pd
from datetime import datetime
import psycopg2 as psy
import os
from dotenv import load_dotenv

def conectar():
    conn = None
    load_dotenv()

    try:
        conn = psy.connect(
            host=os.getenv("HOSTTEST"),
            database=os.getenv("DATABASETESTE"),
            user = os.getenv("USER"),
            password = os.getenv("PASSWORDTESTE"),
            port = os.getenv("PORTTEST"),
        )
    except psy.Error as e:
        print("Erro na conexão")
    finally:
        return conn
    
def desconectar(conn):
    if conn != None:
        conn.close()
    


def main():
    conexaoOBD= obd.OBD()

    dt = pd.DataFrame([{
        'temp_ar_admissao': -1 if conexaoOBD.query(obd.commands.INTAKE_TEMP).is_null() else conexaoOBD.query(obd.commands.INTAKE_TEMP).value.magnitude,
        'posicao_acelerador': -1 if conexaoOBD.query(obd.commands.THROTTLE_POS).is_null() else conexaoOBD.query(obd.commands.THROTTLE_POS).value.magnitude,
        'tempo_motor_ligado':-1 if conexaoOBD.query(obd.commands.RUN_TIME).is_null() else conexaoOBD.query(obd.commands.RUN_TIME).value.magnitude,
        'carga_motor':-1 if conexaoOBD.query(obd.commands.ENGINE_LOAD).is_null() else conexaoOBD.query(obd.commands.ENGINE_LOAD).value.magnitude,
        'rpm_motor':-1 if conexaoOBD.query(obd.commands.RPM).is_null() else conexaoOBD.query(obd.commands.RPM).value.magnitude,
        'dt_hora_leitura':datetime.now(),
        'pressao_pneu':-1,
        'sensores_oxigenio':-1 if conexaoOBD.query(obd.commands.FUEL_LEVEL).is_null() else conexaoOBD.query(obd.commands.FUEL_LEVEL).value.magnitude,
        'qtd_combustivel':-1 if conexaoOBD.query(obd.commands.O2_B1S1).is_null() else conexaoOBD.query(obd.commands.O2_B1S1).value.magnitude,
        'temp_arrefecimento':-1 if conexaoOBD.query(obd.commands.COOLANT_TEMP).is_null() else conexaoOBD.query(obd.commands.COOLANT_TEMP).value.magnitude,
        'pressao_coletor_admissao':-1 if conexaoOBD.query(obd.commands.INTAKE_PRESSURE).is_null() else conexaoOBD.query(obd.commands.INTAKE_PRESSURE).value.magnitude
    }])
    print(dt)


if __name__ == "__main__":
    main()
        