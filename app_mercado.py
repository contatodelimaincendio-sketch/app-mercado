import streamlit as st
import pandas as pd

# Configuração da página para ficar otimizada no celular e no desktop
st.set_page_config(page_title="Lista de Mercado", page_icon="🛒", layout="centered")

# Dados iniciais baseados na sua planilha
DADOS_INICIAIS = [
    # Proteínas
    {"Categoria": "Proteínas", "Item": "Peito / Filé de Frango", "Qtd": 5.0, "Und": "kg", "Preco_Unit": 18.00, "No_Carrinho": True},
    {"Categoria": "Proteínas", "Item": "Carne Moída - Acém ou Patinho", "Qtd": 4.0, "Und": "kg", "Preco_Unit": 25.00, "No_Carrinho": True},
    {"Categoria": "Proteínas", "Item": "Ovos - Cartela c/ 30 und", "Qtd": 2.0, "Und": "und", "Preco_Unit": 35.00, "No_Carrinho": True},
    
    # Grãos e Cereais
    {"Categoria": "Grãos e Cereais", "Item": "Arroz Branco", "Qtd": 5.0, "Und": "kg", "Preco_Unit": 30.00, "No_Carrinho": True},
    {"Categoria": "Grãos e Cereais", "Item": "Feijão Carioca ou Preto", "Qtd": 3.0, "Und": "kg", "Preco_Unit": 24.00, "No_Carrinho": True},
    {"Categoria": "Grãos e Cereais", "Item": "Aveia em Flocos", "Qtd": 1.0, "Und": "kg", "Preco_Unit": 12.00, "No_Carrinho": True},
    {"Categoria": "Grãos e Cereais", "Item": "Macarrão Integral ou Comum", "Qtd": 2.0, "Und": "pct", "Preco_Unit": 14.00, "No_Carrinho": True},
    
    # Gordura e Óleos
    {"Categoria": "Gordura e Óleos", "Item": "Azeite de Oliva", "Qtd": 1.0, "Und": "und", "Preco_Unit": 35.00, "No_Carrinho": True},
    {"Categoria": "Gordura e Óleos", "Item": "Manteiga", "Qtd": 1.0, "Und": "und", "Preco_Unit": 0.00, "No_Carrinho": False},
    
    # Hortifrúti
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
    
    # Laticínios
    {"Categoria": "Laticínios", "Item": "Leite UHT Integral", "Qtd": 4.0, "Und": "und", "Preco_Unit": 5.00, "No_Carrinho": True},
    {"Categoria": "Laticínios", "Item": "Iogurte Natural Integral sem açúcar", "Qtd": 3.0, "Und": "und", "Preco_Unit": 5.00, "No_Carrinho": True},
    {"Categoria": "Laticínios", "Item": "Requeijão", "Qtd": 1.0, "Und": "und", "Preco_Unit": 0.00, "No_Carrinho": False},
    
    # Mercearia, Limpeza, Guloseimas e Bebidas
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
]

# Inicializa o estado dos dados na sessão
if "df_compras" not in st.session_state:
    st.session_state.df_compras = pd.DataFrame(DADOS_INICIAIS)

st.title("🛒 Controle de Mercado")

# Formulário para adicionar novos itens rapidamente
with st.expander("➕ Adicionar novo item"):
    with st.form("novo_item_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        novo_nome = col1.text_input("Nome do item")
        nova_cat = col2.selectbox("Categoria", st.session_state.df_compras["Categoria"].unique().tolist() + ["Diversos"])
        
        col3, col4, col5 = st.columns(3)
        nova_qtd = col3.number_input("Qtd", min_value=0.1, value=1.0, step=0.5)
        nova_und = col4.selectbox("Unidade", ["und", "kg", "pct", "L"])
        novo_preco = col5.number_input("Preço Unit. (R$)", min_value=0.0, value=0.0, step=0.50)
        
        if st.form_submit_button("Adicionar à lista") and novo_nome:
            novo_registro = pd.DataFrame([{
                "Categoria": nova_cat,
                "Item": novo_nome,
                "Qtd": nova_qtd,
                "Und": nova_und,
                "Preco_Unit": novo_preco,
                "No_Carrinho": novo_preco > 0
            }])
            st.session_state.df_compras = pd.concat([st.session_state.df_compras, novo_registro], ignore_index=True)
            st.rerun()

# Exibição e edição interativa por categoria
df = st.session_state.df_compras
categorias = df["Categoria"].unique()

for cat in categorias:
    df_cat = df[df["Categoria"] == cat]
    subtotal_cat = (df_cat[df_cat["No_Carrinho"]]["Qtd"] * df_cat[df_cat["No_Carrinho"]]["Preco_Unit"]).sum()
    
    st.subheader(f"{cat} — R$ {subtotal_cat:.2f}")
    
    # Tabela editável ideal para toque no iPhone ou clique no PC
    edited_df = st.data_editor(
        df_cat[["No_Carrinho", "Item", "Qtd", "Und", "Preco_Unit"]],
        key=f"editor_{cat}",
        use_container_width=True,
        hide_index=True,
        column_config={
            "No_Carrinho": st.column_config.CheckboxColumn("Carrinho", default=False),
            "Item": st.column_config.TextColumn("Produto", disabled=True),
            "Qtd": st.column_config.NumberColumn("Qtd", min_value=0.0, step=0.5),
            "Und": st.column_config.TextColumn("Und", disabled=True),
            "Preco_Unit": st.column_config.NumberColumn("R$ Unit.", min_value=0.0, step=0.10, format="%.2f"),
        }
    )
    
    # Atualiza o DataFrame principal com as alterações feitas na categoria
    st.session_state.df_compras.loc[edited_df.index, ["No_Carrinho", "Qtd", "Preco_Unit"]] = edited_df[["No_Carrinho", "Qtd", "Preco_Unit"]]

# Cálculo do valor total geral
df_atualizado = st.session_state.df_compras
df_atualizado["Total_Item"] = df_atualizado["Qtd"] * df_atualizado["Preco_Unit"]
valor_total_carrinho = df_atualizado[df_atualizado["No_Carrinho"]]["Total_Item"].sum()

st.divider()

# Painel de resumo financeiro no rodapé
col_res1, col_res2 = st.columns(2)
col_res1.metric("💰 Valor Total no Carrinho", f"R$ {valor_total_carrinho:.2f}")
col_res2.metric("📦 Itens Pegos", f"{df_atualizado['No_Carrinho'].sum()} de {len(df_atualizado)}")

# Botão para baixar a compra finalizada em CSV
csv_export = df_atualizado.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Baixar Planilha Atualizada (CSV)",
    data=csv_export,
    file_name="compras_mercado_finalizada.csv",
    mime="text/csv",
    use_container_width=True
)
