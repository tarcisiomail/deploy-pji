import psycopg2
import streamlit as st

# Funções feitas
from funcoes.cadastro import tela_cadastro_livro
from funcoes.cadastro import tela_cadastro_aluno
from funcoes.cadastro import tela_cadastro_emprestimo
from funcoes.cadastro import nada
from funcoes.cadastro import tela_novo_emprestimo
from funcoes.cadastro import tela_finalizar_emprestimo

from funcoes.consulta import tela_consulta_tabelas
from funcoes.consulta import tela_consulta_emprestimo
from funcoes.consulta import tela_consulta_atrasado
from funcoes.consulta import tela_consulta_livros
from funcoes.consulta import tela_consulta_aluno

from funcoes.update import upload_alunos
from funcoes.update import tela_cadastro_update_aluno
from funcoes.update import tela_cadastro_update_livro

# Conexão do Banco de dados
mydb = psycopg2.connect(
    database="dcj8rehkg575jt",
    user="mukyulukhffrky",
    password="1537728423988d4a4010276828a4e0f56798a783e3e044598e12ce421bd23fe4",
    host="ec2-3-214-136-47.compute-1.amazonaws.com",
    port="5432")

st.set_page_config(page_title='Sala de Leitura', page_icon=None, layout='centered', initial_sidebar_state='expanded', menu_items=None)

def gerar_string_tombo(tombo):
    x = str(tombo)
    y = (x[:-6] + '.' + (x[-6:-3]) + '.' + (x[-3:]))
    st.write(y)

def remove_point(x):
    y = x.replace('.', '')
    z = int(y)

# Parte que chama as Funções do Codigo
st.sidebar.subheader('CADASTRO')
tela_cadastro = st.sidebar.radio("Opções de cadastro e empréstimo", ("Empréstimo",
                                                                     "Novo Empréstimo",
                                                                     "Finalizar Empréstimo",
                                                                     "Livro",
                                                                     "Aluno",
                                                                     "Nenhuma ação"), index=5)

st.sidebar.subheader('CONSULTA')
tela_consulta = st.sidebar.radio("Opções de consultas", ("Empréstimos",
                                                         "Livros atrasados",
                                                         "Livros do acervo",
                                                         "Alunos",
                                                         "Tabelas",
                                                         "Nenhuma ação"), index=5)

st.sidebar.subheader('ATUALIZAÇÃO E MANUTENÇÃO')
tela_update = st.sidebar.radio("Opções de consultas", ("Alterar alunos",
                                                       "Alterar livros",
                                                       "Upload de lista de alunos",
                                                       "Upload de lista de livros",
                                                       "Nenhuma ação",), index=4)

# Condições para selecionar as telas de cadastro
if tela_cadastro == "Livro":
    tela_cadastro_livro()

if tela_cadastro == "Aluno":
    tela_cadastro_aluno()
if tela_cadastro == "Empréstimo":
    tela_cadastro_emprestimo()
if tela_cadastro == "Novo Empréstimo":
    tela_novo_emprestimo()
if tela_cadastro == "Finalizar Empréstimo":
    tela_finalizar_emprestimo()


if tela_cadastro == "Nenhuma ação":
    nada()

# Condições para selecionar as telas de consulta
if tela_consulta == "Tabelas":
    tela_consulta_tabelas()
if tela_consulta == "Empréstimos":
    tela_consulta_emprestimo()
if tela_consulta == "Livros atrasados":
    tela_consulta_atrasado()
if tela_consulta == "Livros do acervo":
    tela_consulta_livros()
if tela_consulta == "Alunos":
    tela_consulta_aluno()
if tela_consulta == "Nenhuma ação":
    nada()

# Condições para selecionar as telas de atualização
if tela_update == "Nenhuma ação":
    nada()
if tela_update == "Upload de lista de alunos":
    upload_alunos()
if tela_update == "Alterar alunos":
    tela_cadastro_update_aluno()
if tela_update == "Alterar livros":
    tela_cadastro_update_livro()
