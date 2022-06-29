import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import psycopg2

# Conexão do Banco de dados
mydb = psycopg2.connect(
    database="deg4do58nvsta5",
    user="nvhkstpynbzgqi",
    password="b4288fbb1fbc757e60e9aba5e362828464e2a36db1a54d2f9cb3903f2b0b6dc5",
    host="ec2-52-204-195-41.compute-1.amazonaws.com",
    port="5432")

def consultar_banco(sql):
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    x = mycursor.fetchall()
    return x


def alterar_banco(sql, val):
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()


def num_tombo():
    mycursor = mydb.cursor()
    sql = '''
    SELECT tombo FROM public."LIVRO"
    '''
    mycursor.execute(sql)
    TABELA_T = mycursor.fetchall()

    if len(TABELA_T) > 0:
        DATAFRAME = pd.DataFrame(TABELA_T)

        lista_tombos = DATAFRAME[0].to_list()

        num_tombo = np.random.randint(low=10000, high=99999, dtype=int)

        while num_tombo in lista_tombos:
            num_tombo = np.random.randint(low=10000, high=99999, dtype=int)

        return num_tombo
    else:
        num_tombo = np.random.randint(low=10000, high=99999, dtype=int)
        return num_tombo


def livro_existe(titulo, autor):
    mycursor = mydb.cursor()
    sql = f'''SELECT unaccent(titulo), unaccent(autor) FROM public."LIVRO" 
        WHERE unaccent(titulo) ILIKE unaccent('%{titulo}%') 
        AND unaccent(autor) ILIKE unaccent('%{autor}%')
    '''
    mycursor.execute(sql)
    TABELA_T = mycursor.fetchall()

    if len(TABELA_T) > 0:

        return True

    else:
        return False


def add_num_livro(titulo, autor):
    # achar o num_tombo do livro repetido
    mycursor = mydb.cursor()
    sql = f"""
    SELECT * 
    FROM public."LIVRO"
    WHERE (titulo = '{titulo}' AND autor = '{autor}')
    """
    mycursor.execute(sql)
    TABELA_T = mycursor.fetchall()

    if len(TABELA_T) > 0:
        DATAFRAME = pd.DataFrame(TABELA_T)
        DATAFRAME = DATAFRAME.rename(columns={
            0: 'Número do Tombo',
            1: 'Número do Livro',
            2: 'Título',
            3: 'Autor',
            4: 'Editora',
            5: 'Edição',
            6: 'Genero',
            7: 'Prateleira'
        })
        DATAFRAME['Número do Livro'] = DATAFRAME['Número do Livro'].apply(lambda x: int(x))
        num_tombo = DATAFRAME['Número do Tombo'].unique()[0]
        int_num_livro = DATAFRAME['Número do Livro'].max() + 1
        if int_num_livro < 10:
            num_livro = '00' + str(int_num_livro)
        if int_num_livro >= 10 and int_num_livro < 100:
            num_livro = '0' + str(int_num_livro)
        if int_num_livro > 100:
            num_livro = str(int_num_livro)
        titulo = DATAFRAME['Título'].unique()[0]
        autor = DATAFRAME['Autor'].unique()[0]
        editora = DATAFRAME['Editora'].unique()[0]
        edicao = DATAFRAME['Edição'].unique()[0]
        genero = DATAFRAME['Genero'].unique()[0]


        return num_tombo, num_livro, titulo, autor, editora, edicao, genero

def confirma_livro():
    with st.form('confirma_livro'):
        xy = st.form_submit_button("Teste")
        if xy:
            st.success("yes")

