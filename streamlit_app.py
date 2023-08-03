import streamlit as st
import pandas as pd
import numpy as np
import class_exer
from io import StringIO


st.title('Упраженения по английскому языку')

excercise = class_exer.EngExer()

uploaded_file = st.file_uploader('Загрузите текст')

if uploaded_file:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    excercise.load_text(string_data)

st.header('Введите количество заданий по каждой теме')

verb = st.number_input("Задания на выбор праввильной формы глагола",min_value=0,max_value=15,value =1)
word = st.number_input("Задания на построение предложений из отдельных слов",min_value=0,max_value=15,value=1)
mlt_sent = st.number_input("Задания на перестановку предложений в правильном порядке",min_value=0,max_value=5,value=1)
art = st.number_input("Задания на вписание правильного артикля",min_value=0,max_value=10,value=1)
con = st.number_input("Задания на вписание правильного соединения",min_value=0,max_value=10,value= 1)

@st.cache_data 
def gen_text(verb,word,mlt_sent,art,con):
    return excercise.set_params(verb,word,mlt_sent,art,con)

try:
    df = gen_text(verb,word,mlt_sent,art,con)
    
    position = 0
    if verb!=0:
        st.header('Выбете праввильную форму глагола')
        for i in range(verb):
            result = []
            st.text(' '.join(df.iloc[[i]]['raw'].values[0]))
            for j,h in enumerate(df.iloc[[i]]['options'].values[0]):
                result.append(st.selectbox('nolabel', ['–––'] + h, 
                                             label_visibility="hidden",key = i*10+j))
                if result[j] == '–––':
                    pass
                elif result[j] == df.iloc[[i]]['answer'].values[0][j]:
                    st.success('', icon="✔️")
                else:
                    st.error('', icon="❌")        
                
    position += verb         
    if word!=0:
        st.header('Постройте предложение')
        for i in range(position,position+word):
            
            options = st.multiselect('Варианты',list(df.iloc[[i]]['options'].values[0]),default = None,label_visibility="hidden")
        #st.write(len(options))
        #st.write(len(df.iloc[[i]]['answer'].values[0]))
            st.write(options)
            if len(options) == len(df.iloc[[i]]['answer'].values[0]):
                if options ==  df.iloc[[i]]['raw'].values[0]:
                    st.success('',icon='✔️')
                else:
                    st.error('',icon='❌')
            else:
                pass        

    position+= word
    if mlt_sent!=0:
        st.header('Выставьте предложения в правильном порядке')
        for i in range(position,position+mlt_sent):
            options = st.multiselect('Варианты',list(df.iloc[[i]]['options'].values[0]),default = None,label_visibility="hidden")
        #st.write(len(' '.join(options)))
        #st.write(len(df.iloc[[i]]['answer'].values[0]))
            st.write(options)
            if len(options) == len(df.iloc[[i]]['answer'].values[0]):
                if options ==  df.iloc[[i]]['raw'].values[0]:
                    st.success('',icon='✔️')
                else:
                    st.error('',icon='❌')
                else:
                    pass

    position+= mlt_sent
    if art!=0:
        st.header('Впишите правильный артикль')
        for i in range(position,position+art):
            result = []
            st.text(' '.join(df.iloc[[i]]['raw'].values[0]))
            for j,h in enumerate(df.iloc[[i]]['answer'].values[0]):
                result.append(st.text_input('nolabel',label_visibility="hidden",key = i*10+j))
                if result[j] == None:
                    pass
                elif result[j].lower() == df.iloc[[i]]['answer'].values[0][j].lower():
                    st.success('', icon="✔️")
                else:
                    st.error('', icon="❌") 

    position+= art
    if con!=0:
        st.header('Впишите правильное соединение')
        for i in range(position,position+con):
            result = []
            st.text(' '.join(df.iloc[[i]]['raw'].values[0]))
            for j,h in enumerate(df.iloc[[i]]['answer'].values[0]):
                result.append(st.text_input('nolabel',label_visibility="hidden",key = i*10+j))
                if result[j] == None:
                    pass
                elif result[j].lower() == df.iloc[[i]]['answer'].values[0][j].lower():
                    st.success('', icon="✔️")
                else:
                    st.error('', icon="❌")
