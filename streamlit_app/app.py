import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ARQUIVO_CSV = Path(__file__).parent / "pacientes.csv"
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]
VALORES_INICIAIS = {"nome": "", "idade": None, "convenio": None, "prioridade": 1, "motivo": ""}

st.set_page_config(page_title="Cadastro de Pacientes", layout="centered")

if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(columns=COLUNAS)
if "aviso" not in st.session_state:
    st.session_state.aviso = None
for chave, valor in VALORES_INICIAIS.items():
    st.session_state.setdefault(chave, valor)


def validar(nome, idade, convenio, motivo):
    if not nome and idade is None and not convenio and not motivo:
        return "Preencha os dados do paciente para fazer o cadastro."
    if not nome:
        return "Informe o nome do paciente."
    if idade is None:
        return "Informe a idade do paciente."
    if not convenio:
        return "Selecione o convênio."
    if len(motivo) < 3:
        return "Descreva o motivo da consulta (mínimo 3 caracteres)."
    return None


def cadastrar():
    ss = st.session_state
    nome = ss.nome.strip()
    motivo = ss.motivo.strip()

    erro = validar(nome, ss.idade, ss.convenio, motivo)
    if erro:
        ss.aviso = erro
        return

    linha = {
        "timestamp": datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome,
        "idade": int(ss.idade),
        "convenio": ss.convenio,
        "prioridade": int(ss.prioridade),
        "motivo": motivo,
    }
    novo = pd.DataFrame([linha], columns=COLUNAS)

    ss.pacientes = pd.concat([ss.pacientes, novo], ignore_index=True)
    novo.to_csv(ARQUIVO_CSV, mode="a", header=not ARQUIVO_CSV.exists(), index=False)

    ss.update(VALORES_INICIAIS)
    ss.aviso = f"Paciente {nome} cadastrado com sucesso!"


st.title("Cadastro de Pacientes")
st.caption("Preencha os dados e clique em **Cadastrar**.")

with st.form("cadastro"):
    st.text_input("Nome do paciente", key="nome", placeholder="Ex.: Maria da Silva")
    st.number_input("Idade", key="idade", min_value=0, max_value=120, step=1)
    st.selectbox("Convênio", CONVENIOS, key="convenio", placeholder="Selecione...")
    st.slider("Prioridade do atendimento (5 = urgente)", 1, 5, key="prioridade")
    st.text_area("Motivo da consulta / observações", key="motivo",
                 placeholder="Ex.: dor de cabeça há 3 dias")
    st.form_submit_button("Cadastrar", type="primary", on_click=cadastrar,
                          width="stretch")

if st.session_state.aviso:
    st.toast(st.session_state.aviso)
    st.session_state.aviso = None

st.subheader("Últimos pacientes cadastrados")
st.dataframe(st.session_state.pacientes.tail(5).iloc[::-1], hide_index=True,
             width="stretch")

csv = st.session_state.pacientes.to_csv(index=False).encode("utf-8")
st.download_button("Baixar CSV", csv, "pacientes.csv", "text/csv",
                   disabled=st.session_state.pacientes.empty, width="stretch")
