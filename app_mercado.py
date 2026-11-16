import os
import gspread
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lista de Mercado", page_icon="🛒", layout="centered")

# 1. COLE AQUI O LINK COMPLETO DA SUA PLANILHA DO GOOGLE SHEETS
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/193UrLGzATObLaz8qyE7yyhYy7j8mZyamdtK_9209KDM/edit?gid=779834175#gid=779834175"

# 2. Dados base da sua planilha original (usados apenas se o Google Sheets estiver vazio)
DADOS_INICIAIS = [
    {"Categoria": "Proteínas", "Item": "Peito / Filé de Frango", "Qtd": 5.0, "Und": "kg", "Preco_Unit": 18.00, "No_Carrinho": True},
    {"Categoria": "Proteínas", "Item": "Carne Moída - Acém ou Patinho", "Qtd": 4.0, "Und": "kg", "Preco_Unit": 25.00, "No_Carrinho": True},
    {"Categoria": "Proteínas", "Item": "Ovos - Cartela c/ 30 und", "Qtd": 2.0, "Und": "und", "Preco_Unit": 35.00, "No_Carrinho": True},
    {"Categoria": "Grãos e Cereais", "Item": "Arroz Branco", "Qtd": 5.0, "Und": "kg", "Preco_Unit": 30.00, "No_Carrinho": True},
    {"Categoria": "Grãos e Cereais", "Item": "Feijão Carioca ou Preto", "Qtd": 3.0, "Und": "kg", "Preco_Unit": 24.00, "No_Carrinho": True},
    {"Categoria": "Grãos e Cereais", "Item": "Aveia em Flocos", "Qtd": 1.0, "Und": "kg", "Preco_Unit": 12.00, "No_Carrinho": True},
    {"Categoria": "Grãos e Cereais", "Item": "Macarrão Integral ou Comum", "Qtd": 2.0, "Und": "pct", "Preco_Unit": 14.00, "No_Carrinho": True},
    {"Categoria": "Gordura e Óleos", "Item": "Azeite de Oliva", "Qtd": 1.0, "Und": "und", "Preco_Unit": 35.00, "No_Carrinho": True},
    {"Categoria": "Gordura e Óleos", "Item": "Manteiga", "Qtd": 1.0, "Und": "und", "Preco_Unit": 0.00, "No_Carrinho": False},
    {"Categoria": "Hortifrúti", "Item": "Abóbora", "Qtd": 2.0, "Und": "kg", "Preco_Unit": 6.00, "No_Carrinho": True},
    {"Categoria": "Hortifrúti", "Item": "Cenoura", "Qtd": 1.0, "Und": "kg", "Preco_Unit": 19.90, "No_Carrinho": True},
    {"Categoria": "Hortifrúti", "Item": "Abobrinha", "Qtd": 1.5, "Und": "kg", "Preco_Unit": 12.50, "No_Carrinho": True},
    {"Categoria": "Hortifrúti", "Item": "Mandioca", "Qtd": 1.5, "Und": "kg", "Preco_Unit": 12.50, "No_Carrinho": True},
    {"Categoria": "Hortifrúti", "Item": "Batata Inglesa", "Qtd": 1.5, "Und": "kg", "Preco_Unit": 12.50, "No_Carrinho": True},
    {"Categoria": "Hortifrúti", "Item": "Cebola", "Qtd": 1.0, "Und": "kg", "Preco_Unit": 10.00, "No_Carrinho": True},
    {"Categoria": "Hortifrúti", "Item": "Alho", "Qtd": 1.0, "Und": "kg", "Preco_Unit": 10.00, "No_Carrinho": True},
    {"Categoria": "Hortifrúti", "Item": "Banana", "Qtd": 4.0, "Und": "kg", "Preco_Unit": 6.00, "No_Carrinho": True},
    {"Categoria": "Hortifrúti", "Item": "Maçã", "Qtd": 1.0, "Und": "kg", "Preco_Unit": 15.00, "No_Carrinho": True},
    {"Categoria": "Hortifrúti", "Item": "Mamão", "Qtd": 1.0, "Und": "kg", "Preco_Unit": 15.00, "No_Carrinho": True},
    {"Categoria": "Hortifrúti", "Item": "Laranja", "Qtd": 5.0, "Und": "kg", "Preco_Unit": 3.60, "No_Carrinho": True},
    {"Categoria": "Hortifrúti", "Item": "Couve", "Qtd": 1.0, "Und": "kg", "Preco_Unit": 0.00, "No_Carrinho": False},
    {"Categoria": "Hortifrúti", "Item": "Alface", "Qtd": 1.0, "Und": "kg", "Preco_Unit": 0.00, "No_Carrinho": False},
    {"Categoria": "Hortifrúti", "Item": "Brócolis", "Qtd": 1.0, "Und": "kg", "Preco_Unit": 0.00, "No_Carrinho": False},
    {"Categoria": "Laticínios", "Item": "Leite UHT Integral", "Qtd": 4.0, "Und": "und", "Preco_Unit": 5.00, "No_Carrinho": True},
    {"Categoria": "Laticínios", "Item": "Iogurte Natural Integral sem açúcar", "Qtd": 3.0, "Und": "und", "Preco_Unit": 5.00, "No_Carrinho": True},
    {"Categoria": "Laticínios", "Item": "Requeijão", "Qtd": 1.0, "Und": "und", "Preco_Unit": 0.00, "No_Carrinho": False},
    {"Categoria": "Mercearia", "Item": "Pão", "Qtd": 1.0, "Und": "und", "Preco_Unit": 0.00, "No_Carrinho": False},
    {"Categoria": "Mercearia", "Item": "Peito de Peru", "Qtd": 1.0, "Und": "und", "Preco_Unit": 0.00, "No_Carrinho": False},
    {"Categoria": "Mercearia", "Item": "Queijo", "Qtd": 1.0, "Und": "und", "Preco_Unit": 0.00, "No_Carrinho": False},
    {"Categoria": "Limpeza", "Item": "Detergente", "Qtd": 1.0, "Und": "und", "Preco_Unit": 0.00, "No_Carrinho": False},
    {"Categoria": "Limpeza", "Item": "Saco Lixo", "Qtd": 1.0, "Und": "und", "Preco_Unit": 0.00, "No_Carrinho": False},
    {"Categoria": "Guloseimas", "Item": "Salgadinho", "Qtd": 1.0, "Und": "und", "Preco_Unit": 0.00, "No_Carrinho": False},
    {"Categoria": "Guloseimas", "Item": "Chocolate", "Qtd": 1.0, "Und": "und", "Preco_Unit": 0.00, "No_Carrinho": False},
    {"Categoria": "Bebidas", "Item": "Água com Gás", "Qtd": 1.0, "Und": "und", "Preco_Unit": 0.00, "No_Carrinho": False},
    {"Categoria": "Bebidas", "Item": "Coca-Cola", "Qtd": 1.0, "Und": "und", "Preco_Unit": 0.00, "No_Carrinho": False},
    {"Categoria": "Bebidas", "Item": "Cerveja", "Qtd": 1.0, "Und": "und", "Preco_Unit": 0.00, "No_Carrinho": False},
    {"Categoria": "Diversos", "Item": "Item Diverso 1", "Qtd": 1.0, "Und": "und", "Preco_Unit": 0.00, "No_Carrinho": False},
]

