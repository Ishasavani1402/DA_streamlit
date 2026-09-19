import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

# page configuration
st.set_page_config(page_title='student result analysis' , layout='wide')
st.title('🎓 Student Result Analysis System')

with st.sidebar:
    st.header('📂upload dataset')
    upload_file = st.file_uploader('upload csv file' , type=["csv"])

    st.markdown('-'*20)
    selected = option_menu(
        menu_title = 'Menubar',
        options = ['raw data',
                   'student result' , 
                   'topper' , 
                   'search result' , 
                   'subject analysis' , 
                   'pass/fail',
                   'pivot table'] ,
        icons = ['table' , 
                 'bar-chart' , 'trophy' , 'search','book' , 'check-circle' , 'grid'] , 
        menu_icon = 'menu_button_wide' , 
        default_index = 0
    )
if upload_file is None:
    st.warning('please upload csv file.....')
    st.stop()

df = pd.read_csv(upload_file)
if selected == 'raw data':
    st.subheader('raw data')
    st.dataframe(df)
elif selected == 'student result':
    total_marks = df.groupby('Name')['Marks'].sum()
    avg_marks = df.groupby('Name')['Marks'].mean()

    result = pd.DataFrame({
        'total marks' : total_marks , 
        'avg marks' : avg_marks
    }).reset_index()
    st.dataframe(result)

elif selected == 'topper':
    topper = df.groupby('Name')['Marks'].sum().sort_values(ascending=False)
    n = st.number_input('How many topper do you want ??' , min_value=1 , max_value=len(topper))

    st.subheader(f'top {n} topper')
    st.dataframe(topper.head(n))

elif selected == 'search result':
    st.header('search your result..')
    search_name = st.text_input('enter student name')
    if search_name:
        filter_df = df[df['Name'].str.lower()== search_name.lower()]
        if not filter_df.empty:
            st.success(f'showing result for : {search_name}')
            st.dataframe(filter_df)

            total_marks = filter_df['Marks'].sum()
            avg_marks = filter_df['Marks'].mean()

            st.write(f'total marks {total_marks} , average marks {avg_marks}')
        else:
            st.error('student not found')

elif selected == 'subject analysis':
    subject_avg = df.groupby('Subject')['Marks'].mean()
    subject_total = df.groupby('Subject')['Marks'].sum()
    result = pd.DataFrame({
            'avg marks' : subject_avg,
            'total_marks' : subject_total
        }).reset_index()
    st.header('subject wise Avg. marks')
    st.dataframe(result)

elif selected == 'pass/fail' :
    pass_marks = st.slider('select passing marks' , 0,100,40)

    df['result'] = df['Marks'].apply(
        lambda x :'pass' if x >= pass_marks else 'fail'
    )
    st.subheader('result')
    st.dataframe(df)

elif selected == 'pivot table':
    pivot = df.pivot_table(
        values='Marks',
        index="Name" , 
        columns='Subject'
    )
    st.subheader('students each subject marks')
    st.dataframe(pivot)