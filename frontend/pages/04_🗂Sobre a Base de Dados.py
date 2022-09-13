import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(
     page_title="Dropout Monitor",
     page_icon="🎓",
     layout="wide",
)

st.title('Sobre a Base de Dados')

st.markdown('## Da onde veio')
st.write("Os dados utilizados são os microdados do INEP da educação superior \
         brasileira dos anos de 2009 até 2019. Até o início do projeto esses \
         dados estavam disponíveis publicamente para download, um tempo depois \
         eles foram retirados do ar por conta de alegações de infringimento \
         da LGPD, muito embora os dados já estivessem anonimizados.")
st.markdown('## Filtros realizados')
st.markdown("#### Seleção temporal")
st.write("Para as análises presentes nesse dashboard e para a criação do modelo, \
          a base de dados utilizada variou dos anos de 2015 à 2019, visto que\
          estes anos possuiam a maior parte das variáveis utilizadas para a predição \
          preenchidas e o modelo apresentou melhores resultados por conta disso.")
st.markdown("#### Seleção de cursos")
st.write("Além disso, de todas as diversas áreas de conhecimento de cursos presentes \
     no INEP, este projeto filtrou apenas os dados de alunos de cursos de TI \
     sendo o crivo utilizado para definir quais são esses cursos o seguinte documento \
     governamental: [Manual para Classificação dos Cursos de Graduação e Sequenciais : Cine Brasil](https://www.gov.br/inep/pt-br/centrais-de-conteudo/acervo-linha-editorial/publicacoes-institucionais/estatisticas-e-indicadores-educacionais/manual-para-classificacao-dos-cursos-de-graduacao-e-sequenciais-cine-brasil)")
st.markdown('## Engenharia de Features')
st.markdown("#### Definição da variável *target*")
st.write("A variável target foi definida da seguinte forma:")
st.markdown("- São considerados como **Evadidos** alunos que: \
     Estão desvinculados do curso, estão com a matrícula trancada ou \
     foram transferidos para outro curso da mesma IES")
st.markdown("- São considerados como **Não Evadidos** alunos que: \
     Estão cursando ou estão formados")
st.write("A base argumentativa utilizada para a escolha foi o artigo: [Análise da evasão feminina nos cursos de Ciência da Computação das universidades públicas e presenciais de Santa Catarina](https://seer.ufrgs.br/index.php/renote/article/view/126669)")