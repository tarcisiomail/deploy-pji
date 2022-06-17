import pandas as pd
import streamlit as st
import psycopg2
from datetime import timedelta, date


# Conexão do Banco de dados
mydb = psycopg2.connect(
    database="deg4do58nvsta5",
    user="nvhkstpynbzgqi",
    password="b4288fbb1fbc757e60e9aba5e362828464e2a36db1a54d2f9cb3903f2b0b6dc5",
    host="ec2-52-204-195-41.compute-1.amazonaws.com",
    port="5432")


def alterar_banco(sql, val):
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

def selecionar_registro_livro(tabela, coluna1, coluna2, coluna3, key):
    pesquisa = st.text_input(label='', key=key, help='Digite um termo para sua pesquisa:')
    if pesquisa != '':
        mycursor = mydb.cursor()
        sql = (
            f"""
            SELECT * 
            FROM public."{tabela}" 
            WHERE (unaccent({coluna1}) ILIKE unaccent('%{pesquisa}%') 
            OR unaccent({coluna2}) ILIKE unaccent('%{pesquisa}%') 
            OR unaccent({coluna3}) ILIKE unaccent('%{pesquisa}%'))
            """)
        mycursor.execute(sql)
        resultado = mycursor.fetchall()
        DATAFRAME = pd.DataFrame(resultado)

        mycursor.close()
        DATAFRAME = DATAFRAME.rename(columns={
            0: 'n_tombo',
            1: 'n_livro',
            2: 'titulo',
            3: 'autor',
            4: 'editora',
            5: 'edição',
            6: 'ano_edicao',
            7: 'genero',
            8: 'prateleira'
        })

        if len(DATAFRAME) >= 1:
            DATAFRAME['n_tombo_comp'] = DATAFRAME['n_tombo'] + '-' + DATAFRAME['n_livro']
            options = list()
            options.append("...")
            for i in range(len(DATAFRAME)):
                options.append(str(DATAFRAME.loc[i, 'n_tombo_comp']) + '-' + DATAFRAME.loc[i, 'titulo'])

            select_reg = st.selectbox("", options)

            if select_reg != "...":
                n_tombo = select_reg.split(sep='-')[0].rstrip()
                n_livro = select_reg.split(sep='-')[1].lstrip()
                titulo = select_reg.split(sep='-')[2]

                mycursor = mydb.cursor()
                mycursor.execute(
                    f"""
                    SELECT * 
                    FROM public."{tabela}" 
                    WHERE (unaccent(titulo) ILIKE unaccent('%{titulo}%') 
                        AND tombo ILIKE '%{n_tombo}%'
                        AND nlivro ILIKE '%{n_livro}%')
                    """)
                resultado = mycursor.fetchall()
                mycursor.close()
                return resultado

        else:
            st.error('Nenhum resultado encontrado!')


def selecionar_registro_condicional(tabela, coluna1, ano, turma, key):
    col1, col2 = st.columns(2)
    with col1:
        pesquisa = st.text_input(label='', key=key, help='Digite um termo para sua pesquisa:')
    with col2:
        if pesquisa == '' and ano != '...' and turma != '...':
            mycursor = mydb.cursor()
            sql = (f'''
                SELECT * FROM public."{tabela}" WHERE
                ano = '{ano}' AND
                turma = '{turma}' ORDER BY nome ASC
            ''')
            mycursor.execute(sql)
            resultado = mycursor.fetchall()
            mydb.commit()
            mycursor.close()
            options = ['...']
            for i in range(len(resultado)):
                options.append(resultado[i][1])
            select_reg = st.selectbox("", options)
            if select_reg != "...":
                return resultado

        if pesquisa != '':
            mycursor = mydb.cursor()
            if ano != '...' and turma == '...':
                sql = (f'''
                    SELECT * FROM public."{tabela}" WHERE 
                    ano = '{ano}' AND
                    unaccent({coluna1}) ILIKE unaccent('%{pesquisa}%') ORDER BY {coluna1} ASC
                    ''')
                mycursor.execute(sql)
                resultado = mycursor.fetchall()
                mydb.commit()
                mycursor.close()
                if len(resultado) == 1:
                    option = [resultado[0][1]]
                    st.selectbox('', option)
                    return resultado
                elif len(resultado) > 1:
                    options = list()
                    options.append("...")
                    for i in range(len(resultado)):
                        options.append(resultado[i][1])
                    select_reg = st.selectbox("", options)
                    mycursor = mydb.cursor()
                    mycursor.execute(f'''
                        SELECT * FROM public."{tabela}" WHERE unaccent({coluna1}) ILIKE unaccent('%{select_reg}%')
                        ''')
                    resultado = mycursor.fetchall()
                    mycursor.close()
                    if select_reg != "...":
                        return resultado
                else:
                    st.error('Nenhum resultado encontrado!')

            if ano == '...' and turma != '...':
                sql = (f'''
                    SELECT * FROM public."{tabela}" WHERE 
                    turma = '{turma}' AND
                    unaccent({coluna1}) ILIKE unaccent('%{pesquisa}%') ORDER BY {coluna1} ASC
                    ''')
                mycursor.execute(sql)
                resultado = mycursor.fetchall()
                mydb.commit()
                mycursor.close()
                if len(resultado) == 1:
                    option = [resultado[0][1]]
                    st.selectbox('', option)
                    return resultado
                elif len(resultado) > 1:
                    options = list()
                    options.append("...")
                    for i in range(len(resultado)):
                        options.append(resultado[i][1])
                    select_reg = st.selectbox("", options)
                    mycursor = mydb.cursor()
                    mycursor.execute(f'''
                        SELECT * FROM unaccent({tabela}) 
                        WHERE unaccent({coluna1})ILIKE unaccent('%{select_reg}%')
                        ''')
                    resultado = mycursor.fetchall()
                    mycursor.close()
                    if select_reg != "...":
                        return resultado
                else:
                    st.error('Nenhum resultado encontrado!')

            if ano != '...' and turma != '...':
                sql = (f'''
                    SELECT * FROM public."{tabela}" WHERE 
                    (ano = '{ano}' AND turma = '{turma}') AND
                    unaccent({coluna1}) ILIKE unaccent('%{pesquisa}%') ORDER BY {coluna1} ASC
                    ''')
                mycursor.execute(sql)
                resultado = mycursor.fetchall()
                mydb.commit()
                mycursor.close()
                if len(resultado) == 1:
                    option = [resultado[0][1]]
                    st.selectbox('', option)
                    return resultado
                elif len(resultado) > 1:
                    options = list()
                    options.append("...")
                    for i in range(len(resultado)):
                        options.append(resultado[i][1])
                    select_reg = st.selectbox("", options)
                    mycursor = mydb.cursor()
                    mycursor.execute(
                        f"SELECT * FROM {tabela} WHERE unaccent({coluna1}) ILIKE unaccent('%{select_reg}%')")
                    resultado = mycursor.fetchall()
                    mycursor.close()
                    if select_reg != "...":
                        return resultado
                else:
                    st.error('Nenhum resultado encontrado!')

            if ano == '...' and turma == '...':
                sql = (f'''
                    SELECT * FROM public."ALUNO" 
                    WHERE unaccent({coluna1}) ILIKE unaccent('%{pesquisa}%') ORDER BY {coluna1} ASC
                    ''')
                mycursor.execute(sql)
                resultado = mycursor.fetchall()
                mydb.commit()
                mycursor.close()
                if len(resultado) == 1:
                    option = [resultado[0][1]]
                    st.selectbox('', option)
                    return resultado
                elif len(resultado) > 1:
                    options = list()
                    options.append("...")
                    for i in range(len(resultado)):
                        options.append(resultado[i][1])
                    select_reg = st.selectbox("", options)
                    mycursor = mydb.cursor()
                    mycursor.execute(f'''
                        SELECT * FROM public."{tabela}" WHERE unaccent({coluna1}) ILIKE unaccent('%{select_reg}%')
                    ''')
                    resultado = mycursor.fetchall()
                    mycursor.close()
                    if select_reg != "...":
                        return resultado
                else:
                    st.error('Nenhum resultado encontrado!')


