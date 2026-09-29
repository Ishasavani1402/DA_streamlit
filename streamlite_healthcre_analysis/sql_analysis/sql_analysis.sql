select * from clean_dataset;

-- A . KPI -- 
-- 1. total patients -- 
select count(distinct patient_name) as total_patient from clean_dataset;

-- 2 . total doctores -- 
select count(distinct doctor_name) as total_doctor from clean_dataset;

-- 3 .total hospital -- 
select count(distinct hospital_name) as total_hospital from clean_dataset;

-- 4 . avg_admit_days --
select round(avg(no_of_day_admit),2) as avg_admit_day from clean_dataset;


-- B. sql analysis -- 
-- 1 . Which medical condition has the highest average billing amount?
select medical_condition , round(avg(billing_amount),2) as avg_bill from clean_dataset
group by medical_condition order by avg_bill desc;

-- 2 . Which insurance provider brings in the most total revenue?
select insurance_provider , round(sum(billing_amount),2) as total_revenue from clean_dataset
group by insurance_provider order by total_revenue desc;

-- 3 . What's the average length of stay (no_of_day_admit) by admission_type?
select admission_type , round(avg(no_of_day_admit),2) as avg_admit_day
from clean_dataset group by admission_type order by avg_admit_day desc;

-- 4 . Which age_group has the highest share of "Abnormal" test results?
select age_group , count(case when test_results = 'Abnormal' then 1 end) as abanormal_count , 
count(*) as total , 
round(count(case when test_results = 'Abnormal' then 1 end) * 100.0 /
count(*) , 2) as pct_of_total
from clean_dataset group by age_group order by pct_of_total desc;

-- 5 . Top 5 doctors by total number of patients treated?
select doctor_name , count(distinct patient_name) as total_patient from clean_dataset
group by doctor_name order by total_patient desc limit 5;

-- 6 . Which hospital's average billing is highest, and by how much does it exceed the overall average?
with higest_bill as (select hospital_name  , round(avg(billing_amount),2) as avg_bill from clean_dataset
group by hospital_name order by avg_bill desc limit 1) , 
overall_avg as ( select  round(avg(billing_amount),2) as overall_avg_bill from clean_dataset)
select h.hospital_name , h.avg_bill as higest_avg_bill , 
o.overall_avg_bill , round(h.avg_bill - o.overall_avg_bill) as exceed_by from higest_bill h
cross join overall_avg o ;

-- 7 . For each medical_condition, which doctor treats the most patients?
with doctor_rnk as (select medical_condition , doctor_name , 
count(distinct patient_name) as total_patient , 
row_number() over(partition by medical_condition order by count(distinct patient_name) desc) as higest_treat 
from clean_dataset
group by medical_condition , doctor_name)
select * from doctor_rnk where higest_treat = 1;

-- 8 . Which month/year had the highest number of admissions — any seasonal pattern?
select year(date_of_admission) as admit_year ,
 month(date_of_admission) as admit_month , count(distinct patient_name) as total_admission 
from clean_dataset group by  year(date_of_admission) ,
month(date_of_admission) 
order by  total_admission desc;

-- 9 . Which blood type shows the highest occurrence of each medical condition — any risk pattern worth flagging?
with ranked as (select medical_condition , blood_type , count(*) as total_record , 
dense_rank() over(partition by medical_condition order by count(*) desc) as rnk
from clean_dataset group by medical_condition , blood_type)
select * from ranked where rnk = 1 order by medical_condition , blood_type;

-- 10 . Which patients are billed above the 90th percentile — who are the high-cost outliers?
with ranked as (select patient_name , PERCENT_RANK() over(order by billing_amount) as pct_rank
from clean_dataset)
select * from ranked where pct_rank > 0.9;

