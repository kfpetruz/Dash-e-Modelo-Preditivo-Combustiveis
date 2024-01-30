# Importação das bibliotecas
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pickle
from utils import select_bq,modelo_ets_perfomance,dias_uteis_futuros,modelo_ets_previsao

# Configuração da página
st.set_page_config(page_title= 'Modelo - Predição', layout='wide', page_icon= ':fuelpump:')

# Título da página e descrição introdutória do modelo escolhido, parâmetros e performance
st.title('Modelo Preditivo :telescope:')

st.markdown('<p style="text-align: justify;">Considerando que os dados apresentaram uma leve repetição sazonal a cada intervalo de 30 dias, optamos por utilizar o modelo <span style="font-weight: bold">ETS (Erro, Tendência, Sazonalidade)</span>. O modelo ETS é adequado para séries temporais com características variáveis no tempo, permitindo a captura de padrões complexos mesmo em situações onde as tendências e sazonalidades são mínimas. Além disso, o modelo ETS oferece uma estrutura flexível que pode ser adaptada para se ajustar às particularidades dos dados, garantindo uma modelagem precisa e robusta.</p>', unsafe_allow_html = True)

st.header('Parâmetros')
st.markdown('<p style="text-align: justify;">ETS é um modelo de séries temporais que descreve a evolução de uma variável ao longo do tempo, levando em consideração três parâmetros principais: tendência, sazonalidade e períodos sazonais.  </p>', unsafe_allow_html = True)
st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Tendência (trend):</span> O parâmetro "trend" determina como a tendência é modelada no modelo ETS. Existem duas opções para a tendência:</p>', unsafe_allow_html = True)
st.markdown('* "add" ou "additive": Indica que a tendência é aditiva, ou seja, a variação da tendência é constante ao longo do tempo.', unsafe_allow_html = True)
st.markdown('* "mul" ou "multiplicative": Indica que a tendência é multiplicativa, o que significa que a variação da tendência é proporcional ao nível da série temporal.', unsafe_allow_html = True)

st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Sazonalidade (seasonal):</span> O parâmetro "seasonal" determina como a sazonalidade é modelada no modelo ETS. Assim como com a tendência, existem duas opções para a sazonalidade:</p>', unsafe_allow_html = True)
st.markdown('* "add" ou "additive": Indica que a sazonalidade é aditiva, ou seja, a variação sazonal é constante ao longo do tempo.', unsafe_allow_html = True)
st.markdown('* "mul" ou "multiplicative": Indica que a sazonalidade é multiplicativa, o que significa que a variação sazonal é proporcional ao nível da série temporal.', unsafe_allow_html = True)

st.markdown('<p style="text-align: justify;"><span style="font-weight: bold">Períodos Sazonais (seasonal_periods):</span> O parâmetro "seasonal_periods" indica o número de períodos em uma temporada ou ciclo sazonal.</p>', unsafe_allow_html = True) 
st.markdown('Por exemplo, se os dados forem diários e houver uma sazonalidade mensal, o número de períodos sazonais seria 30.', unsafe_allow_html = True)

st.header('Performance do Modelo')
st.markdown('<p style="text-align: justify;">Para a divisão dos dados em treinamento e teste foi utilizado o <span style="font-weight: bold">TimeSeriesSplit</span>, uma técnica de validação cruzada especializada para séries temporais. O TimeSeriesSplit divide os dados em conjuntos de treinamento e teste mantendo a ordem temporal. Ao avaliar o modelo em múltiplas divisões temporais, você obtém uma estimativa mais robusta do desempenho médio do modelo ao longo do tempo. Isso pode ajudar a reduzir o viés de avaliação e fornecer uma avaliação mais confiável do modelo.</p>', unsafe_allow_html = True) 
st.markdown('Além disso, é possível comparar as diferentes combinações de parâmetros do modelo e avaliar seu desempenho em termos de <span style="font-weight: bold">Erro Médio Absoluto(MAE)</span> ao longo do tempo em diferentes períodos, ajudando a selecionar o resultado mais robusto e generalizável para a série temporal.', unsafe_allow_html = True)

# Leitura dos dados de petróleo gravados no BigQuery
tabela_bq = 'tb_preco_petroleo'
dados = select_bq(tabela_bq)

# Leitura do arquivo pickle com a função do modelo de previsão
with open('modelo_ets.pkl', 'rb') as arquivo:
    modelo_carregado = pickle.load(arquivo)
