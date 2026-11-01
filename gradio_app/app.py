import gradio as gr
import pandas as pd
from datetime import datetime
from pathlib import Path

ARQUIVO_CSV = Path(__file__).parent / "pacientes.csv"
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]


def ultimos_pacientes(qtd=5):
    if not ARQUIVO_CSV.exists():
        return pd.DataFrame(columns=COLUNAS)
    return pd.read_csv(ARQUIVO_CSV).tail(qtd).iloc[::-1]


def validar(nome, idade, convenio, motivo):
    if not nome and not convenio and not motivo:
        return "Preencha os dados do paciente para fazer o cadastro."
    if not nome:
        return "Informe o nome do paciente."
    if idade is None or not 0 <= idade <= 120:
        return "Informe uma idade entre 0 e 120."
    if not convenio:
        return "Selecione o convênio."
    if len(motivo) < 3:
        return "Descreva o motivo da consulta (mínimo 3 caracteres)."
    return None


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    nome = (nome or "").strip()
    motivo = (motivo or "").strip()

    erro = validar(nome, idade, convenio, motivo)
    if erro:
        gr.Warning(erro, duration=5)
        return [gr.skip()] * 7

    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome,
        "idade": int(idade),
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": motivo,
    }
    arquivo_novo = not ARQUIVO_CSV.exists()
    pd.DataFrame([linha], columns=COLUNAS).to_csv(
        ARQUIVO_CSV, mode="a", header=arquivo_novo, index=False
    )

    return (
        f"Paciente {nome} cadastrado com sucesso!",
        ultimos_pacientes(),
        "", None, None, 1, "",
    )


with gr.Blocks(title="Cadastro de Pacientes") as demo:
    gr.Markdown("## Cadastro de Pacientes\nPreencha os dados e clique em **Cadastrar**.")

    nome = gr.Textbox(label="Nome do paciente", placeholder="Ex.: Maria da Silva")
    idade = gr.Number(label="Idade", precision=0, minimum=0, maximum=120)
    convenio = gr.Dropdown(CONVENIOS, label="Convênio", value=None)
    prioridade = gr.Slider(1, 5, value=1, step=1, label="Prioridade do atendimento (5 = urgente)")
    motivo = gr.Textbox(
        label="Motivo da consulta / observações",
        placeholder="Ex.: dor de cabeça há 3 dias",
        lines=3,
    )
    botao = gr.Button("Cadastrar", variant="primary")

    saida_msg = gr.Textbox(label="Status", interactive=False)
    tabela = gr.Dataframe(label="Últimos pacientes cadastrados", interactive=False)

    botao.click(
        cadastrar_paciente,
        inputs=[nome, idade, convenio, prioridade, motivo],
        outputs=[saida_msg, tabela, nome, idade, convenio, prioridade, motivo],
    )
    demo.load(ultimos_pacientes, outputs=tabela)

demo.launch()
