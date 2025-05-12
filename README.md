# 📊 Dashboard de Monitoramento de Crédito

Este é um dashboard interativo desenvolvido com **Streamlit** e **Plotly** para análise de crédito, risco e inadimplência de tomadores, incluindo recursos como:

- Upload ou geração automática de dados simulados
- Visualização de KPIs (volume, inadimplência, concentração)
- Gráficos interativos por setor, score e maiores devedores
- Formulário de adição de novos devedores com validação de CNPJ
- Exportação dos dados em Excel
- Testes automatizados com Pytest
- Integração com GitHub Actions + Microsoft Teams

## 🚀 Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 🧪 Executar testes

```bash
make test
# ou
./run_tests.sh
```

## 🛠️ CI/CD com GitHub Actions

Inclui workflow automatizado com execução de testes e envio de notificações para Microsoft Teams.

## 📦 Requisitos

- Python 3.10+
- Streamlit, Plotly, Pandas, Pytest