arquivo.close()

# Apresentação do melhor resultado do modelo comparando o erro da base de teste e dados previstos
st.header('Melhor Resultado do Treino e Teste')

# Possibilidade de escolher a quantidade de dias que deseja usar no modelo de treino e teste, mínimo de 90 dias para melhor performance
qt_dias_treino_teste = st.number_input("Escolha a quantidade de dias mais recentes para utilizar no treino e teste do modelo:", min_value=90, max_value=len(dados), value=180)
st.markdown(f'Resultado destacado com o menor erro alcançado para **{qt_dias_treino_teste} dias** históricos, comparando dados de teste e dados previstos:', unsafe_allow_html = True)

# Função criada para treinar e testar os dados
melhor_mae, melhores_parametros, melhores_dados_teste, melhores_dados_treinamento, fit_train, melhor_wmape, df_completo = modelo_ets_perfomance(dados,qt_dias_treino_teste)

cor_estilizada = 'color: #0145AC;'
fonte_negrito = 'font-weight: bold;'

# Apresentação em colunas ou cartões as informações do melhor resultado: 
# data inicial e final da análise, qtd de dias treinados e testados menor MAE encontrado, WMAPE, parâmetros de tendência e sazonalidade
col1, col2, col3, col4 = st.columns(4)
with col1:
    metric1 = melhores_dados_treinamento.index.min().strftime('%d/%m/%Y')
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric1}</h2> <span style='{fonte_negrito}'> Data inicial da análise </span>", unsafe_allow_html=True)
    metric2 = melhor_mae.round(2)
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric2}</h2> <span style='{fonte_negrito}'> Menor MAE </span>", unsafe_allow_html=True)
with col2:
    metric3 = melhores_dados_teste.index.max().strftime('%d/%m/%Y')
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric3}</h2> <span style='{fonte_negrito}'> Data final da análise </span>", unsafe_allow_html=True)
    metric4 = f'{melhor_wmape:.2%}'
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric4}</h2> <span style='{fonte_negrito}'> WMAPE </span>", unsafe_allow_html=True)
with col3:
    metric5 = len(melhores_dados_treinamento)
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric5}</h2> <span style='{fonte_negrito}'> Qtd dias treinados </span>", unsafe_allow_html=True)
    metric6 = melhores_parametros['trend']
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric6}</h2> <span style='{fonte_negrito}'> Tendência </span>", unsafe_allow_html=True)
with col4:
    metric7 = len(melhores_dados_teste)
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric7}</h2> <span style='{fonte_negrito}'> Qtd dias testados </span>", unsafe_allow_html=True)
    metric8 = melhores_parametros['seasonal']
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric8}</h2> <span style='{fonte_negrito}'> Sazonalidade </span>", unsafe_allow_html=True)

# Construção do gráfico de comparação entre os dados treinados, testados e previstos 
fig = go.Figure()
fig.add_trace(go.Scatter(x=melhores_dados_treinamento.index.to_numpy(), y=melhores_dados_treinamento['Preco'].to_numpy(), mode='lines', name='Dados de Treino'))
fig.add_trace(go.Scatter(x=melhores_dados_teste.index.to_numpy(), y=melhores_dados_teste['Preco'].to_numpy(), mode='lines', name='Dados de Teste'))
fig.add_trace(go.Scatter(x=melhores_dados_teste.index.to_numpy(), y=fit_train.forecast(metric7).to_numpy(), mode='lines', name='Dados de Previsão do modelo',line=dict(color='red')))
fig.update_layout(title= 'Comparação entre os dados de teste com o resultado da previsão do modelo',
  xaxis_title='Data',
  yaxis_title='Preço (US$)')
st.plotly_chart(fig, use_container_width=True)

# Visualização de todos os resultados que o modelo conseguiu chegar, trocando os parâmetros 
with st.expander("Visualizar todos os resultados"):
    st.write(df_completo)

# Prever os dias levando em consideração a quantidade de dias recentes que deseja treinar e, os parâmetros do modelo
st.header('Previsão') 

# Atribuindo índice para os parâmetros, para que o valor padrão da previsão, seja o resultado do modelo de treino e teste
biblioteca_indice = {
    'additive': 0,
    'multiplicative': 1
}

indice_tendencia = biblioteca_indice[metric6]
indice_sazonalidade = biblioteca_indice[metric8]