# Conector compatível com gspread usando chave_google.json local ou Secrets na nuvem
class PlanilhaGoogle:
    def __init__(self):
        caminho_json = os.path.join(os.path.dirname(__file__), "chave_google.json")
        if os.path.exists(caminho_json):
            self.gc = gspread.service_account(filename=caminho_json)
        else:
            credenciais = dict(st.secrets["connections"]["gsheets"])
            credenciais.pop("spreadsheet", None)
            self.gc = gspread.service_account_from_dict(credenciais)

    def read(self, spreadsheet, ttl=0):
        aba = self.gc.open_by_url(spreadsheet).sheet1
        registros = aba.get_all_records()
        return pd.DataFrame(registros)

    def update(self, spreadsheet, data):
        aba = self.gc.open_by_url(spreadsheet).sheet1
        aba.clear()
        df_salvar = data.fillna("")
        dados_lista = [df_salvar.columns.values.tolist()] + df_salvar.values.tolist()
        aba.update(dados_lista)

conn = PlanilhaGoogle()

def carregar_dados():
    df = conn.read(spreadsheet=URL_PLANILHA)
    if df.empty or len(df) == 0:
        df = pd.DataFrame(DADOS_INICIAIS)
        conn.update(spreadsheet=URL_PLANILHA, data=df)
    else:
        df["Item"] = df["Item"].fillna("").astype(str)
        df["Und"] = df["Und"].fillna("und").astype(str)
        df["Qtd"] = pd.to_numeric(df["Qtd"], errors="coerce").fillna(1.0)
        df["Preco_Unit"] = pd.to_numeric(df["Preco_Unit"], errors="coerce").fillna(0.0)
        df["No_Carrinho"] = df["No_Carrinho"].astype(str).str.upper().isin(["TRUE", "1", "SIM"])
    return df
