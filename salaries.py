# -*- coding: utf-8 -*-
"""Salaries.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZjIOm9-sF7AFEyCepwUFKf6wbJ6MlKEt
"""

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

st.write(
        """
        # Анализ заработных плат в России
        ## Загрузка данных
        
        Загрузим данные Росстата о номинальных заработных платах в России за 2020-2023 гг. 
        Они представлены в виде двух таблиц: c 2000 по 2016 г. и с 2017 по 2023 г. Разделение связано с переходом на ОКВЭД2.
        """
    )

def load_salaries():
    df = pd.read_excel('tab3-zpl_2023.xlsx')
    excel_reader = pd.ExcelFile('tab3-zpl_2023.xlsx')
    df_1 = excel_reader.parse('с 2017 г.')
    df_2 = excel_reader.parse('2000-2016 гг.')

    df_1= df_1.rename(columns={'Unnamed: 0': 'Среднемесячная начисленная заработная плата по видам экономической деятельности', 'Unnamed: 1': '2017', 'Unnamed: 2': '2018', 'Unnamed: 3': '2019', 'Unnamed: 4': '2020', 'Unnamed: 5': '2021', 'Unnamed: 6': '2022', 'Unnamed: 7': '2023'})
    df_2= df_2.rename(columns={'Unnamed: 1': '2000', 'Unnamed: 2': '2001', 'Unnamed: 3': '2002', 'Unnamed: 4': '2003', 'Unnamed: 5': '2004', 'Unnamed: 6': '2005', 'Unnamed: 7': '2006','Unnamed: 8': '2007', 'Unnamed: 9': '2008', 'Unnamed: 10': '2009', 'Unnamed: 11': '2010', 'Unnamed: 12': '2011', 'Unnamed: 13': '2012', 'Unnamed: 14': '2013', 'Unnamed: 15': '2014', 'Unnamed: 16': '2015', 'Unnamed: 17': '2016'})
    df_1.fillna('', inplace=True)
    df_2.fillna('', inplace=True)
    return df_1, df_2
    
df_1, df_2 = load_salaries()    
st.dataframe(df_2)
st.dataframe(df_1)

st.write(
  """
  Также для анализа используем [данные об инфляции](https://xn----ctbjnaatncev9av3a8f8b.xn--p1ai/):
  """
)

def load_inflation():
    tables = pd.read_html('https://xn----ctbjnaatncev9av3a8f8b.xn--p1ai/%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D1%8B-%D0%B8%D0%BD%D1%84%D0%BB%D1%8F%D1%86%D0%B8%D0%B8')
    i = tables[1]
    return i

i = load_inflation()
st.dataframe(i)

st.write(
  """
  ## Предобработка данных
  
  Из данных Росстата о заработных платах выберем три вида экономической деятельности: 
  - производство кокса и нефтепродуктов;
  - строительство;
  - образование.
  
  Представим данные за 2000-2023 гг. в одной таблице.
  """
)
def select_salaries():
    df_1, df_2 = load_salaries()  
    df_1 = df_1.loc[[26, 43, 54]]
    df_1 = df_1.T
    df_1 = df_1.drop("Среднемесячная начисленная заработная плата по видам экономической деятельности")
    df_1[26] = df_1[26].astype(float)
    df_1[43] = df_1[43].astype(float)
    df_1[54] = df_1[54].astype(float)
    df_1 = df_1.rename(columns = {26 :"Производство кокса и нефтепродуктов", 43:"Строительство", 54:"Образование"})
    del df_2['СРЕДНЕМЕСЯЧНАЯ НОМИНАЛЬНАЯ НАЧИСЛЕННАЯ ЗАРАБОТНАЯ ПЛАТА РАБОТНИКОВ  ПО ПОЛНОМУ КРУГУ ОРГАНИЗАЦИЙ ПО ВИДАМ ЭКОНОМИЧЕСКОЙ ДЕЯТЕЛЬНОСТИ (в соответствии с ОКВЭД-2007) В РОССИЙСКОЙ ФЕДЕРАЦИИ ЗА 2000-2016гг.']
    df_2 = df_2.loc[[16, 26, 34]]
    df_2=df_2.T
    df_2[16] = df_2[16].astype(float)
    df_2[26] = df_2[26].astype(float)
    df_2[34] = df_2[34].astype(float)
    df_2 = df_2.rename(columns = {16 :"Производство кокса и нефтепродуктов", 26:"Строительство", 34:"Образование"})
    df = pd.concat([df_2, df_1])
    return df

df = select_salaries()
st.dataframe(df)

st.write(
    """
    Выберем данные  о годовой инфляции за 2000-2023 гг. 
    """
)

def select_inflation():
    i = load_inflation()
    i = i.T
    i= i.rename(columns={0: '2024', 1: '2023', 2: '2022', 3: '2021', 4: '2020', 5: '2019', 6: '2018',7: '2017', 8: '2016', 9: '2015', 10: '2014', 11: '2013', 12: '2012', 13: '2011', 14: '2010', 15: '2009', 16: '2008', 17: '2007', 18: '2006', 19: '2005', 20: '2004', 21: '2003', 22: '2002', 23: '2001', 24: '2000'})
    i = i.loc[["Всего"]]
    i = i.T
    i = i.rename(columns = {"Всего":"Процент инфляции"})
    i = i.iloc[1:25]
    i = i.iloc[::-1]
    return i
    
i = select_inflation()
st. dataframe(i)

st.write(
  """
  ## Визуализация данных
  ### Номинальные заработные платы
  Построим график номинальных заработных плат.
  """
)

