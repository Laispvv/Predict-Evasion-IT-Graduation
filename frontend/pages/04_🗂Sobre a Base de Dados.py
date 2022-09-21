import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(
     page_title="Dropout Monitor",
     page_icon="🎓",
     layout="wide",
)

# all_features = Image.open("./frontend/pages/all_features.png")
all_features = Image.open("./frontend/pages/all_features.png")
final_features = Image.open('./frontend/pages/final_feature.png')

st.title('Sobre a Base de Dados')


st.markdown('## Da onde veio')
st.write("Os dados utilizados são os microdados do INEP da educação superior \
         brasileira dos anos de 2009 até 2019. Até o início do projeto esses \
         dados estavam disponíveis publicamente para download, um tempo depois \
         eles foram retirados do ar por conta de alegações de infringimento \
         da LGPD, muito embora os dados já estivessem anonimizados.")


st.markdown('## Filtros realizados')


st.markdown("#### Seleção temporal")
st.write("Para as análises presentes nesse dashboard, os dados datam de 2009 até 2019 \
          enquanto que para a criação do modelo, a base de dados utilizada variou \
          dos anos de 2015 à 2019, visto que estes anos possuiam a maior parte \
          das variáveis utilizadas para a predição \
          preenchidas e o modelo apresentou melhores resultados por conta disso.")


st.markdown("#### Seleção de cursos")
st.write("Além disso, de todas as diversas áreas de conhecimento de cursos presentes \
     no INEP, este projeto filtrou apenas os dados de alunos de cursos de TI \
     sendo o crivo utilizado para definir quais são esses cursos o seguinte documento \
     governamental: [Manual para Classificação dos Cursos de Graduação e Sequenciais : Cine Brasil](https://www.gov.br/inep/pt-br/centrais-de-conteudo/acervo-linha-editorial/publicacoes-institucionais/estatisticas-e-indicadores-educacionais/manual-para-classificacao-dos-cursos-de-graduacao-e-sequenciais-cine-brasil).")


st.markdown('## Engenharia de Features')


st.markdown("#### Definição da variável *target*")
st.write("A variável target foi definida da seguinte forma:")
st.markdown("- São considerados como **Evadidos** alunos que: \
     Estão desvinculados do curso, estão com a matrícula trancada ou \
     foram transferidos para outro curso da mesma IES")
st.markdown("- São considerados como **Não Evadidos** alunos que: \
     Estão cursando ou estão formados")
st.write("A base argumentativa utilizada para a escolha foi o artigo: [Análise da evasão feminina nos cursos de Ciência da Computação das universidades públicas e presenciais de Santa Catarina](https://seer.ufrgs.br/index.php/renote/article/view/126669)")


st.markdown("#### Limpeza dos dados")
st.write("O primeiro passo para a preparação do Dataset para as análises e treinamento do \
     modelo foi realizar a junção das bases filtradas com os filtros mencionados, \
     anteriormente, com o objetivo de trabalhar com os 10 anos de dados em uma única base.")
st.write("Após isso, depois de concatenada, features que apresentavam valores 100% nulos foram \
     removidas. Além disso, alguns conjuntos de features foram juntas em uma única, que resumem \
     elas. É o caso da feature que indica se o estudante é deficiente, se possui financiamento estudantil \
     reembolsável ou não, se possui bolsa de atividade extraclasse, entre outras. Por fim, criou-se \
     a feature ANOS_DESPENDIDOS, que diz respeito a quantos anos o aluno está no curso atual.")


st.markdown("#### Seleção de Features para o Modelo")
st.write("Após a limpeza, testamos diversos modelos com a base de dados limpa, e verificamos a \
     importância das features para cada modelo. Abaixo está a imagem da importância das features para \
     o modelo LightGBM, que foi o modelo escolhido por apresentar os melhores resultados, conforme \
     descrito na seção 'Sobre o Modelo'.")
st.image(all_features, caption='Imagem da importância de cada feature para o modelo LightGBM')
st.write("De posse dessa informação, escolhemos as variáveis utilizadas para a modelagem de forma que \
a menor quantidade possível de variáveis fosse selecionada sem perder a capacidade preditiva do modelo. \
Além disso, foram priorizadas as variáveis que lidavam com dados mais acessíveis e menos sensíveis dos alunos, de modo \
a facilitar o preenchimento das features pelo docente ou responsável administrativo que utilizar a ferramenta, sem ferir \
a privacidade do aluno. Desta forma, a imagem abaixo apresenta o conjunto de features finais selecionadas.")
st.image(final_features, caption='Imagem da importância das features selecionadas para o modelo LightGBM')