# Introdução sobre construção do modelo
st.markdown('<p style="text-align: justify;"> O modelo de previsão foi persistido em um arquivo serializável com auxílio do módulo Python chamado <span style="font-weight: bold">Pickle</span>, essa prática pode trazer eficiência para o resultado e, é facilmente integrado com outras ferramentas e sistemas. A seguir, selecione os parâmetros necessários para a previsão, os quais são pré-determinados com base nos resultados do treinamento e teste mencionados anteriormente.</p>', unsafe_allow_html = True)

# Parâmetros dinâmicos, considerados para prever a quantidade de dias desejado, tendo como padrão o resultado do modelo de treino e teste
col1, col2, col3, col4 = st.columns(4)
with col1:
    qt_dias_historicos = st.number_input("Qtd de dias para treino do modelo:", min_value=60, max_value=len(dados), value=metric5)
with col2:
    qt_dias_prever = st.number_input("Qtd de dias previsão:", min_value=0, max_value=len(dados), value=metric7)
with col3:
    opcao_tendencia = st.selectbox("Tendência:", ['additive','multiplicative'], index=indice_tendencia)
with col4:
    opcao_sazonalidade = st.selectbox("Sazonalidade:", ['additive','multiplicative'], index = indice_sazonalidade)

# Carregar a função do modelo de previsão
forecasting = modelo_carregado(dados, qt_dias_historicos, qt_dias_prever, opcao_tendencia, opcao_sazonalidade)

# Criação de um data frame para juntar os dados previstos e os dias futuros
df_forecasting = pd.DataFrame()

# Função criada para gerar os dias futuros, a partir da data máxima da base de dados
dias_futuros = dias_uteis_futuros(dados.index.max(),qt_dias_prever)
df_forecasting['Data'] = dias_futuros
df_forecasting['Preco'] = forecasting.reset_index(drop=True)

# Transformando a data em índice do novo data frame
df_forecasting['Data'] = pd.to_datetime(df_forecasting['Data'], format = '%d/%m/%Y')
df_forecasting.set_index('Data', inplace = True)

# Selecionando o preço mínimo previsto e sua respectiva data
preco_min = df_forecasting['Preco'].min()
data_preco_min = df_forecasting[df_forecasting['Preco']==preco_min].index

# Selecionando o preço máximo previsto e sua respectiva data
preco_max = df_forecasting['Preco'].max()
data_preco_max = df_forecasting[df_forecasting['Preco']==preco_max].index

# Apresentação dos dados dividos em colunas, como se fossem cartões do maior e menos preço previstos, e suas respectivas datas
col1, col2, col3, col4 = st.columns(4)
with col1:
    metric9 = data_preco_max[0].strftime('%d/%m/%Y')
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric9}</h2> <span style='{fonte_negrito}'> Data prevista de maior pico </span>", unsafe_allow_html=True)
with col2:
    metric10 = preco_max
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric10:.2f}</h2> <span style='{fonte_negrito}'> Valor do maior pico </span>", unsafe_allow_html=True)
with col3:
    metric11 = data_preco_min[0].strftime('%d/%m/%Y')
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric11}</h2> <span style='{fonte_negrito}'> Data prevista de menor pico </span>", unsafe_allow_html=True)
with col4:
    metric12 = preco_min
    st.markdown(f"<h2 style='{cor_estilizada}'>{metric12:.2f}</h2> <span style='{fonte_negrito}'> Valor do menor pico </span>", unsafe_allow_html=True)

# Construção do gráfico mostrando os dados treinados e previstos 
fig = go.Figure()
fig.add_trace(go.Scatter(x=dados.tail(qt_dias_historicos).index.to_numpy(), y=dados.tail(qt_dias_historicos)['Preco'].to_numpy(), mode='lines', name='Dados de Treino'))
fig.add_trace(go.Scatter(x=dias_futuros, y=forecasting.to_numpy(), mode='lines', name='Dados de Previsão do modelo',line=dict(color='red')))
titulo = f'Previsão de preço para {qt_dias_prever} dias com base em treino {qt_dias_historicos} dias'
fig.update_layout(title= titulo,
  xaxis_title='Data',
  yaxis_title='Preço (US$)')
st.plotly_chart(fig, use_container_width=True)

# Visualização dos dias e preços previstos
with st.expander("Visualizar preços previstos"):
    st.write(df_forecasting.reset_index())
