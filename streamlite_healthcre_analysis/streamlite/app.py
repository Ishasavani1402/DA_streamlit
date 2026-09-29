import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from csv_to_mysql import create_connection
import queries
import matplotlib.pyplot as plt
from pathlib import Path 


# page configuration
st.set_page_config(page_title='healthcare analysis' , layout='wide')

# ---------- helper functions ----------
def load_css(file_name):
    css_path = Path(__file__).parent / file_name
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def kpi_card(column, label, value):
    column.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)


load_css("style.css")

# # head part
st.markdown("""
<h2 style="margin-bottom:0;">💉 Healthcare Analysis System</h2>
<p style="color:gray; margin-top:0; margin-bottom:10px;">
</p>
""", unsafe_allow_html=True)


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
        ],
        index=0
    )

# get connection
conn = create_connection()

if menu == 'Overview':
    st.header("📌 Key Business Metrics")
     # 🔥 KPI CARDS

    # col1, col2, col3, col4 = st.columns(4)

    patient = pd.read_sql(queries.total_patient, conn)
    hospital = pd.read_sql_query(queries.total_hospital , conn)
    doctor = pd.read_sql_query(queries.total_doctor , conn)
    total_revenue  = pd.read_sql_query(queries.total_revenue , conn)

    k1,k2,k3 , k4 = st.columns(4)
    kpi_card(k1, "Total Patients", f"{int(patient.iloc[0,0]):,}")
    kpi_card(k2, "Total Hospitals", f"{int(hospital.iloc[0,0]):,}")
    kpi_card(k3, "Total Doctors", f"{int(doctor.iloc[0,0]):,}")
    kpi_card(k4, "Total Revenue", f"${int(total_revenue.iloc[0,0]):,}")

# ---------- Row 2: charts ----------
    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("🚑 Admission Type wise total patient ")
        adm = pd.read_sql_query(queries.admission_type_split, conn)
        # st.dataframe(adm)
        st.bar_chart(adm, x='admission_type', y='total_patient')

    with c2:
        st.subheader("🧪 Test Results wise total patient")
        tr = pd.read_sql_query(queries.test_result_split, conn)
        # st.dataframe(tr)
        st.bar_chart(tr, x='test_results', y='total_patient')

 # ---------- Smart Insights ----------
    st.markdown("---")
    st.subheader("🧠 Key Insights")

    top_adm = adm.sort_values('total_patient', ascending=False).iloc[0]
    adm_pct = round(top_adm['total_patient'] / adm['total_patient'].sum() * 100, 1)
    st.info(f"🚑 Most patients come through **{top_adm['admission_type']}** admission ({adm_pct}%).")

    abn = tr[tr['test_results'].str.lower() == 'abnormal']['total_patient'].sum()
    abn_pct = round(abn / tr['total_patient'].sum() * 100, 1)
    st.warning(f"🧪 {abn_pct}% of patients had abnormal test results.")

    cond = pd.read_sql(queries.medical_condition, conn)
    top_cond = cond.sort_values('avg_bill', ascending=False).iloc[0]
    st.error(f"💰 Costliest condition on average: **{top_cond['medical_condition']}** (₹/$ {int(top_cond['avg_bill'])} per patient).")

    st.markdown("---")
    st.caption("🚀 healthcare analysis system | Built by Isha")



elif menu == 'medical condition':
    st.subheader("Which medical condition has the highest average billing amount?")
    df = pd.read_sql(queries.medical_condition , conn)
    st.dataframe(df)

    st.bar_chart(df , x = 'medical_condition' , y='avg_bill')

    # que 2
    st.markdown('-'*20)
    st.subheader('For each medical condition, which doctor treats the most patients?')
    df = pd.read_sql_query(queries.medical_condition_patient_treat , conn)
    st.dataframe(df)

    # Prepare data for chart
    chart_data = df.pivot(
    index='medical_condition',
    columns='doctor_name',
    values='total_patient'
).fillna(0)
    st.bar_chart(chart_data , use_container_width=True)

    # qu 3
    st.markdown('-'*20)
    st.subheader('Which blood type shows the highest occurrence of each medical condition — any risk pattern worth flagging?')
    df = pd.read_sql_query(queries.blood_type , conn)
    st.dataframe(df , use_container_width=True)

    # Prepare data for chart
    chart_data = df.pivot(
    index='medical_condition',
    columns='blood_type',
    values='total_record'
).fillna(0)

    st.bar_chart(chart_data , use_container_width=True)

    # que 4
    st.markdown('-'*20)
    st.subheader('Top 3 most expensive medical conditions within each age_group')
    df = pd.read_sql_query(queries.expensive_medical_condition , conn)
    st.dataframe(df)

    # Prepare data for chart
    chart_data = df.pivot(
    index='age_group',
    columns='medical_condition',
    values='total_bill'
    ).fillna(0)

    st.bar_chart(chart_data , use_container_width=True)

    st.markdown("---")
    st.caption("🚀 healthcare analysis system | Built by Isha")

elif menu == 'insurance provider':
    st.subheader("Which insurance provider brings in the most total revenue?")
    df= pd.read_sql_query(queries.insurance_provider , conn)
    st.dataframe(df)

    st.bar_chart(df , x = 'insurance_provider' , y = 'total_revenue')

    # que 2
    st.markdown('-'*20)
    st.subheader(''' Insurance provider comparison: normal vs abnormal vs inconclusive test result rates''')
    df = pd.read_sql_query(queries.insurance_provider_test_result , conn)
    st.dataframe(df , use_container_width=True)

    st.markdown("---")
    st.caption("🚀 healthcare analysis system | Built by Isha")

elif menu == 'doctor analysis':
    st.subheader('Top 5 doctors by total number of patients treated')
    df = pd.read_sql_query(queries.doctor , conn)
    st.dataframe(df)

    st.bar_chart(df , x = 'doctor_name' , y = 'total_patient')

    st.markdown("---")
    st.caption("🚀 healthcare analysis system | Built by Isha")

elif menu == 'hospital analysis':
    st.subheader('''Which hospital's average billing is highest, and by how much does it exceed the overall average''')
    df = pd.read_sql_query(queries.hospital , conn)
    st.dataframe(df)

    # que 2 
    st.markdown('-'*20)
    st.subheader('''Within each hospital, rank doctors by total billing generated — who's the top revenue doctor per hospital''')
    df = pd.read_sql_query(queries.hospital_rank , conn)
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
   
    


