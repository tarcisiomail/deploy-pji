import pandas as pd
import streamlit as st
import mysql.connector
from datetime import datetime, timedelta, date
import time


SENHA = 'root'  # alterar a senha apenas aqui, entre aspas

# Conexão do Banco de dados
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=SENHA,  # alterar a constante SENHA, acima
    database="pji"
)


def consultar_banco(sql):
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    x = mycursor.fetchall()
    mydb.close()
    return x


def alterar_banco(sql, val):
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()


# Função para exibir o formulário de cadastro de livros
def tela_cadastro_livro():
    with st.form(key='form_livro', clear_on_submit=True):
        st.subheader("CADASTRAR NOVO VOLUME")

        # Tombo
        tombo = st.text_input(label='Tombo', max_chars=15)

        # Título
        titulo = st.text_input(label='Título', max_chars=200)
        col1, col2 = st.columns(2)
        with col1:
            # Autor
            autor = st.text_input(label='Nome do(a) Autor(a)', max_chars=100)

            # Editora
            editora = st.text_input(label='Editora', max_chars=100)

            # Edição
            edicao = st.text_input(label='Edição', max_chars=50)
        with col2:
            # Ano da Edição
            ano_edicao = st.number_input(label='Ano da edição', min_value=1900, max_value=2099)

            # ISBN
            isbn = st.text_input(label='Número ISBN - 13 dígitos', max_chars=13)

            # Gênero
            genero = st.text_input(label='Gênero', max_chars=30)

        # Prateleira
        prateleira = st.text_input(label='Prateleira', max_chars=30)

        button_new_livro = st.form_submit_button(label='CADASTRAR 📘')

        if button_new_livro:
            mycursor = mydb.cursor()
            sql = f"""
            INSERT INTO LIVRO (n_tombo, titulo, autor, editora, edicao, ano_edicao, ISBN, genero, Prateleira) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            val = (tombo, titulo, autor, editora, edicao, ano_edicao, isbn, genero, prateleira)
            mycursor.execute(sql, val)
            mydb.commit()


# Função para exibir o formulário de cadastro de alunos
def tela_cadastro_aluno():
    with st.form(key='form_aluno',clear_on_submit=True):
        st.subheader('CADASTRAR ALUNO(A)')

        # RA
        ra = st.text_input(label='Registro do(a) Aluno(a) (RA):', max_chars=8)

        # Nome
        nome = st.text_input(label='Nome do(a) Aluno(a):', max_chars=200)
        col1, col2 = st.columns(2)
        with col1:
            # Sexo
            sexo = st.text_input(label='Sexo: Feminino (F) ou Masculino (M)', max_chars=1)

            # CPF
            cpf = st.text_input(label='CPF:', max_chars=11)

            # RG
            rg = st.text_input(label='RG:', max_chars=45)

            # Data de nascimento
            nascimento = st.date_input(label='Data de nascimento do(a) Aluno(a):')

        with col2:
            # Telefone
            telefone = st.text_input(label='Telefone:', max_chars=20)

            # Série (O preenchimento deste campo está gerando erros)
            SALA_serie = st.text_input('Série:', max_chars=1)

            # Turma (O preenchimento deste campo está gerando erros)
            SALA_turma = st.text_input('Turma', max_chars=1)

            # Responsável (o nome dessa coluna no Banco de Dados consta como 'resposavel'
            responsavel = st.text_input(label='Nome do(a) Responsável pelo(a) Aluno(a):', max_chars=200)

        button_new_aluno = st.form_submit_button(label='CADASTRAR ALUNO(A)')

        if button_new_aluno:
            mycursor = mydb.cursor()
            sql = """
            INSERT INTO ALUNO (ra, nome, sexo, cpf, rg, telefone, resposavel, nascimento, SALA_serie, SALA_turma) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            val = (ra, nome, sexo, cpf, rg, telefone, responsavel, nascimento, SALA_serie, SALA_turma)
            mycursor.execute(sql, val)
            mydb.commit()
            with st.spinner('Cadastro realizado+ com sucesso!'):
                time.sleep(3)
                st.success('Aluno(a) cadastrado(a): '+nome+', RA: '+ra)


# Função para parar de exibir 'telas'/formulários, limpando a tela
def nada():
    return None


