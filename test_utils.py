import pandas as pd
from streamlit_app import validar_cnpj, calcular_metricas

def test_validar_cnpj():
    assert validar_cnpj("11.222.333/0001-81") is True
    assert validar_cnpj("00.000.000/0000-00") is False
    assert validar_cnpj("12345678000195") is True
    assert validar_cnpj("123") is False

def test_calcular_metricas():
    df = pd.DataFrame({
        "Exposição Atual (R$)": [1000, 2000, 3000],
        "Dias de Atraso": [0, 31, 60]
    })
    vol, ina, conc = calcular_metricas(df)
    assert vol == 6000
    assert round(ina, 2) == 83.33
    assert round(conc, 2) == 50.0
