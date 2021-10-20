import pandas as pd
import mysql.connector
import streamlit as st
import time

from funcoes.cadastro import SENHA
from funcoes.cadastro import selecionar_registro

# Conexão do Banco de dados
mydb = mysql.connector.connect(
  host="localhost",
  user="root", #alterar a constante SENHA apenas no módulo 'cadastro.py'
  password=SENHA,
  database="pji"
)

#Funções relativas a rotinas de alteração e atualização

def update_aluno(resultado):
    with st.form(key ='form_aluno'):

        #RA
        st.write('Registro do(a) Aluno(a) (RA):')
        st.warning(resultado[0][0])
        ra = resultado[0][0]
        #Nome
        nome = st.text_input(label='Nome do(a) Aluno(a):',value=resultado[0][1], max_chars=200)

        col1, col2 = st.columns(2)
        with col1:
            if resultado[0][2] == 'F':
                index = 1
            elif resultado[0][2] == 'M':
                index = 2
            else:
                index = 0
            #Sexost.selectbox('Sexo: Feminino (F) ou Masculino (M)', ('','F','M'))
            sexo = st.selectbox('Sexo: Feminino (F) ou Masculino (M)',('','F','M'),index=index)

            #CPF
            cpf = st.text_input(label='CPF:',value=resultado[0][3], max_chars=11)

            #RG
            rg = st.text_input(label='RG:',value=resultado[0][4], max_chars=45)

            # Data de nascimento
            nascimento = st.date_input(label='Data de nascimento do(a) Aluno(a):',value=resultado[0][7])

        with col2:
            #Telefone
            telefone = st.text_input(label='Telefone:',value=resultado[0][5], max_chars=20)

            # Série (O preenchimento deste campo está gerando erros)
            SALA_serie = st.text_input('Série:',value=resultado[0][8], max_chars=1)

            #Turma (O preenchimento deste campo está gerando erros)
            SALA_turma = st.text_input('Turma',value=resultado[0][9], max_chars=1)

            # Responsável (o nome dessa coluna no Banco de Dados consta como 'resposavel'
            responsavel = st.text_input(label='Nome do(a) Responsável pelo(a) Aluno(a):',value=resultado[0][6], max_chars=200)

        button_new_aluno = st.form_submit_button(label='ATUALIZAR CADASTRO')

        if (button_new_aluno):
            mycursor = mydb.cursor()
            sql = "REPLACE INTO ALUNO (ra, nome, sexo, cpf, rg, telefone, resposavel, nascimento, SALA_serie, SALA_turma) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (ra, nome, sexo, cpf, rg, telefone, responsavel, nascimento, SALA_serie, SALA_turma)
            mycursor.execute(sql, val)
            mydb.commit()

            with st.spinner('Cadastro atualizado com sucesso!'):
                time.sleep(3)
                st.success('Cadastro atualizado: '+nome+', RA: '+ra)

def tela_cadastro_update_aluno():
    st.subheader("Atualização de Cadastro")
    st.write("Pesquise o cadastro dos alunos por Nome ou RA:")
    atualizar_aluno = selecionar_registro('aluno','nome','nome','ra',1,235)
    if atualizar_aluno is not None:
        update_aluno(atualizar_aluno)

def update_livro(resultado):
    with st.form(key='form_update_livro'):
        st.subheader("ATUALIZAR VOLUMES CADASTRADOS")
        st.write("Tombo: ")
        st.warning(resultado[0][0])
        tombo = resultado[0][0]

        titulo = st.text_input(label='Título', value=resultado[0][1], max_chars=200)
        col1, col2 = st.columns(2)
        with col1:

            autor = st.text_input(label='Nome do(a) Autor(a)', value=resultado[0][2], max_chars=100)

            editora = st.text_input(label='Editora', value=resultado[0][3], max_chars=100)

            edicao = st.text_input(label='Edição', value=resultado[0][4], max_chars=50)
        with col2:

            ano_edicao = st.number_input(label='Ano da edição', value=resultado[0][5], min_value=1900, max_value=2099)

            isbn = st.text_input(label='Número ISBN - 13 dígitos', value=resultado[0][6], max_chars=13)

            genero = st.text_input(label='Gênero', value=resultado[0][7], max_chars=30)

        prateleira = st.text_input(label='Prateleira', value=resultado[0][8], max_chars=30)

        button_update_livro = st.form_submit_button(label='ATUALIZAR 📘')

        if button_update_livro:
            mycursor = mydb.cursor()
            sql = f"""
                UPDATE LIVRO SET titulo='{titulo}', autor='{autor}', editora='{editora}', 
                edicao='{edicao}', ano_edicao='{ano_edicao}', ISBN='{isbn}', genero='{genero}', Prateleira='{prateleira}' 
                WHERE n_tombo = '{tombo}'
                """
            mycursor.execute(sql)
            mydb.commit()
            st.success("Livro atualizado com sucesso!")

def tela_cadastro_update_livro():
    st.subheader("Atualização dos Livros Cadastrados")
    st.write("Pesquise o cadastro dos livros por título, autor ou número de tombo:")
    atualizar_livro = selecionar_registro('livro','titulo','autor','n_tombo',1,478)
    if atualizar_livro is not None:
        update_livro(atualizar_livro)

def upload_alunos():
#Função para fazer o upload de uma lista de alunos em formato csv padronizado
    upload_lista_alunos = st.file_uploader("Escolha o arquivo contendo a lista de alunos")
    st.write(upload_lista_alunos)
    if upload_lista_alunos is not None:
        dataframe = pd.read_csv(upload_lista_alunos,header=None)
        st.dataframe(dataframe)

        mycursor = mydb.cursor()

        for i in range(1,len(dataframe)-1):

            sql = f'''REPLACE INTO pji.ALUNO 
                (
                    ra, nome, sexo, 
                    cpf, rg, telefone, 
                    resposavel, nascimento, SALA_serie, 
                    SALA_turma
                )
                VALUES (
                    '{dataframe[0][i]}','{dataframe[1][i]}','{dataframe[2][i]}',
                    '{dataframe[3][i]}','{dataframe[4][i]}','{dataframe[5][i]}',
                    '{dataframe[6][i]}','{dataframe[7][i]}','',
                    ''
                )
                '''

            mycursor.execute(sql)
            mydb.commit()
        st.success("Dados carregados com sucesso!")


