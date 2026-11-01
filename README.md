# Cadastro de Pacientes — Gradio x Streamlit

Atividade Prática da Aula 1 (prof. Francisco Fambrini): a mesma aplicação de cadastro de pacientes
feita com duas bibliotecas Python de interface web.

| Pasta | Biblioteca | Onde roda |
|---|---|---|
| `gradio_app/` | Gradio (`gr.Blocks`) | Localmente |
| `streamlit_app/` | Streamlit (`st.form` + `st.session_state`) | Streamlit Community Cloud |

**App publicado:** https://cadastro-pacientes-gradio-app-nqc6euceguzguhl3caxlkf.streamlit.app/

## Como executar

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt

python gradio_app/app.py                 # http://127.0.0.1:7860
streamlit run streamlit_app/app.py       # http://localhost:8501
```

## Arquivos da entrega

- `gradio_app/print_gradio.png`: interface Gradio rodando localmente
- `gradio_app/pacientes.csv`: CSV de exemplo gerado nos testes (dados fictícios)
