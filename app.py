from scipy.stats import binom
import streamlit as st


# ------------------------ Cálculos --------------------------------------
def calcular_ITM(tamanho_amostra, Pa, tamanho_lote):
    return tamanho_amostra + (1 - Pa) * (tamanho_lote - tamanho_amostra)

def calcular_riscos_e_custos(tamanho_lote, custo_unitario_inspecao, despesa_lote_reprovado, NQA, tamanho_amostra, aceitacao_maxima, taxa_defeituosos, dias_uteis_mes, PTDL):

    # Cálculo dos riscos
    risco_fornecedor = 1 - binom.cdf(aceitacao_maxima, tamanho_amostra, NQA / 100)
    risco_consumidor = binom.cdf(aceitacao_maxima, tamanho_amostra, PTDL / 100)

    # Cálculo da probabilidade de aceitação considerando a taxa de defeitos atual
    Pa = binom.cdf(aceitacao_maxima, tamanho_amostra, taxa_defeituosos / 100)

    # Cálculo da Inspeção Total Média (ITM) considerando a taxa de defeitos atual
    ITM = calcular_ITM(tamanho_amostra, Pa, tamanho_lote)

    # Cálculo dos custos de inspeção
    custo_inspecao = dias_uteis_mes * ITM * custo_unitario_inspecao
    custo_lotes_rejeitados = dias_uteis_mes * (1 - Pa ) * despesa_lote_reprovado

    # Cálculo do custo total considerando lotes reprovados
    custo_total = custo_inspecao + custo_lotes_rejeitados

    # Determinação de aceitação ou rejeição do lote
    lote_aceito = Pa > (1 - PTDL / 100)

    # Resultados
    return risco_fornecedor, risco_consumidor, custo_inspecao, custo_total, ITM, custo_lotes_rejeitados, lote_aceito, Pa


# -------------  Interface e chamada do cálculo. --------------------

# Título da página
st.markdown("<h1 style='text-align: center; color: white; background-color: #0362fc; padding: 10px;'>Controle de Qualidade em uma Produção</h1><br>", unsafe_allow_html=True)

# Texto introdutório
st.write("**Digite os parâmetros abaixo para calcular os riscos e custos associados ao controle de qualidade de um lote:**")

# Entrada de Parâmetros
col1, col2 = st.columns(2)

with col1:
    TAMANHO_LOTE = st.number_input("Tamanho do Lote:", value=0)
    TAMANHO_AMOSTRA = st.number_input("Tamanho da Amostra:", value=0)
    CUSTO_UNITARIO_INSPECAO = st.number_input("Custo unitário por inspeção:", value=0.0, format="%g")
    CUSTO_DISPESA_LOTE_REPROVADO = st.number_input("Custo dispesa por lote reprovado:", value=0.0, format="%g")

with col2:
    NQA = st.number_input("Nível de Qualidade Aceitável (%):", value=0.0, format="%g")
    INDICE_ACEITACAO_MAXIMA = st.number_input("Indice de aceitação máxima (%):", value=0.0, format="%g")
    PTDL = st.number_input("Percentual Tolerável de Defeitos no Lote (%):", value=0.0, format="%g")
    HISTORICO_TAXA_DEFEITUOSO = st.number_input("Histórico da Taxa de Defeituosos do Fornecedor (%):", value=0.0, format="%g")
    DIAS_UTEIS_MES = st.number_input("Número de dias úteis no mês:", value=0)

st.markdown("<hr>", unsafe_allow_html=True)

# Botão de ação
if st.button("Calcular"):

    # Chamada da função de cálculo
    risco_fornecedor, risco_consumidor, custo_inspecao, custo_total, ITM, custo_lotes_rejeitados, lote_aceito, Pa = calcular_riscos_e_custos(
        tamanho_lote=TAMANHO_LOTE, 
        custo_unitario_inspecao=CUSTO_UNITARIO_INSPECAO, 
        despesa_lote_reprovado=CUSTO_DISPESA_LOTE_REPROVADO, 
        NQA=NQA, 
        tamanho_amostra=TAMANHO_AMOSTRA, 
        aceitacao_maxima=INDICE_ACEITACAO_MAXIMA, 
        taxa_defeituosos=HISTORICO_TAXA_DEFEITUOSO, 
        dias_uteis_mes=DIAS_UTEIS_MES, 
        PTDL=PTDL
    )

    st.session_state["risco_fornecedor"] = risco_fornecedor
    st.session_state["risco_consumidor"] = risco_consumidor
    st.session_state["custo_inspecao"] = custo_inspecao
    st.session_state["custo_lotes_rejeitados"] = custo_lotes_rejeitados
    st.session_state["custo_total"] = custo_total
    st.session_state["ITM"] = ITM
    st.session_state["lote_aceito"] = lote_aceito
    st.session_state["Pa"] = Pa

    st.markdown("<br>", unsafe_allow_html=True)
    st.success("**Resultado do Cálculo**")
    st.write("**Riscos:**")

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"Risco do fornecedor: **{st.session_state["risco_fornecedor"]:.4f}**")
        st.info(f"Risco do consumidor: **{st.session_state["risco_consumidor"]:.4f}**")

    with col2:
        st.info(f"Inspeção Total Média (ITM): **{st.session_state["ITM"]:.2f}**")
        st.info(f"Probabilidade de Aceitação (Pa): **{st.session_state["Pa"]:.2f}**")


    st.write("**Custos:**")
    st.metric(label="Custo de inspeção", value=f"R$ {st.session_state["custo_inspecao"]:.2f}")
    st.metric(label="Custo de despesas", value=f"R$ {st.session_state["custo_lotes_rejeitados"]:.2f}")
    st.metric(label="Custo total", value=f"R$ {st.session_state["custo_total"]:.2f}")

    st.write("**Lote passou na inspeção ?**")

    if st.session_state["lote_aceito"]:
        st.success("Sim, passou na inspeção")
    else:
        st.error("Não passou na inspeção")


    

    