# Função para exibir o formulário de cadastro de livros
def tela_cadastro_livro():
    st.warning("Antes de cadastrar um novo livro, verifique os livros existentes pesquisando pelo título ou autor.")
    selecionar_livro = selecionar_registro_titulo('LIVRO', 'titulo', 'autor', 'tombo', 2, 277)

    if selecionar_livro is None:
        st.subheader("CADASTRAR NOVO VOLUME")
        with st.form(key='form_livro',clear_on_submit=True):

            # Título
            titulo = st.text_input(label='Título', max_chars=200)
            col1, col2 = st.columns(2)
            with col1:
                # Autor
                autor = st.text_input(label='Nome do(a) Autor(a)', max_chars=100)
                # Editora
                editora = st.text_input(label='Editora', max_chars=100)
            with col2:
                # Edição
                edicao = st.text_input(label='Edição', max_chars=50)
                # Gênero
                genero = st.text_input(label='Gênero', max_chars=30)
            # Prateleira
            prateleira = st.text_input(label='Prateleira', max_chars=30)

            button_new_livro = st.form_submit_button(label='CADASTRAR 📘')

            if button_new_livro:

                ######### Verificar a existencia do livro
                tem_livro = livro_existe(titulo, autor)

                # Verifica se ja tem o livro
                if tem_livro:
                    st.warning('Livro ***'+str(titulo)+'*** de ***'+str(autor)+'*** já existe. '
                               'Tem certeza que deseja prosseguir? Um novo tombo será criado. '
                               'Sugerimos que a caixa de pesquisa acima seja utilizada.')
                    st.session_state['confirma'] = 1

                else:
                    # Se não tem, cria um novo numero de tombo
                    tombo = num_tombo()
                    n_livro = '001'
                    mycursor = mydb.cursor()
                    sql = f"""
                    INSERT INTO public."LIVRO" (tombo, nlivro, titulo, autor, editora, edicao, genero, prateleira) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    val = (tombo, n_livro, titulo, autor, editora, edicao, genero, prateleira)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    st.success("Novo volume cadastrado com sucesso! Número do Tombo: "+str(tombo)+'-'+str(n_livro))
                    dialogo_sucesso = '''
                        <script language="javascript">
                        alert("Novo volume cadastrado com sucesso!");
                        </script>
                    '''
                    components.html(dialogo_sucesso, height=0)

        try:
            if st.session_state.confirma == 1:

                with st.form('confirma_livro_existente'):
                    confirma_livro_existente = st.form_submit_button("Confirmar cadastro de livro existente")
                    if confirma_livro_existente:
                        tombo = num_tombo()
                        n_livro = '001'
                        mycursor = mydb.cursor()
                        sql = f"""
                                INSERT INTO public."LIVRO" (tombo,nlivro, titulo, autor, editora, 
                                edicao, genero) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """
                        val = (tombo, n_livro, titulo, autor, editora, edicao, genero)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        dialogo_sucesso = '''
                            <script language="javascript">
                            alert("Novo volume cadastrado com sucesso!");
                            </script>
                        '''
                        components.html(dialogo_sucesso)
                        st.success(
                            "Novo volume cadastrado com sucesso! Número do Tombo: " + str(tombo) + '-' + str(n_livro))

                        st.session_state.confirma = 0
        except:
            mydb.rollback()

    if selecionar_livro is not None:
        st.write('Última prateleira: '+str(selecionar_livro[len(selecionar_livro)-1][7]))
        with st.form(key='repetir livro'):
            col1, col2 = st.columns(2)
            with col1:
                st.write('')
                st.write('')
                repetir_livro = st.form_submit_button('Adicionar novo volume')
            with col2:
                prateleira = st.text_input(label=('Atualizar a prateleira, se necessário.'))
            if not repetir_livro:
                dframe = pd.DataFrame(selecionar_livro)
                dframe = dframe.rename(columns={
                    0: 'Nº do Tombo',
                    1: 'Nº do Livro',
                    2: 'Título',
                    3: 'Autor',
                    4: 'Editora',
                    5: 'Edição',
                    6: 'Gênero',
                    7: 'Prateleira'
                })
                st.dataframe(dframe)
            if repetir_livro:
                tombo = selecionar_livro[0][0]
                titulo = selecionar_livro[0][2]
                autor = selecionar_livro[0][3]
                editora = selecionar_livro[0][4]
                edicao = selecionar_livro[0][5]
                genero = selecionar_livro[0][6]

                tombo, n_livro, titulo, autor, editora, edicao, genero = \
                    add_num_livro(selecionar_livro[0][2], selecionar_livro[0][3])
                if prateleira == '':
                    prateleira_atual = selecionar_livro[len(selecionar_livro)-1][7]
                else:
                    prateleira_atual = prateleira
                mycursor = mydb.cursor()
                sql = f"""
                       INSERT INTO public."LIVRO" (tombo,nlivro, titulo, autor, editora, edicao, genero, prateleira) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                       """
                val = (tombo, str(n_livro), titulo, autor, editora, edicao, genero, prateleira_atual)
                mycursor.execute(sql, val)
                mydb.commit()
                update_query = consultar_banco(f'''
                    SELECT * FROM public."LIVRO" WHERE 
                    (titulo = '{titulo}' and autor = '{autor}')''')
                dframe = pd.DataFrame(update_query)
                dframe = dframe.rename(columns={
                    0: 'Nº do Tombo',
                    1: 'Nº do Livro',
                    2: 'Título',
                    3: 'Autor',
                    4: 'Editora',
                    5: 'Edição',
                    6: 'Gênero',
                    7: 'Prateleira'
                })
                st.dataframe(dframe)
                st.success('Novo volume cadastrado com sucesso!')
                dialogo_sucesso = '''
                    <script language="javascript">
                    alert("Novo volume cadastrado com sucesso!");
                    </script>
                '''
                components.html(dialogo_sucesso)

def selecionar_registro_titulo(tabela, coluna1, coluna2, coluna3, coluna_exibida, key):
    pesquisa = st.text_input(label='', key=key, help='Digite um termo para sua pesquisa:')

    if pesquisa != '':
        mycursor = mydb.cursor()
        sql = (f'''
            SELECT * FROM public."{tabela}" WHERE 
            (unaccent({coluna1}) ILIKE unaccent('%{pesquisa}%') 
            OR unaccent({coluna2}) ILIKE unaccent('%{pesquisa}%') 
            OR unaccent({coluna2}) ILIKE unaccent('%{pesquisa}%')
            OR unaccent({coluna3}) ILIKE unaccent('%{pesquisa}%'))
            ''')
        mycursor.execute(sql)
        resultado = mycursor.fetchall()
        mydb.commit()

        if len(resultado) >= 1:

            options = list()
            options.append("...")
            options.append(resultado[0][coluna_exibida] + ' - ' + resultado[0][3])
            for i in range(len(resultado)):
                if i > 0 and (resultado[i - 1][0] != resultado[i][0]):
                    options.append(resultado[i][coluna_exibida] + ' - ' + resultado[i][3])

            select_reg = st.selectbox("", options)
            select_reg_titulo = select_reg.split(sep='-')[0].rstrip()

            mycursor = mydb.cursor()
            mycursor.execute(f'''
                SELECT * FROM public."{tabela}" WHERE unaccent({coluna1}) ILIKE unaccent('%{select_reg_titulo}%')
                ''')
            resultado = mycursor.fetchall()

            if select_reg != "...":
                return resultado

        elif len(resultado) == 0:
            st.error('Nenhum resultado encontrado!')


