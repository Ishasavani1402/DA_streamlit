create database if not exists walmart;
use walmart;

-- table creation----
create table  sales(
invoice_id varchar(50) not null primary key , 
branch varchar(30) not null , 
city varchar(30) not null , 
customer_type varchar (50) not null , 
gender varchar(20) not null , 
product_name varchar (50) not null , 
product_line varchar (50) not null , 
unit_price decimal (10,2) not null , 
quantity int not null , 
vat decimal (6,4) not null , 
total decimal (12,4) not null , 
date datetime not null , 
time time not null , 
payment varchar (50) not null , 
cogs decimal (10 ,2) not null ,
gross_margin_pct decimal (12,4) , 
gross_income decimal (12 , 4) , 
rating decimal (2,1) ,
 product_category varchar (50));
 
 --- load data---
 
 show global variables like 'local_infile'; -- we can load data from local machine 
 set global local_infile = 1;
 
 load data local infile
 'D:/Data Analytics/walmart_sql/dataset/Walmart_Sales.csv'
 into table sales
 fields terminated by ','
 enclosed by '"'
 lines terminated by '\n'
 ignore 1 rows
 (invoice_id, branch, city, customer_type, gender, product_name, product_line,
 unit_price, quantity, vat, total, @date_var, time, payment, cogs,
 gross_margin_pct, gross_income, rating, product_category)
SET date = STR_TO_DATE(@date_var, '%d-%m-%Y %H:%i');

select * from sales;
drop table healthcare_dataset;
 
