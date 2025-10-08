class Informacoes:

    def __init__(self,tempArAdmissao,posicaoAcelerador,tempoMotorLigado,cargaMotor,rpmMotor,
            dtHoraLeitura,pressaoPneu,sensoresOxigenio,qtdCombustivel,tempArrefecimento,
            pressaoColetorAdmissao):
        
        self.tempArAdmissao=tempArAdmissao
        self.posicaoAcelerador=posicaoAcelerador
        self.tempoMotorLigado=tempoMotorLigado
        self.cargaMotor=cargaMotor
        self.rpmMotor=rpmMotor
        self.dtHoraLeitura=dtHoraLeitura
        self.pressaoPneu=pressaoPneu
        self.sensoresOxigenio=sensoresOxigenio
        self.qtdCombustivel=qtdCombustivel
        self.tempArrefecimento=tempArrefecimento
        self.pressaoColetorAdmissao=pressaoColetorAdmissao

    def __str__(self):
        return f"""Temperatura Ar Admissão: {self.tempArAdmissao}
Posição Acelerador: {self.posicaoAcelerador}
Tempo Motor Ligado: {self.tempoMotorLigado}
Carga Motor: {self.cargaMotor}
RMP Motor: {self.rpmMotor}
Data Hora Leitura: {self.dtHoraLeitura}
Pressão Pneu: {self.pressaoPneu}
Sensores Oxigêni: {self.sensoresOxigenio}
Quantidade Combustível: {self.qtdCombustivel}
Temperatura Arrefecimento: {self.tempArrefecimento}
Pressão Coletor Admissão: {self.pressaoColetorAdmissao}"""    
        