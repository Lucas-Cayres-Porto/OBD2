import cores as c


def test_cores_ansi_definidas():
    assert c.reset == "\033[0m"
    assert c.verde == "\033[32m"
    assert c.vermelho == "\033[31m"
    assert c.azul == "\033[34m"


def test_separador_executa_sem_erros(capsys):
    c.separador()
    captured = capsys.readouterr()
    assert "-" * 70 in captured.out
