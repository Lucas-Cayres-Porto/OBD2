import obd
import pandas as pd
from datetime import datetime

def main():
    conexaoOBD= obd.OBD()

    dt = pd.DataFrame([{
        'temp_ar_admissao':conexaoOBD.query(obd.commands.INTAKE_TEMP).value,
        'posicao_acelerador':conexaoOBD.query(obd.commands.THROTTLE_POS).value,
        'tempo_motor_ligado':conexaoOBD.query(obd.commands.RUN_TIME).value,
        'carga_motor':conexaoOBD.query(obd.commands.ENGINE_LOAD).value,
        'rpm_motor':conexaoOBD.query(obd.commands.RPM).value,
        'dt_hora_leitura':datetime.now(),
        'pressao_pneu':50,
        'sensores_oxigenio':conexaoOBD.query(obd.commands.FUEL_LEVEL).value,
        'qtd_combustivel':conexaoOBD.query(obd.commands.O2_B1S1).value,
        'temp_arrefecimento':conexaoOBD.query(obd.commands.COOLANT_TEMP).value,
        'pressao_coletor_admissao':conexaoOBD.query(obd.commands.INTAKE_PRESSURE).value
    }])
    print(dt)


if __name__ == "__main__":
    main()
        