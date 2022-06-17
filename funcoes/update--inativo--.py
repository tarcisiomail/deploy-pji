import pandas as pd
import mysql.connector
import streamlit as st
import time

# Conexão do Banco de dados
mydb = psycopg2.connect(
    database="deg4do58nvsta5",
    user="nvhkstpynbzgqi",
    password="b4288fbb1fbc757e60e9aba5e362828464e2a36db1a54d2f9cb3903f2b0b6dc5",
    host="ec2-52-204-195-41.compute-1.amazonaws.com",
    port="5432")

def selecionar_registro(tabela, coluna1, coluna2, coluna3, coluna_exibida, key):
    pesquisa = st.text_input(label='', key=key, help='Digite um termo para sua pesquisa:')
    if pesquisa != '':
        mycursor = mydb.cursor()
        sql = mycursor.execute(
            f"SELECT * FROM {tabela} WHERE ({coluna1} LIKE '%{pesquisa}%' OR {coluna2} LIKE '%{pesquisa}%' OR {coluna3} LIKE '%{pesquisa}%')")
        mycursor.execute(sql)
        resultado = mycursor.fetchall()
        mydb.commit()

        if len(resultado) == 1:
            st.write('Registro selecionado: ', resultado[0][0])

            return resultado
        elif len(resultado) > 1:
            options = list()
            options.append("...")
            for i in range(len(resultado)):
                options.append(resultado[i][coluna_exibida])

            select_reg = st.selectbox("", options)

            mycursor = mydb.cursor()
            mycursor.execute(
                f"SELECT * FROM {tabela} WHERE ({coluna1} LIKE '%{select_reg}%' OR {coluna2} LIKE '%{select_reg}%')")
            resultado = mycursor.fetchall()
            if select_reg != "...":
                return resultado

        else:
            st.error('Nenhum resultado encontrado!')


#Funções relativas a rotinas de alteração e atualização

def update_aluno(resultado):
    with st.form(key ='form_aluno'):

        #RA
        st.write('Registro do(a) Aluno(a) (RA):')
        st.warning(resultado[0][0])
        ra = resultado[0][0]
        #Nome
        nome = st.text_input(label='Nome do(a) Aluno(a):',value=resultado[0][1], max_chars=200)

        # Série (O preenchimento deste campo está gerando erros)
        ano = st.text_input('Ano:',value=resultado[0][2], max_chars=1)

        #Turma (O preenchimento deste campo está gerando erros)
        turma = st.text_input('Turma',value=resultado[0][3], max_chars=1)

        button_new_aluno = st.form_submit_button(label='ATUALIZAR CADASTRO')

        if (button_new_aluno):
            mycursor = mydb.cursor()
            sql = "REPLACE INTO ALUNO (ra, nome, ano, turma) VALUES (%s, %s, %s, %s)"
            val = (ra, nome, ano, turma)
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
    st.subheader("Carregar lista de alunos")
    st.write('''
        INSTRUÇÕES:  \n
        1. A planilha deve conter apenas as seguintes 04 colunas:  \n
           1.1 Registro de aluno (RA) / Código EOL;  \n
           1.2 Nome;  \n
           1.3 Ano;  \n
           1.4 Turma.  \n
        2. Salve a planilha como CSV (separado por vírgulas);  \n
        3. A primeira linha da planilha será ignorada.
    ''')
    upload_lista_alunos = st.file_uploader("Escolha o arquivo contendo a lista de alunos")
    st.write(upload_lista_alunos)
    if upload_lista_alunos is not None:
        upload_button = st.button('Atualizar lista de alunos')

        dataframe = pd.read_csv(upload_lista_alunos,header=None,sep=';')
        if len(dataframe.columns) < 4:
            dataframe = pd.read_csv(upload_lista_alunos, header=None, sep=',')
        st.dataframe(dataframe)
        if upload_button:
            mycursor = mydb.cursor()

            for i in range(1,len(dataframe)):

                sql = f'''REPLACE INTO pji.ALUNO 
                    (
                        ra, nome, ano, turma
                    )
                    VALUES (
                        '{dataframe[0][i]}','{dataframe[1][i]}','{dataframe[2][i]}',
                        '{dataframe[3][i]}'
                    )
                    '''

                mycursor.execute(sql)
                mydb.commit()
            st.success("Dados carregados com sucesso!")