def select_column_ano(tabela, coluna, tag, key):
    # Função utilizada para criar um selectbox com registros únicos de uma determinada coluna
    mycursor = mydb.cursor()
    mycursor.execute(f'SELECT DISTINCT {coluna} FROM public."{tabela}" ORDER BY {coluna} ASC')
    series_all = mycursor.fetchall()
    mycursor.close()
    series_options = list()
    series_options.append("...")
    for i in range(len(series_all)):
        series_options.append(series_all[i][0])
    series = st.selectbox(tag, options=series_options, key=key)
    return series


def select_column_turma(tabela, coluna, ano, tag, key):
    # Função utilizada para criar um selectbox com registros únicos de uma determinada coluna
    mycursor = mydb.cursor()
    mycursor.execute(f'''
        SELECT DISTINCT {coluna} FROM public."{tabela}" WHERE ano = '{ano}' ORDER BY {coluna} ASC
        ''')
    series_all = mycursor.fetchall()
    mycursor.close()
    series_options = list()
    series_options.append("...")
    for i in range(len(series_all)):
        series_options.append(series_all[i][0])
    series = st.selectbox(tag, options=series_options, key=key)
    return series


def novo_emprestimo(aluno, livro, data_inicio, data_entrega):
    df_aluno = pd.DataFrame(aluno)
    df_livro = pd.DataFrame(livro)

    mylist = [str(df_livro[0].unique()[0]), str(df_livro[1].unique()[0]), str(df_aluno[1].unique()[0]),
              str(df_aluno[0].unique()[0]), str(df_aluno[2].unique()[0]), str(df_aluno[3].unique()[0]), data_inicio,
              data_entrega]
    try:
        alterar_banco(f'''
                        INSERT INTO public."EMPRESTIMO" 
                        (livrotombo, livronlivro, alunonome, alunora, alunoano, alunoturma, datainicio, dataentrega)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                      ''', mylist)
        st.success("Empréstimo cadastrado!")

    except:
        st.warning("O livro selecionado não está disponível.")
        mydb.rollback()

def tela_novo_emprestimo():
    st.subheader("CADASTRAR NOVO EMPRÉSTIMO")
    col1, col2 = st.columns(2)
    with col1:
        ano = select_column_ano('ALUNO', 'ano', 'Selecione o Ano', 113)
    with col2:
        turma = select_column_turma('ALUNO', 'turma', ano, 'Selecione a Turma', 114)

    st.warning("Selecione o(a) Aluno(a) pesquisando pelo nome:")

    aluno = selecionar_registro_condicional('ALUNO', 'nome', ano, turma, 11)
    st.write('__________________________________________________________')
    st.warning("Selecione o livro desejado pesquisando por autor, título ou número de tombo:")
    livro = selecionar_registro_livro('LIVRO', 'autor', 'titulo', 'tombo', 10)
    data_inicio = st.date_input("Selecione a data do início do empréstimo:")
    data_entrega = date.today() + timedelta(7)
    with st.form(key='borrow', clear_on_submit=True):
        new_borrow = st.form_submit_button(label="CADASTRAR EMPRÉSTIMO")
        if new_borrow:
            if aluno is not None and livro is not None:
                novo_emprestimo(aluno, livro, data_inicio, data_entrega)
            else:
                st.error("Um erro ocorreu, tente novamente com novos parâmetros.")
