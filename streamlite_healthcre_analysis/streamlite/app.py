import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from csv_to_mysql import create_connection
import queries
import matplotlib.pyplot as plt
import seaborn as sns



# page configuration
st.set_page_config(page_title='healthcare analysis' , layout='wide')
st.title('💉 Healthcare analysis System')

with st.sidebar:
    st.sidebar.title("📌 Navigation")
    menu = st.radio(
        'Select Analysis',
        options=[
            'Overview',
            'medical condition',
            'insurance provider',
            'doctor analysis',
            'hospital analysis',
            'seasonal analysis',
            'pivot table'
        ],
        index=0
    )

# get connection
conn = create_connection()

if menu == 'Overview':
    st.subheader("📊 Overview")
    st.header("📌 Key Business Metrics")
     # 🔥 KPI CARDS

    col1, col2, col3, col4 = st.columns(4)

    patient = pd.read_sql(queries.total_patient, conn)
    hospital = pd.read_sql_query(queries.total_hospital , conn)
    doctor = pd.read_sql_query(queries.total_doctor , conn)
    admit_day  = pd.read_sql_query(queries.avg_admit_days , conn)

    col1.metric("Total Patient", f"{int(patient.iloc[0,0])}")
    col2.metric("Total Hospital", int(hospital.iloc[0,0]))
    col3.metric("Total doctor", int(doctor.iloc[0,0]))
    col4.metric("Avg Admit Day", int(admit_day.iloc[0,0]))

elif menu == 'medical condition':
    st.subheader("Which medical condition has the highest average billing amount?")
    df = pd.read_sql(queries.medical_condition , conn)
    st.dataframe(df)

    st.bar_chart(df , x = 'medical_condition' , y='avg_bill')
    # plt.figure(figsize=(10,5))
    # plt.bar(df['medical_condition'], df['avg_bill'], color='blue') 
    # plt.xlabel("medical_condition")
    # plt.ylabel("avg_bill")
    # plt.title("medical condition analysis")
    # st.pyplot(plt)

    # que 2
    st.markdown('-'*20)
    st.subheader('For each medical condition, which doctor treats the most patients?')
    df = pd.read_sql_query(queries.medical_condition_patient_treat , conn)
    st.dataframe(df)
    
    st.markdown("---")
    st.caption("🚀 healthcare analysis system | Built by Isha")

elif menu == 'insurance provider':
    st.subheader("Which insurance provider brings in the most total revenue?")
    df= pd.read_sql_query(queries.insurance_provider , conn)
    st.dataframe(df)

    st.bar_chart(df , x = 'insurance_provider' , y = 'total_revenue')
    # plt.figure(figsize=(10,5))
    # plt.bar(df['insurance_provider'], df['total_revenue'], color='blue') 
    # plt.xlabel("insurance_provider")
    # plt.ylabel("total_revenue")
    # plt.title("insurance provider analysis")
    # st.pyplot(plt)

    st.markdown("---")
    st.caption("🚀 healthcare analysis system | Built by Isha")

elif menu == 'doctor analysis':
    st.subheader('Top 5 doctors by total number of patients treated')
    df = pd.read_sql_query(queries.doctor , conn)
    st.dataframe(df)

    st.bar_chart(df , x = 'doctor_name' , y = 'total_patient')
    # plt.figure(figsize=(10,5))
    # plt.bar(df['doctor_name'], df['total_patient'], color='blue') 
    # plt.xlabel("doctor_name")
    # plt.ylabel("total_patient")
    # plt.title("doctor analysis")
    # st.pyplot(plt)

    st.markdown("---")
    st.caption("🚀 healthcare analysis system | Built by Isha")

elif menu == 'hospital analysis':
    st.subheader('''Which hospital's average billing is highest, and by how much does it exceed the overall average''')
    df = pd.read_sql_query(queries.hospital , conn)
    st.dataframe(df)

    st.markdown("---")
    st.caption("🚀 healthcare analysis system | Built by Isha")

elif menu == 'seasonal analysis':
    st.subheader('yearly total no of patient admit')
    df = pd.read_sql_query(queries.yearly_admit , conn)
    st.dataframe(df)

    st.line_chart(df, x='admit_year', y='total_admission')

    st.markdown("---")
    st.caption("🚀 healthcare analysis system | Built by Isha")

    


