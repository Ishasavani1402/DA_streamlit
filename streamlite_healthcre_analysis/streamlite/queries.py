total_patient = '''
select count(distinct patient_name) as total_patient from clean_dataset;'''

total_doctor = '''select count(distinct doctor_name) as total_doctor from clean_dataset;'''

total_hospital = '''select count(distinct hospital_name) as total_hospital from clean_dataset;'''

avg_admit_days = '''select round(avg(no_of_day_admit),2) as avg_admit_day from clean_dataset;'''

total_revenue = """
SELECT ROUND(SUM(billing_amount), 0) AS total_revenue
FROM clean_dataset;
"""

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

blood_type = '''with ranked as (select medical_condition , blood_type , count(*) as total_record , 
dense_rank() over(partition by medical_condition order by count(*) desc) as rnk
from clean_dataset group by medical_condition , blood_type)
select * from ranked where rnk = 1 order by medical_condition , blood_type;'''

hospital_rank = '''with overall_bill as (select hospital_name , doctor_name , round(sum(billing_amount),2) as total_bill
from clean_dataset group by 1 , 2),
rnk as (select * , dense_rank() over(partition by hospital_name order by total_bill desc) as top_bill_rnk
from overall_bill)
select * from rnk where top_bill_rnk = 1;'''

expensive_medical_condition = '''with all_group as (select age_group , medical_condition , round(sum(billing_amount),2) as total_bill , 
dense_rank() over(partition by age_group order by round(sum(billing_amount),2) desc) as most_expensive_rnk
from clean_dataset group by 1 ,2)
select * from all_group where most_expensive_rnk <=3 order by age_group;
'''

insurance_provider_test_result = '''select insurance_provider , 
round(avg(case when trim(replace(test_results , char(13) , '')) = 'Normal' then 1 else 0 end)* 100,2)
as normal_result ,
round(avg(case when trim(replace(test_results , char(13) , '')) = 'Abnormal' then 1 else 0 end) * 100,2)
as abnormal_result , 
round(avg(case when trim(replace(test_results , char(13) , '')) = 'Inconclusiv' then 1 else 0 end) * 100,2 )
as inconclusive_result 
from clean_dataset group by insurance_provider;  '''

admission_type_split = """
SELECT admission_type, COUNT(*) AS total_patient
FROM clean_dataset
GROUP BY admission_type;
"""

test_result_split = """
SELECT test_results, COUNT(*) AS total_patient
FROM clean_dataset
GROUP BY test_results;
"""