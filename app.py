from scipy.stats import binom
import streamlit as st


# ------------------------ Cálculos de Inspeção --------------------------------------


# ------------------------ Função para cálculo da inspeção média total ------------------------
def calcular_inspecao_media_total(tamanho_amostra, probabilidade_aceitacao, tamanho_lote):
    return tamanho_amostra + (1 - probabilidade_aceitacao) * (tamanho_lote - tamanho_amostra)

# ------------------------ Função para cálculo do custo de deslocamento ------------------------
def calcular_custo_deslocamento(distancia, custo_por_km, numero_visitas):
    return distancia * custo_por_km * numero_visitas

# ------------------------ Função para cálculo dos riscos e custos ------------------------
def calcular_riscos_e_custos(tamanho_lote, custo_unitario_inspecao, despesa_lote_reprovado, nivel_qualidade_aceitavel, tamanho_amostra, aceitacao_maxima, taxa_defeituosos, dias_uteis_mes, percent_toleravel_defeitos_lote, distancia, custo_por_km, numero_visitas):

     # Calculos - Risco do fornecedor e do consumidor
    risco_do_fornecedor = 1 - binom.cdf(aceitacao_maxima, tamanho_amostra, nivel_qualidade_aceitavel / 100)
    risco_do_consumidor = binom.cdf(aceitacao_maxima, tamanho_amostra, percent_toleravel_defeitos_lote / 100)

    # Cálculo da probabilidade de aceitação baseada na taxa de defeitos
    probabilidade_aceitacao = binom.cdf(aceitacao_maxima, tamanho_amostra, taxa_defeituosos / 100)

    # Inspeção Total Média (ITM) considerando a taxa de defeitos
    inspeção_media_total  = calcular_inspecao_media_total(tamanho_amostra, probabilidade_aceitacao, tamanho_lote)

    # Custo de inspeção
    custo_inspecao = dias_uteis_mes * inspeção_media_total * custo_unitario_inspecao
    custo_lotes_rejeitados = dias_uteis_mes * (1 - probabilidade_aceitacao ) * despesa_lote_reprovado

    # Cálculo do custo de deslocamento
    custo_deslocamento = calcular_custo_deslocamento(
        distancia=distancia, 
        custo_por_km=custo_por_km, 
        numero_visitas=numero_visitas
    )

    # Cálculo do custo total
    custo_total = custo_inspecao + custo_lotes_rejeitados + custo_deslocamento

    # Verificação de aceitação ou rejeição do lote
    lote_aceito = probabilidade_aceitacao > (1 - percent_toleravel_defeitos_lote / 100)

    # Retorno dos resultados
    return risco_do_fornecedor, risco_do_consumidor, custo_inspecao, custo_total, inspeção_media_total , custo_lotes_rejeitados, lote_aceito, probabilidade_aceitacao, custo_deslocamento


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
    CUSTO_POR_KM = st.number_input("Custo por km rodado (R$):", value=0.0, format="%g")
    DISTANCIA = st.number_input("Distância até o local da inspeção (km):", value=0.0, format="%g")

with col2:
    NIVEL_QUALIDADE_ACEITAVEL = st.number_input("Nível de Qualidade Aceitável (%):", value=0.0, format="%g")
    INDICE_ACEITACAO_MAXIMA = st.number_input("Indice de aceitação máxima (%):", value=0.0, format="%g")
    PERCENT_TOLERAVEL_DEFEITOS_LOTE = st.number_input("Percentual Tolerável de Defeitos no Lote (%):", value=0.0, format="%g")
    HISTORICO_TAXA_DEFEITUOSO = st.number_input("Histórico da Taxa de Defeituosos do Fornecedor (%):", value=0.0, format="%g")
    DIAS_UTEIS_MES = st.number_input("Número de dias úteis no mês:", value=0)
    NUMERO_VISITAS = st.number_input("Número de visitas por mês:", value=0)

st.markdown("<hr>", unsafe_allow_html=True)

# Botão de ação
if st.button("Calcular"):

    # Chamada da função de cálculo
    risco_fornecedor, risco_consumidor, custo_inspecao, custo_total, inspeção_media_total, custo_lotes_rejeitados, lote_aceito, probabilidade_aceitacao, custo_deslocamento = calcular_riscos_e_custos(
        tamanho_lote=TAMANHO_LOTE, 
        custo_unitario_inspecao=CUSTO_UNITARIO_INSPECAO, 
        despesa_lote_reprovado=CUSTO_DISPESA_LOTE_REPROVADO,
        nivel_qualidade_aceitavel=NIVEL_QUALIDADE_ACEITAVEL,
        tamanho_amostra=TAMANHO_AMOSTRA, 
        aceitacao_maxima=INDICE_ACEITACAO_MAXIMA, 
        taxa_defeituosos=HISTORICO_TAXA_DEFEITUOSO, 
        dias_uteis_mes=DIAS_UTEIS_MES, 
        percent_toleravel_defeitos_lote=PERCENT_TOLERAVEL_DEFEITOS_LOTE,
        distancia=DISTANCIA,
        numero_visitas=NUMERO_VISITAS,
        custo_por_km=CUSTO_POR_KM
    )

    st.session_state["risco_fornecedor"] = risco_fornecedor
    st.session_state["risco_consumidor"] = risco_consumidor
    st.session_state["custo_inspecao"] = custo_inspecao
    st.session_state["custo_lotes_rejeitados"] = custo_lotes_rejeitados
    st.session_state["custo_total"] = custo_total
    st.session_state["ITM"] = inspeção_media_total
    st.session_state["lote_aceito"] = lote_aceito
    st.session_state["probabilidade_aceitacao"] = probabilidade_aceitacao
    st.session_state["custo_deslocamento"] = custo_deslocamento

    st.markdown("<br>", unsafe_allow_html=True)
    st.success("**Resultado do Cálculo**")
    st.write("**Riscos:**")

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"Risco do fornecedor: **{st.session_state["risco_fornecedor"]:.4f}**")
        st.info(f"Risco do consumidor: **{st.session_state["risco_consumidor"]:.4f}**")

    with col2:
        st.info(f"Inspeção Total Média (ITM): **{st.session_state["ITM"]:.2f}**")
        st.info(f"Probabilidade de Aceitação (Pa): **{st.session_state["probabilidade_aceitacao"]:.2f}**")


    st.write("**Custos:**")
    st.metric(label="Custo de inspeção", value=f"R$ {st.session_state["custo_inspecao"]:.2f}")
    st.metric(label="Custo de despesas", value=f"R$ {st.session_state["custo_lotes_rejeitados"]:.2f}")
    st.metric(label="Custo de deslocamento", value=f"R$ {st.session_state["custo_deslocamento"]:.2f}")
    st.metric(label="Custo total", value=f"R$ {st.session_state["custo_total"]:.2f}")

    st.write("**Lote passou na inspeção ?**")

    if st.session_state["lote_aceito"]:
        st.success("Sim, passou na inspeção")
    else:
        st.error("Não passou na inspeção")


    

    