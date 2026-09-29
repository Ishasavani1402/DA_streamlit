total_patient = '''
select count(distinct patient_name) as total_patient from clean_dataset;'''

total_doctor = '''select count(distinct doctor_name) as total_doctor from clean_dataset;'''

total_hospital = '''select count(distinct hospital_name) as total_hospital from clean_dataset;'''

avg_admit_days = '''select round(avg(no_of_day_admit),2) as avg_admit_day from clean_dataset;'''

medical_condition = '''select medical_condition , round(avg(billing_amount),2) as avg_bill from clean_dataset
group by medical_condition order by avg_bill desc'''

insurance_provider = '''select insurance_provider , round(sum(billing_amount),2) as total_revenue from clean_dataset
group by insurance_provider order by total_revenue desc;'''

avg_stay_days = '''select admission_type , round(avg(no_of_day_admit),2) as avg_admit_day
from clean_dataset group by admission_type order by avg_admit_day desc;'''

#pending
age_group = '''select age_group , count(case when test_results = 'Abnormal' then 1 end) as abanormal_count , 
count(*) as total , 
round(count(case when test_results = 'Abnormal' then 1 end) * 100.0 /
count(*) , 2) as pct_of_total
from clean_dataset group by age_group order by pct_of_total desc;'''

doctor = '''select doctor_name , count(distinct patient_name) as total_patient from clean_dataset
group by doctor_name order by total_patient desc limit 5;'''

hospital = '''with higest_bill as (select hospital_name  , round(avg(billing_amount),2) as avg_bill from clean_dataset
group by hospital_name order by avg_bill desc limit 1) , 
overall_avg as ( select  round(avg(billing_amount),2) as overall_avg_bill from clean_dataset)
select h.hospital_name , h.avg_bill as higest_avg_bill , 
o.overall_avg_bill , round(h.avg_bill - o.overall_avg_bill) as exceed_by from higest_bill h
cross join overall_avg o ;
'''

medical_condition_patient_treat = '''with doctor_rnk as (select medical_condition , doctor_name , 
count(distinct patient_name) as total_patient , 
row_number() over(partition by medical_condition order by count(distinct patient_name) desc) as higest_treat 
from clean_dataset
group by medical_condition , doctor_name)
select * from doctor_rnk where higest_treat = 1;'''

yearly_admit = '''select year(date_of_admission) as admit_year , count(distinct patient_name) as total_admission 
from clean_dataset group by  year(date_of_admission)
order by  admit_year;'''