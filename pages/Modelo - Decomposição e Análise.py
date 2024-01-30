# Importação das bibliotecas
import streamlit as st
from statsmodels.tsa.seasonal import seasonal_decompose
from utils import select_bq,decomposicao,teste_estatistico

# Configuração da página
st.set_page_config(page_title= 'Modelo - Decomposição e Análise', layout='wide', page_icon= ':fuelpump:')

# Título da página e descrição introdutória da decomposição e período sazonal
st.title('Modelo - Decomposição e Análise da Série Temporal 📊')
st.markdown('<p style="text-align: justify;"> Na decomposição sazonal de uma série temporal, os termos "multiplicativo" (multi) e "aditivo" (add) referem-se à maneira como os componentes de tendência e sazonalidade são combinados para reconstruir a série original. Além disso, para uma análise exploratória dos dados, é importante identificar o período sazonal relevante para os padrões presentes na série temporal, para avaliar o ajuste no modelo. Aqui estão alguns tipos comuns de sazonalidade que podem ser observados em séries temporais diárias.</p>', unsafe_allow_html = True)

st.subheader('Modelo de Decomposição')
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Decomposição Multiplicativa:</span> Série temporal modelada como o produto dos componentes de tendência, sazonalidade e resíduos. Útil quando a variação sazonal muda proporcionalmente com o nível da série temporal.</p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Decomposição Aditiva:</span> Série temporal modelada como a soma dos componentes de tendência, sazonalidade e resíduos. Útil quando variação sazonal é aproximadamente constante ao longo do tempo.</p>', unsafe_allow_html = True)

st.subheader('Período Sazonal')
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Sazonalidade diária:</span> Análise das variações diárias utilizando o parâmetro period=1.</p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Sazonalidade semanal:</span> Padrões que se repetem semanalmente. Por exemplo, em dados de tráfego da web, pode haver flutuações sazonais dependendo do dia da semana. O período sazonal associado seria 7 dias.</p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Sazonalidade mensal:</span> Variações que ocorrem a cada mês. Muitos fenômenos naturais e comportamentais exibem sazonalidade mensal, como vendas sazonais em certas indústrias, flutuações na demanda por energia elétrica, etc. O período sazonal associado seria 30 dias (em média).</p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Sazonalidade anual:</span> Padrões que se repetem anualmente. Por exemplo, em dados climáticos, podemos observar variações sazonais nas temperaturas ao longo das estações do ano. O período sazonal associado seria 365 dias.</p>', unsafe_allow_html = True)

# Leitura dos dados de petróleo gravados no BigQuery
tabela_bq = 'tb_preco_petroleo'
dados = select_bq(tabela_bq)

# Agrupamento dos dados em semanal, mensal e diário
df_semanal = dados.resample('W')['Preco'].mean()
df_mensal = dados.resample('M')['Preco'].mean()
df_anual = dados.resample('Y')['Preco'].mean()

# Seleção do modelo de decomposição e período sazonal
modelo = st.sidebar.selectbox("Selecione o modelo de decomposição", ['Multiplicativo','Aditivo'])
formato = st.sidebar.selectbox("Selecione o período sazonal", ['1','7','30','365'])

# Para cada combinação de seleção, é apresentado as análises de decomposição, teste estatístico e gráficos de autocorrelação
if (modelo == 'Multiplicativo' and formato == '1'):
    st.markdown('<h2> Sazonalidade diária com decomposição multiplicativa </h2>', unsafe_allow_html = True)
    result_mult_diaria = seasonal_decompose(dados, period = 1, model='multiplicative')
    decomposicao(dados,result_mult_diaria)
    string_teste = 'Resultado referente aos dados diários do preço do petróleo:'
    teste_estatistico(dados,string_teste)
    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Séries Temporais Diárias:</span> Para séries temporais diárias, podem ser observados lags significativos no ACF e PACF em torno de múltiplos de 7 (uma semana), indicando padrões semanais de autocorrelação devido a comportamentos repetitivos que ocorrem a cada semana. Além disso, para séries temporais diárias, também podem ser observados lags significativos em torno de 30 (um mês), indicando padrões mensais de autocorrelação.</p>', unsafe_allow_html = True)

elif (modelo == 'Aditivo' and formato == '1'):
    st.markdown('<h2> Sazonalidade diária com decomposição aditiva </h2>', unsafe_allow_html = True)
    result_adit_diaria = seasonal_decompose(dados, period = 1, model='aditive')
    decomposicao(dados,result_adit_diaria)   
    string_teste = 'Resultado referente aos dados diários do preço do petróleo:'
    teste_estatistico(dados,string_teste)
    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Séries Temporais Diárias:</span> Para séries temporais diárias, podem ser observados lags significativos no ACF e PACF em torno de múltiplos de 7 (uma semana), indicando padrões semanais de autocorrelação devido a comportamentos repetitivos que ocorrem a cada semana. Além disso, para séries temporais diárias, também podem ser observados lags significativos em torno de 30 (um mês), indicando padrões mensais de autocorrelação.</p>', unsafe_allow_html = True)

