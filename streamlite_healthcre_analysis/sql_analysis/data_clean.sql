select * from healthcare_dataset;
SET SQL_SAFE_UPDATES = 0;

-- 1. total record --
select count(*) as total_record from healthcare_dataset;

-- 2 . show data types --
describe healthcare_dataset;

-- 3. change column name --
alter table healthcare_dataset rename column name to patient_name;
alter table healthcare_dataset rename column hospital to hospital_name;
alter table healthcare_dataset rename column doctor to doctor_name;

-- 4 . check for null values -- 
SELECT
SUM(patient_name IS NULL) patient_name,
SUM(age IS NULL) age,
SUM(gender IS NULL) gender,
SUM(blood_type IS NULL) blood_type,
SUM(medical_condition IS NULL) medical_condition,
sum(date_of_admission is null) date_of_admission , 
SUM(doctor_name IS NULL) doctor_name,
SUM(hospital_name IS NULL) hospital_name,
SUM(insurance_provider IS NULL) insurance_provider,
SUM(billing_amount IS NULL) billing_amount,
SUM(room_number IS NULL) room_numer,
SUM(admission_type IS NULL) admission_type,
SUM(discharge_date IS NULL) discharge_date,
SUM(medication IS NULL) medication,
SUM(test_results IS NULL) test_results
FROM healthcare_dataset;
-- ans : no null value found -- 

-- 5 . check blank value -- 
select * from healthcare_dataset
where trim(patient_name) = ''
or trim(medical_condition) = ''
or trim(doctor_name) = ''
or trim(hospital_name) = ''
or trim(insurance_provider) = ''
or trim(admission_type) = ''
or trim(medication) = ''
or trim(test_results) = ''
or trim(blood_type) = ''
or trim(gender) = '';
-- ans : no blank value found

-- 6 : remove white spaces --
UPDATE healthcare_dataset
SET
patient_name = TRIM(patient_name),
gender = TRIM(gender),
medical_condition = TRIM(medical_condition),
doctor_name = TRIM(doctor_name),
hospital_name = TRIM(hospital_name),
insurance_provider = TRIM(insurance_provider),
admission_type = trim(admission_type) , 
medication = trim(medication) , 
test_results = TRIM(test_results);

-- 7 . check unique values -- 
SELECT 'patient_name' AS column_name, COUNT(DISTINCT patient_name) AS unique_count,
GROUP_CONCAT(DISTINCT patient_name ORDER BY patient_name SEPARATOR ', ') AS unique_values
FROM healthcare_dataset
UNION ALL

SELECT 'gender', COUNT(DISTINCT gender),GROUP_CONCAT(DISTINCT gender ORDER BY gender SEPARATOR ', ')
FROM healthcare_dataset

UNION ALL

SELECT
    'blood_type',
    COUNT(DISTINCT blood_type),
    GROUP_CONCAT(DISTINCT blood_type ORDER BY blood_type SEPARATOR ', ')
FROM healthcare_dataset

UNION ALL

SELECT
    'medical_condition',
    COUNT(DISTINCT medical_condition),
    GROUP_CONCAT(DISTINCT medical_condition ORDER BY medical_condition SEPARATOR ', ')
FROM healthcare_dataset

UNION ALL

SELECT
    'doctor_name',
    COUNT(DISTINCT doctor_name),
    GROUP_CONCAT(DISTINCT doctor_name ORDER BY doctor_name SEPARATOR ', ')
FROM healthcare_dataset

UNION ALL

SELECT
    'hospital_name',
    COUNT(DISTINCT hospital_name),
    GROUP_CONCAT(DISTINCT hospital_name ORDER BY hospital_name SEPARATOR ', ')
FROM healthcare_dataset

UNION ALL

SELECT
    'insurance_provider',
    COUNT(DISTINCT insurance_provider),
    GROUP_CONCAT(DISTINCT insurance_provider ORDER BY insurance_provider SEPARATOR ', ')
FROM healthcare_dataset

union all 
select 'admission_type' , 
count(distinct admission_type),
group_concat(distinct admission_type order by admission_type separator ', ')
from healthcare_dataset

union all
select 'medication' , 
count(distinct medication),
group_concat(distinct medication order by medication separator ', ')
from healthcare_dataset

union all
select 'test_results',
count(distinct test_results) , 
group_concat(distinct test_results order by test_results separator ', ')
from healthcare_dataset

union all 
select 'room_number' , 
count(distinct room_number) , 
group_concat(distinct room_number order by room_number separator ', ')
from healthcare_dataset;

-- 8 . check duplicate data -- 
with a as (select patient_name,age,gender,blood_type,medical_condition,
date_of_admission,doctor_name,hospital_name,
insurance_provider,
billing_amount,room_number,admission_type,
discharge_date,medication,test_results ,  count(*) as total from healthcare_dataset
group by patient_name,age,gender,blood_type,medical_condition,
date_of_admission,doctor_name,hospital_name,
insurance_provider,
billing_amount,room_number,admission_type,
discharge_date,medication,test_results having count(*) > 1)
select count(*) as duplicate from a;
-- ans : found 534 duplicate data 

-- to remove duplicate data --
-- 1 . add column id as we don't have any promary key column
alter table healthcare_dataset add column id int primary key auto_increment first;

-- 2 . Rank duplicates and delete the extras (keep the first occurrence, remove the rest)
with ranked as (select id , row_number() over(partition by 
patient_name, age, gender, blood_type, medical_condition,
date_of_admission, doctor_name, hospital_name,
insurance_provider, billing_amount, room_number,
admission_type, discharge_date, medication, test_results
order by id) as rn from healthcare_dataset)
delete from healthcare_dataset where id in (select id from ranked where rn > 1);   

-- 3 . Verify - should return 0 now
with a as (select patient_name,age,gender,blood_type,medical_condition,
date_of_admission,doctor_name,hospital_name,
insurance_provider,
billing_amount,room_number,admission_type,
discharge_date,medication,test_results ,  count(*) as total from healthcare_dataset
group by patient_name,age,gender,blood_type,medical_condition,
date_of_admission,doctor_name,hospital_name,
insurance_provider,
billing_amount,room_number,admission_type,
discharge_date,medication,test_results having count(*) > 1)
select count(*) as duplicate from a;
-- ans : now remove duplicate data properly

-- 9 . check data shape after remove duplicate -- 
select count(*) as total_record from healthcare_dataset;

-- 10 . fix patient_name column as the name is not proper case 
update healthcare_dataset set patient_name = lower(patient_name);
select * from healthcare_dataset;

-- create new columns (feature engineering) --
-- 1 . patient_admit_days --
alter table healthcare_dataset add column no_of_day_admit int ; 
update healthcare_dataset set no_of_day_admit = datediff(discharge_date , date_of_admission);

select * from healthcare_dataset;


-- 2 . age group -- 
select min(age)  , max(age) from healthcare_dataset;

alter table healthcare_dataset add column age_group varchar(30);
update healthcare_dataset set age_group = 
case when age between 13 and 19 then 'teenagers'
when age between 20 and 29 then 'young adult' 
when age between 30 and 39 then 'adult' 
when age between 40 and 49 then 'middle age'
when age between 50 and 59 then 'older adult'
when age between  60 and 69 then 'senior adult'
when age between 70 and 79 then 'elderly'
else 'very elderly' end;

select * from healthcare_dataset;
drop table clean_dataset;
-- save clean_dataset -- 
create table clean_dataset as 
select * from healthcare_dataset;