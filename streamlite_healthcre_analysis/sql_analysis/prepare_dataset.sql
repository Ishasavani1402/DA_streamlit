create database if not exists healthcare;
use healthcare;

-- table creation --
create table if not exists healthcare_dataset(
name varchar(50) , 
age int , 
gender varchar(30) , 
blood_type varchar(20) , 
medical_condition varchar (30) , 
date_of_admission date , 
doctor text , 
hospital text , 
insurance_provider varchar(20) , 
billing_amount decimal (12,2) , 
room_number int , 
admission_type varchar (30) , 
discharge_date date ,
medication text , 
test_results varchar(20)
);

-- load dataset --
set global local_infile = 1;

load data local infile
'D:/Data Analytics/healthcre_analysis_sql/dataset/healthcare_dataset.csv'
 into table healthcare_dataset
 fields terminated by ','
 enclosed by '"'
 lines terminated by '\n'
 ignore 1 rows
 (name,age,gender,blood_type,
medical_condition,
@date_of_admission,
doctor,hospital,
insurance_provider,
billing_amount,
room_number,
admission_type,
@discharge_date,
medication,test_results
)
set Date_of_Admission = STR_TO_DATE(@date_of_admission, '%d-%m-%Y'),
	Discharge_Date = STR_TO_DATE(@discharge_date, '%d-%m-%Y');

select * from healthcare_dataset;