if "df_compras" not in st.session_state:
    st.session_state.df_compras = carregar_dados()

st.title("🛒 Controle de Mercado")

# Botão para zerar carrinho no início de uma nova compra
if st.button("🔄 Iniciar Nova Compra (Desmarcar todos os itens)"):
    st.session_state.df_compras["No_Carrinho"] = False
    conn.update(spreadsheet=URL_PLANILHA, data=st.session_state.df_compras)
    st.toast("Carrinho zerado e salvo na planilha!", icon="✅")
    st.rerun()

df = st.session_state.df_compras
categorias = df["Categoria"].unique()
novos_blocos = []
houve_alteracao = False

colunas_tabela = ["No_Carrinho", "Item", "Qtd", "Und", "Preco_Unit"]

for cat in categorias:
    df_cat = df[df["Categoria"] == cat].reset_index(drop=True)
    subtotal_cat = (df_cat[df_cat["No_Carrinho"]]["Qtd"] * df_cat[df_cat["No_Carrinho"]]["Preco_Unit"]).sum()
    
    st.subheader(f"{cat} — R$ {subtotal_cat:.2f}")
    
    # Tabela totalmente editável com opção de adicionar (+) ou excluir linhas
    edited_df = st.data_editor(
        df_cat[colunas_tabela],
        key=f"editor_{cat}",
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "No_Carrinho": st.column_config.CheckboxColumn("Carrinho", default=False),
            "Item": st.column_config.TextColumn("Produto", default="Novo item"),
            "Qtd": st.column_config.NumberColumn("Qtd", min_value=0.0, step=0.5, default=1.0),
            "Und": st.column_config.SelectboxColumn("Und", options=["und", "kg", "pct", "L", "g", "ml"], default="und"),
            "Preco_Unit": st.column_config.NumberColumn("R$ Unit.", min_value=0.0, step=0.10, format="%.2f", default=0.0),
        }
    )
    
    # Preenche valores padrão caso uma nova linha tenha sido criada pelo botão '+'
    edited_df["No_Carrinho"] = edited_df["No_Carrinho"].fillna(False).astype(bool)
    edited_df["Item"] = edited_df["Item"].fillna("Novo item").astype(str)
    edited_df["Qtd"] = pd.to_numeric(edited_df["Qtd"], errors="coerce").fillna(1.0)
    edited_df["Und"] = edited_df["Und"].fillna("und").astype(str)
    edited_df["Preco_Unit"] = pd.to_numeric(edited_df["Preco_Unit"], errors="coerce").fillna(0.0)
    edited_df["Categoria"] = cat
    
    # Verifica se houve adição, exclusão ou edição nesta categoria
    if not df_cat[colunas_tabela].equals(edited_df[colunas_tabela]):
        houve_alteracao = True
        
    novos_blocos.append(edited_df[["Categoria"] + colunas_tabela])

# Reconstrói a planilha completa e salva no Google Sheets se algo mudou
if houve_alteracao:
    df_reconstruido = pd.concat(novos_blocos, ignore_index=True)
    df_reconstruido = df_reconstruido[df_reconstruido["Item"].str.strip() != ""].reset_index(drop=True)
    st.session_state.df_compras = df_reconstruido
    conn.update(spreadsheet=URL_PLANILHA, data=df_reconstruido)
    st.toast("Alterações salvas no Google Sheets!", icon="☁️")
    st.rerun()

df_atualizado = st.session_state.df_compras
valor_total_carrinho = (df_atualizado[df_atualizado["No_Carrinho"]]["Qtd"] * df_atualizado[df_atualizado["No_Carrinho"]]["Preco_Unit"]).sum()

st.divider()

col_res1, col_res2 = st.columns(2)
col_res1.metric("💰 Valor Total no Carrinho", f"R$ {valor_total_carrinho:.2f}")
col_res2.metric("📦 Itens Pegos", f"{df_atualizado['No_Carrinho'].sum()} de {len(df_atualizado)}")