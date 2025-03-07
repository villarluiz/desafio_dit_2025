# -*- coding: utf-8 -*-
"""desafio_dit.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vhJw2NumeShgBlj9Or2WaV0hThy5Eka6
"""

import pandas as pd  ## usando biblioteca pandas para explorar os dados
data = pd.read_csv("drive/MyDrive/Colab Notebooks/dados_ficha_a_desafio.csv") ## lendo o arquivo .csv via pandas
data.info() ## visualizando a dimensao e caracteristica de cada coluna

"""Como primeiro contato, podemos explorar as dimensoes do dataset: sao 35 variaveis para um total de 100.000 registros. Idealmente, teriamos todas as colunas preenchidas 100% sem objetos 'null' ou nulos, entretanto, para as variaveis 'identidade_genero', 'altura', 'peso', 'pressao_sistolica' e 'pressao_diastolica' encontramos registros em branco. Manteremos atençao a esses dados para futuras oportunidades de processamento. Podemos ver tambem que o dataset consiste em maioria de dados do tipo 'string' com poucas colunas identificadas como numeros 'int64/float64'.

"""

pd.set_option('display.max_columns', None) ## impedindo que o pandas encurte as colunas quando printar
data.head() ## visualizando algumas entradas para entender os registros, impedindo o encurtamento de colunas

"""Visualizando agora as primeiras entradas do dataset, podemos inferir alguns possíveis problemas que vamos investigar para avaliar a integridade dos dados:
- As colunas 'obito', 'luz_eletrica', 'em_situacao_de_rua', 'frequenta_escola', 'possui_plano_saude', 'vulnerabilidade_social', 'familia_beneficiaria_auxilio_brasil' e 'crianca_matriculada_creche_pre_escola' possuem entradas do tipo booleano 0 ou 1. Podemos ver que algumas dessas colunas possuem misturas com entradas 'True' e 'False', sendo necessário traduzir essas entradas para booleanos correspondentes (0 = False, 1 = True). Tambem sabemos que os dados dessas colunas, com excecao de 'frequenta_escola', estao como type 'object', que poderia ser tratado para 'int64' apos a traducao;
- Colunas com 'strings' como 'doencas_condicoes', 'meios_comunicacao', 'em_caso_doenca_procura' e 'em_caso_doenca_procura' denunciam a ma formatacao de inputs para essas variaveis, indicando a necessidade de investigar e aplicar formatacao para todas essas colunas;
- Registros de 'identidade_genero' como 'Nao' precisam ser investigadas se querem realmente dizer 'Nao informado';
- As variaveis 'altura' e 'peso' mostram algumas inconsistencias com uma pessoa medindo 53 centimetros e pesando 82 quilos (provavelmente um erro na altura, podendo estar em pes e polegadas por ex.) e uma pessoa com 154cm de altura e pesando apenas 8.5 quilos (muito provavelmente erro de casa decimal, 8.5 ao inves de 85.0);
"""

data.describe() ## visualizando dados numericos

"""Focando nos dados com entrada numérica, podemos ver que 'altura', 'peso', 'pressao_sistolica' e 'pressao_diastolica' possuem valores surreais apresentados nas categorias 'max' e 'min', como por exemplo uma pessoa com 810 centimetros de altura ou pressao sistolica de 900.

"""

## vetor de colunas de interesse e frequencia de valores unicos (nao-duplicados)
cols = ['sexo', 'bairro', 'raca_cor', 'religiao', 'escolaridade', 'nacionalidade', 'renda_familiar', 'meios_transporte', 'identidade_genero', 'meios_comunicacao', 'orientacao_sexual', 'em_caso_doenca_procura', 'situacao_profissional']
data[cols].nunique()

"""A partir da contagem das entradas unicas de algumas variaveis que ainda nao foram analisadas, podemos identificar colunas que tem um numero nao realista de respostas:
- Variaveis 'meios_comunicacao', 'meios_transporte' e 'em_caso_doenca_procura' sofrem do erro de formatacao do texto e descrevem, por exemplo, 655 formas de se locomover;
- Variaveis 'religiao', 'identidade de genero', 'escolaridade' e 'renda_familiar' podem conter mais entradas que o necessario para registro, como por exemplo duplicar resposta de '1 Salario' com '1 Salario minimo' (esse tipo de verificacao deve ser feito para todas as variaveis descritivas, mesmo que a contagem de valores unicos nao aponte erro a principio).
"""

data['religiao'].value_counts() ## valores unicos e frequencia de registro de cada entrada

"""Explorando primeiramente a variavel religiao, podemos ver que as entradas 'Nao' poderiam ser alocadas para 'Sem religiao' e algumas entradas diferentes do esperado sao encontradas ao final com baixissima frequencia."""

data['identidade_genero'].value_counts()

"""Explorando a variavel 'identidade_genero' agora, podemos ver que algo similar acontece: 'Nao' e 'Sim' sao entradas indesejaveis para essa coluna, bem como confundimento de identidade de genero com sexualidade, como visto pelas respostas 'Heterossexual' por exemplo.

Explorando agora algumas interacoes entre variaveis que podemos fazer, podemos verificar se 'data_nascimento' condiz com 'situacao_profissional' ou 'ocupacao' por exemplo:
"""

## filtrando as entradas com ate 10 anos de idade e explorando o cargo ocupacional
data.loc[data['data_nascimento'] > '2015-01-01', ['data_nascimento', 'situacao_profissional', 'ocupacao']]

"""Podemos ver que pessoas com ate 10 anos de idade estao registradas com 'Emprego Formal' ou com cargo, o que nao faz sentido e provavelmente e um confundimento entre o registro 'data_nascimento' com 'updated_at' ou 'data_atualizacao_cadastro'.

Dessa exploracao rapida da base de dados, podemos fazer as seguintes inferencias:
- As colunas com valores Booleanos precisam passar por testes para verificar que todas as entradas estao padronizadas (ou ate mesmo um tratamento rapido via python para garantir que todas as entradas sao do tipo 'int64' com valores 0 e 1);
- Algumas colunas descritivas possuem ma formatacao de texto, que inviabilisa analises mais profundas como por exemplo frequencia de meios de transporte utilizados pela populacao que e atendida nas unidades de saude;
- Variaveis 'altura', 'peso' e as medidas de pressao, por serem variaveis quantitativas, sofrem com erros de digitacao ou entao erros de conversao para a unidade de medida;
- As colunas descritivas, tambem, possuem algumas 'respostas livres' que acaba contaminando o dataset com entradas duplicadas ou entao erros de registro.

Algumas medidas que poderiam mitigar esses erros sao, respectivamente:
- As colunas booleanas poderiam ter uma restricao para impedir o registro de algum outro valor que fuja do padrao;
- Isso tambem vale para as colunas descritivas, que poderiam ser registradas sem a utilizacao de acentos para impedir a ma traducao entre sistemas operacionais;
- Medidas quantitativas poderiam ter um threshold de valores aceitaveis a depender da variavel (por exemplo maior peso que pode ser registrado como '600' kgs);
- Algumas colunas com 'resposta livre', como por exemplo 'identidade_genero' poderiam ser questionarios com opcoes fixas para diminuir o desentendimento entre o paciente e o coletador de dados.
"""