elif (modelo == 'Multiplicativo' and formato == '7'):
    st.markdown('<h2> Sazonalidade semanal com decomposição multiplicativa </h2>', unsafe_allow_html = True)
    result_mult_diaria = seasonal_decompose(dados, period = 7, model='multiplicative')
    decomposicao(dados,result_mult_diaria)
    string_teste = 'Resultado referente a média semanal do preço do petróleo:'
    teste_estatistico(df_semanal,string_teste)
    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Séries Temporais Semanais:</span> Para séries temporais semanais, podem ser observados lags significativos no ACF e PACF em torno de múltiplos de 4 (um mês), indicando padrões mensais de autocorrelação. Além disso, lags em torno de 52 (um ano) podem ser observados para capturar padrões anuais de autocorrelação.</p>', unsafe_allow_html = True)

elif (modelo == 'Aditivo' and formato == '7'):
    st.markdown('<h2> Sazonalidade semanal com decomposição aditiva </h2>', unsafe_allow_html = True)
    result_adit_diaria = seasonal_decompose(dados, period = 7, model='aditive')
    decomposicao(dados,result_adit_diaria)
    string_teste = 'Resultado referente a média semanal do preço do petróleo:'
    teste_estatistico(df_semanal,string_teste)
    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Séries Temporais Semanais:</span> Para séries temporais semanais, podem ser observados lags significativos no ACF e PACF em torno de múltiplos de 4 (um mês), indicando padrões mensais de autocorrelação. Além disso, lags em torno de 52 (um ano) podem ser observados para capturar padrões anuais de autocorrelação.</p>', unsafe_allow_html = True)

elif (modelo == 'Multiplicativo' and formato == '30'):
    st.markdown('<h2> Sazonalidade mensal com decomposição multiplicativa </h2>', unsafe_allow_html = True)
    result_mult_diaria = seasonal_decompose(dados, period = 30, model='multiplicative')
    decomposicao(dados,result_mult_diaria)
    string_teste = 'Resultado referente a média mensal do preço do petróleo:'
    teste_estatistico(df_mensal,string_teste)
    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Séries Temporais Mensais:</span> Para séries temporais mensais, lags em torno de 12 (um ano) podem ser frequentemente ressaltados no ACF e PACF, indicando padrões anuais de autocorrelação. Além disso, para séries mensais, também podem ser observados lags em torno de 6 (meio ano) devido a sazonalidades semestrais.</p>', unsafe_allow_html = True)

elif (modelo == 'Aditivo' and formato == '30'):
    st.markdown('<h2> Sazonalidade mensal com decomposição aditiva </h2>', unsafe_allow_html = True)
    result_adit_diaria = seasonal_decompose(dados, period = 30, model='aditive')
    decomposicao(dados,result_adit_diaria) 
    string_teste = 'Resultado referente a média mensal do preço do petróleo:'
    teste_estatistico(df_mensal,string_teste)
    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Séries Temporais Mensais:</span> Para séries temporais mensais, lags em torno de 12 (um ano) podem ser frequentemente ressaltados no ACF e PACF, indicando padrões anuais de autocorrelação. Além disso, para séries mensais, também podem ser observados lags em torno de 6 (meio ano) devido a sazonalidades semestrais.</p>', unsafe_allow_html = True)

elif (modelo == 'Multiplicativo' and formato == '365'):
    st.markdown('<h2> Sazonalidade anual com decomposição multiplicativa </h2>', unsafe_allow_html = True)
    result_mult_diaria = seasonal_decompose(dados, period = 365, model='multiplicative')
    decomposicao(dados,result_mult_diaria)
    string_teste = 'Resultado referente a média anual do preço do petróleo:'
    teste_estatistico(df_anual,string_teste)
    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Séries Temporais Anuais:</span> Para séries temporais anuais, podem ser observados lags em torno de 1 (um ano) no ACF e PACF, indicando autocorrelação anual. Além disso, podem ser observados lags em torno de 5 (cinco anos) para capturar padrões de autocorrelação de longo prazo. </p>', unsafe_allow_html = True)

elif (modelo == 'Aditivo' and formato == '365'):
    st.markdown('<h2> Sazonalidade anual com decomposição aditiva </h2>', unsafe_allow_html = True)
    result_adit_diaria = seasonal_decompose(dados, period = 365, model='aditive')
    decomposicao(dados,result_adit_diaria)
    string_teste = 'Resultado referente a média anual do preço do petróleo:'
    teste_estatistico(df_anual,string_teste)
    st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Séries Temporais Anuais:</span> Para séries temporais anuais, podem ser observados lags em torno de 1 (um ano) no ACF e PACF, indicando autocorrelação anual. Além disso, podem ser observados lags em torno de 5 (cinco anos) para capturar padrões de autocorrelação de longo prazo. </p>', unsafe_allow_html = True)