def fig():
    df = select_salaries()
    fig, ax = plt.subplots()
    ax.plot(df.index, df['Производство кокса и нефтепродуктов'], label = "Номинальная зп в сфере пр-ва кокса и нефтепродуктов")
    ax.plot(df.index, df['Строительство'], label = "Номинальная зп в сфере строительства")
    ax.plot(df.index, df['Образование'], label = "Номинальная зп в сфере образования")
    ax.legend(loc='best')
    ax.set_title("Динамика номинальных зарплат в России")
    plt.xticks(rotation=90)
    return fig, ax

fig, ax = fig()
st.pyplot(fig)

st.write("Среднемесячные номинальные заработные платы растут по всем трем рассматриваемым видам экономической деятельности - производство кокса и нефтепродуктов, строительство и образование. На графике номинальных заработных плат в сфере производства кокса и нефтепродуктов есть снижение в 2018 году, что предположительно можно связать с падением цен на продукцию отрасли в этот период.")

def count_real_salaries():
    df = select_salaries()
    dfi = df.join(i)
    dfi['Реальная зп Пр-во кокса и нефтепродуктов'] = dfi['Производство кокса и нефтепродуктов'] *100 / (100 + dfi['Процент инфляции'])
    dfi['Реальная зп Строительство'] = dfi['Строительство'] *100 / (100 + dfi['Процент инфляции'])
    dfi['Реальная зп Образование'] = dfi['Образование'] *100 / (100 + dfi['Процент инфляции'])
    dfi = dfi[['Реальная зп Пр-во кокса и нефтепродуктов', 'Реальная зп Строительство', 'Реальная зп Образование']]
    return dfi

st.write(
         """
         ### Расчет и визуализация реальных заработных плат
         Рассчитаем реальные зарплаты на основе данных о номинальной зарплате и годовой инфляции
         """
         )
dfi = count_real_salaries()
st.dataframe(dfi)
st.write("Построим график реальных зарплат")

def fig1():
    df = select_salaries()
    fig1, ax1 = plt.subplots()
    ax1.plot(dfi.index, dfi['Реальная зп Пр-во кокса и нефтепродуктов'], label = "Реальная зп в сфере пр-ва кокса и нефтепродуктов")
    ax1.plot(dfi.index, dfi['Реальная зп Строительство'], label = "Реальная зп в сфере строительства")
    ax1.plot(dfi.index, dfi['Реальная зп Образование'], label = "Реальная зп в сфере образования")
    ax1.legend(loc='best')
    ax.set_title("Динамика реальных зарплат в России")
    plt.xticks(rotation=90)
    return fig1, ax1

fig1, ax1 = fig1()
st.pyplot(fig1)

st.write("""В целом графики реальных зарплат схожи с графиками номинальных зарплат, только значения реальных зарплат ниже номинальных.""")

st.write(
         """
         ### Расчет темпа прироста реальных зарплат и визуализация полученных данных в сравнении с годовой инфляцией
         Рассчитаем темп прироста реальных зарплат, сравнив значение каждого года с предыдущим.
         """
         )

def count_changes():
    dfi = count_real_salaries()
    dfi['Прирост зп Пр-во кокса и нефтепродуктов'] = (dfi['Реальная зп Пр-во кокса и нефтепродуктов']/ dfi['Реальная зп Пр-во кокса и нефтепродуктов'].shift(1) - 1) *100
    dfi['Прирост зп Строительство'] = (dfi['Реальная зп Строительство']/ dfi['Реальная зп Строительство'].shift(1) - 1) *100
    dfi['Прирост зп Образование'] = (dfi['Реальная зп Образование']/ dfi['Реальная зп Образование'].shift(1) - 1) *100
    dfi2 = dfi[['Прирост зп Пр-во кокса и нефтепродуктов', 'Прирост зп Строительство', 'Прирост зп Образование']]
    dfi2 = dfi2.join(i)
    return dfi2

dfi2 = count_changes()
st.dataframe(dfi2)

st.write("Сравним динамику реальных зарплат по трем видам экономической деятельности и инфляции")

def fig2():
    dfi2 = count_changes()
    fig2, ax2 = plt.subplots()
    ax2.plot(dfi2.index, dfi2['Прирост зп Пр-во кокса и нефтепродуктов'], label = "Прирост зп в сфере пр-ва кокса и нефтепродуктов")
    ax2.plot(dfi2.index, dfi2['Прирост зп Строительство'], label = "Прирост зп в сфере строительства")
    ax2.plot(dfi2.index, dfi2['Прирост зп Образование'], label = "Прирост зп в сфере образования")
    ax2.plot(dfi2.index, dfi2['Процент инфляции'], label = "Годовая инфляция")
    ax2.legend(loc='best')
    ax2.set_title("Прирост реальных зарплат и годовая инфляция в России")
    plt.xticks(rotation=90)
    return fig2, ax2

fig2, ax2 = fig2()
st.pyplot(fig2)

st.write(
         """Прирост реальных зп чаще всего превышает процент инфляции, за исключением кризисных периодов (2009 год в строительстве, 2010 год в образовании, 2014 год в строительстве и образовании, 2015 год по всем отраслям, с 2018 по 2022 год в производстве кокса и нефтепродуктов, 2020 год в образовании, 2021 год в строительстве). Ситуации, когда темпы роста зарплат не догоняют инфляцию, связаны с экономическими кризисами или являются реакцией на негативные обстоятельства (например, пандемию в 2020 году для образования и строительства, при этом снижение цен на нефтепродукты в 2018 году привело к снижению как реальных, так и номинальных зп в отрасли)."""
         )
