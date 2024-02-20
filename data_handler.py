import pymysql
import calendar
import pandas as pd
from db_queries import *
from datetime import datetime

def consulta():
    connection = pymysql.connect(
        host='localhost',
        user='teste',
        password='teste',
        database='testehelpdesk'
    )
    # Executa a consulta SQL e armazena o resultado em um dataframe do Pandas
    df = pd.read_sql(query_1, connection)
    connection.close()

    # df = pd.read_csv('dataset.csv')

    # Trata dataframe
    df = df.drop_duplicates(subset=['CHAMADO'])
    df['ABERTURA'] = (pd.to_datetime(df['ABERTURA'])).dt.date
    df['DataSolucao'] = (pd.to_datetime(df['DataSolucao'])).dt.date
    df['DataFechamento'] = (pd.to_datetime(df['DataFechamento'])).dt.date

    # Cria dataframe "df_s" que irá ser filtrado pela Data de Solução, enquanto o "df" pela Data de Abertura
    df_a = df.copy()
    df_s = df.copy()
    df_f = df.copy()

    df_s = df_s.dropna(subset=['DataSolucao'])
    df_s['MesAnoSolucao'] = df_s['DataSolucao'].apply(
        lambda x: x.replace(day=calendar.monthrange(x.year, x.month)[1]))

    df_a = df_a.dropna(subset=['ABERTURA'])
    df_a['MesAnoAbertura'] = df_a['ABERTURA'].apply(
        lambda x: x.replace(day=calendar.monthrange(x.year, x.month)[1]))

    ultima_atualizacao = datetime.now().strftime("%d/%m/%Y %H:%M")

    return df, df_a, df_f, df_s, ultima_atualizacao