-- 11 . . What's the year-over-year growth in total billing revenue?
with yearly_revenue as (select year(date_of_admission) as admission_year , 
round(sum(billing_amount),2) as total_bill_revenue , 
lag(round(sum(billing_amount),2)) over(order by year(date_of_admission)) as previous_year_bill_revenue
from clean_dataset group by year(date_of_admission))
select * , round((total_bill_revenue - previous_year_bill_revenue) / nullif(previous_year_bill_revenue , 0) * 100.0 , 2)
as revenue_growth from  yearly_revenue;

-- 12 . Running (cumulative) total of billing amount over time, month by month.
with monthly_revenue as (
select month(date_of_admission) as admit_month , round(sum(billing_amount),2) as total_bill_revenue
from clean_dataset group by  month(date_of_admission))
select admit_month  , total_bill_revenue , 
round(sum(total_bill_revenue) over(order by admit_month) ,2) as cumulative_revenue
from monthly_revenue;

-- 13 . Within each hospital, rank doctors by total billing generated — who's the top revenue doctor per hospital?
with overall_bill as (select hospital_name , doctor_name , round(sum(billing_amount),2) as total_bill
from clean_dataset group by 1 , 2),
rnk as (select * , dense_rank() over(partition by hospital_name order by total_bill desc) as top_bill_rnk
from overall_bill)
select * from rnk where top_bill_rnk = 1;

-- 14 . Which patients appear more than once in the dataset (by name) — repeat-admission pattern?
select patient_name , count(*) as total_count , 
count(distinct gender) as gender
from clean_dataset group by patient_name 
having count(patient_name) > 1 order by total_count desc;

-- 15. Which admission_type + medical_condition combination has the longest average stay, and what's its cost impact?
select admission_type , medical_condition , round(avg(no_of_day_admit),2) as avg_stay , 
round(sum(billing_amount),2) as total_bill , 
round(avg(billing_amount),2) as avg_bill ,
 count(*) as total_case
from clean_dataset group by 1 , 2 order by avg_stay desc;

-- 16 . Is there a correlation between insurance_provider and % of "Abnormal" test results (conditional aggregation)?
select insurance_provider , count(*) as total_record ,
count(case when test_results = 'Abnormal' then 1 end) as abanormal_count , 
round(count(case when test_results = 'Abnormal' then 1 end) * 100.0 /
count(*) , 2) as pct_of_total from clean_dataset
group by 1;

-- 17 . Top 3 most expensive medical conditions within each age_group
with all_group as (select age_group , medical_condition , round(sum(billing_amount),2) as total_bill , 
dense_rank() over(partition by age_group order by round(sum(billing_amount),2) desc) as most_expensive_rnk
from clean_dataset group by 1 ,2)
select * from all_group where most_expensive_rnk <=3 order by age_group;

-- 18 . Cost-per-day of stay — which hospitals are outliers on cost efficiency?
with hospital_metrix as (select hospital_name , 
round(avg(billing_amount / nullif(no_of_day_admit , 0)),2) as cost_per_day_admit
from clean_dataset group by hospital_name),
tield as (select * , ntile(10) over(order by cost_per_day_admit) as cost_tile from hospital_metrix)
select * from tield where cost_tile in (1 , 10)
order by cost_per_day_admit desc;

-- 19 . Which quarter of the year sees the highest volume of "Emergency" admissions?
select quarter(date_of_admission) as qtr , 
count(case when admission_type = 'Emergency' then 1 end) as Emergency_admit
from clean_dataset group by quarter(date_of_admission)
order by Emergency_admit desc; 

-- 20 . Insurance provider comparison: normal vs abnormal vs inconclusive test result rates, 
-- side by side (pivot-style with CASE + AVG).
select insurance_provider , 
round(avg(case when trim(replace(test_results , char(13) , '')) = 'Normal' then 1 else 0 end)* 100,2)
as normal_result ,
round(avg(case when trim(replace(test_results , char(13) , '')) = 'Abnormal' then 1 else 0 end) * 100,2)
as abnormal_result , 
round(avg(case when trim(replace(test_results , char(13) , '')) = 'Inconclusiv' then 1 else 0 end) * 100,2 )
as inconclusive_result 
from clean_dataset group by insurance_provider;  