# Função para cadastro de empréstimo, elaborada pelo Rodrigo
def tela_cadastro_emprestimo():
    with st.form(key='form_emprestimo'):
        st.subheader("CADASTRAR NOVO EMPRESTIMO")

        aluno = st.text_input("RA Aluno", max_chars=8)
        livro = st.text_input("Numero de Tombo do Livro", max_chars=15)
        dias = st.number_input("Dias de Emprestimo", step=1)
        data_emprestimo = datetime.today().strftime('%Y-%m-%d')
        data_devolucao = date.today() + timedelta(days=dias)

        button_new_emprestimo = st.form_submit_button(label='Adicionar o Emprestimo')
        # adicionar = st.form_submit_button('Adicionar o Emprestimo')

        if button_new_emprestimo:
            mycursor = mydb.cursor()
            # Puxar a Sala do Aluno pelo RA:
            sql = f"""
            SELECT 

                a.ra AS aluno,
                a.nome AS aluno,
                a.SALA_serie AS serie,
                a.SALA_turma AS turma
            FROM pji.aluno AS a
            WHERE a.ra = '{aluno}'
            """
            mycursor.execute(sql)
            TABELA_E = mycursor.fetchall()
            DATAFRAME = pd.DataFrame(TABELA_E)
            serie = DATAFRAME[2].unique()[0]
            turma = DATAFRAME[3].unique()[0]

            # Query de adição do emprestimo

            sql = f"""
            INSERT INTO pji.emprestimo (LIVRO_n_tombo, ALUNO_ra, ALUNO_SALA_serie, ALUNO_SALA_turma, data_inicio, data_entrega)
            VALUES ("{livro}", "{aluno}", "{serie}", "{turma}", "{data_emprestimo}", "{data_devolucao}");
            """
            mycursor.execute(sql)  # executa a Query
            mydb.commit()  # Adiciona o banco de dados
            st.spinner("Empréstimo cadastrado com sucesso!")
            time.sleep(3)
            st.success("Empréstimo cadastrado com sucesso")
    # nada()


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


def novo_emprestimo(aluno, livro, data_inicio, data_entrega):
    df_aluno = pd.DataFrame(aluno)
    df_livro = pd.DataFrame(livro)

    mylist = [str(df_livro[0].unique()[0]), str(df_aluno[0][0]), str(df_aluno[8][0]), str(df_aluno[9][0]), data_inicio,
              data_entrega]
    alterar_banco('''
                    INSERT INTO EMPRESTIMO (LIVRO_n_tombo, ALUNO_ra, ALUNO_SALA_serie, ALUNO_SALA_turma, data_inicio, data_entrega)
                    VALUES (%s, %s, %s, %s, %s, %s)
                  ''', mylist)
    st.success("Empréstimo cadastrado!")


def tela_novo_emprestimo():
    st.warning("Selecione o(a) Aluno(a) pesquisando por nome ou código EOL:")
    aluno = selecionar_registro('pji.aluno', 'nome', 'ra', 'SALA_serie', 1, 11)
    if aluno is not None:
        st.write("Aluno(a) selecionado(a):", aluno[0][1], aluno[0][0])
    st.write('__________________________________________________________')
    st.warning("Selecione o livro desejado pesquisando por autor, título ou número de tombo:")
    livro = selecionar_registro('pji.livro', 'autor', 'titulo', 'n_tombo', 1, 10)
    if livro is not None:
        st.write("Livro selecionado:", livro[0][1], ',', livro[0][2], ',', livro[0][0])
    data_inicio = st.date_input("Selecione a data do início do empréstimo:")
    data_entrega = st.date_input("Selecione a data máxima para devolução:", value=date.today() + timedelta(3))
    if data_inicio >= data_entrega:
        st.error("Atenção: a devolução está prevista para o mesmo dia do empréstimo!")
    with st.form(key='borrow', clear_on_submit=True):
        new_borrow = st.form_submit_button(label="CADASTRAR EMPRÉSTIMO")
        if new_borrow:
            if aluno is not None and livro is not None:
                novo_emprestimo(aluno, livro, data_inicio, data_entrega)
            else:
                st.error("Um erro ocorreu, tente novamente com novos parâmetros.")

def tela_finalizar_emprestimo():
    st.subheader("Finalizar empréstimo")
    st.write("Pesquise os empréstimos vigentes por nome ou ra do aluno, ou título ou tombo do livro:")
    busca = st.text_input("Filtre sua busca até obter apenas uma linha de resultado:")
    if busca is not None:
        mycursor = mydb.cursor()
        mycursor.execute(f'''
            SELECT emprestimo.LIVRO_n_tombo,livro.titulo,aluno.nome,aluno.ra,emprestimo.data_inicio,emprestimo.data_entrega
            FROM aluno
            INNER JOIN emprestimo ON aluno.ra=emprestimo.ALUNO_ra
            INNER JOIN livro ON  emprestimo.LIVRO_n_tombo=livro.n_tombo 
            WHERE (nome LIKE '%{busca}%' OR ra LIKE '%{busca}%' OR titulo LIKE '%{busca}%' OR n_tombo LIKE '%{busca}%') 
        ''')
        nova_tabela = mycursor.fetchall()
        if len(nova_tabela) > 0:
            df = pd.DataFrame(nova_tabela)
            df = df.rename(columns={
                0: 'Número do Tombo',
                1: 'Título do Livro',
                2: 'Nome do(a) Aluno(a)',
                3: 'RA do(a) Aluno(a)',
                4: 'Início do Empréstimo',
                5: 'Fim do Empréstimo'
            })
            st.dataframe(df)
            if len(nova_tabela) == 1:
                with st.form(key="finish_borrow"):
                    finish_button = st.form_submit_button("FINALIZAR EMPRÉSTIMO")
                    if finish_button:
                        mycursor = mydb.cursor()
                        mycursor.execute(f"DELETE FROM pji.EMPRESTIMO WHERE LIVRO_n_tombo = '{nova_tabela[0][0]}'")
                        mydb.commit()
                        st.success("Empréstimo finalizado!")
