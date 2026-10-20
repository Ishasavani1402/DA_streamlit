select * from sales;
SET SQL_SAFE_UPDATES = 0;

-- 1 . total record--
select count(*) as total_record from sales;

-- 2 . check invoice id (duplicate or not) --
select invoice_id , count(*) as total from sales group by invoice_id
having count(*) > 1; 

-- 3. check null value --
SELECT
SUM(invoice_id IS NULL) invoice_id,
SUM(branch IS NULL) branch,
SUM(city IS NULL) city,
SUM(customer_type IS NULL) customer_type,
SUM(gender IS NULL) gender,
sum(product_name is null) product_name , 
SUM(product_line IS NULL) product_line,
SUM(unit_price IS NULL) unit_price,
SUM(quantity IS NULL) quantity,
SUM(vat IS NULL) vat,
SUM(total IS NULL) total,
SUM(date IS NULL) sale_date,
SUM(time IS NULL) sale_time,
SUM(payment IS NULL) payment,
SUM(cogs IS NULL) cogs,
SUM(gross_margin_pct IS NULL) gross_margin_pct,
SUM(gross_income IS NULL) gross_income,
SUM(rating IS NULL) rating , 
sum(product_category is null) product_category
FROM sales;
-- ans : no null value found

-- 4. Check Blank Values --
SELECT *
FROM sales
WHERE TRIM(city)=''
OR TRIM(branch)=''
OR TRIM(customer_type)=''
OR TRIM(product_line)=''
or trim(product_name)=''
or trim(product_category)=''
OR TRIM(payment)='';
-- ans : no blank found

-- 5 . remove extra spaces
UPDATE sales
SET
city = TRIM(city),
branch = TRIM(branch),
customer_type = TRIM(customer_type),
gender = TRIM(gender),
product_line = TRIM(product_line),
product_name = trim(product_name) , 
product_category = trim(product_category) , 
payment = TRIM(payment);

-- 6 . verify data types
describe sales;

-- 7 . velidate if 0 or negetive value occure --
select * from sales where quantity <= 0 or
total <= 0 or unit_price <= 0 or gross_margin_pct <= 0 
or rating <= 0;

-- 8 . check unique values
SELECT 'branch' AS column_name, COUNT(DISTINCT branch) AS unique_count,
GROUP_CONCAT(DISTINCT branch ORDER BY branch SEPARATOR ', ') AS unique_values
FROM sales
UNION ALL

SELECT 'city', COUNT(DISTINCT city),GROUP_CONCAT(DISTINCT city ORDER BY city SEPARATOR ', ')
FROM sales

UNION ALL

SELECT
    'customer_type',
    COUNT(DISTINCT customer_type),
    GROUP_CONCAT(DISTINCT customer_type ORDER BY customer_type SEPARATOR ', ')
FROM sales

UNION ALL

SELECT
    'gender',
    COUNT(DISTINCT gender),
    GROUP_CONCAT(DISTINCT gender ORDER BY gender SEPARATOR ', ')
FROM sales

UNION ALL

SELECT
    'product_line',
    COUNT(DISTINCT product_line),
    GROUP_CONCAT(DISTINCT product_line ORDER BY product_line SEPARATOR ', ')
FROM sales

UNION ALL

SELECT
    'payment',
    COUNT(DISTINCT payment),
    GROUP_CONCAT(DISTINCT payment ORDER BY payment SEPARATOR ', ')
FROM sales

UNION ALL

SELECT
    'product_category',
    COUNT(DISTINCT product_category),
    GROUP_CONCAT(DISTINCT product_category ORDER BY product_category SEPARATOR ', ')
FROM sales

union all 
select 'product_name' , 
count(distinct product_name),
group_concat(distinct product_name order by product_name separator ', ')
from sales;


-- 9 . create column time_of_day --
SELECT time,
CASE 
	WHEN `time` BETWEEN "00:00:00" AND "12:00:00" THEN "Morning"
	WHEN `time` BETWEEN "12:01:00" AND "16:00:00" THEN "Afternoon"
	ELSE "Evening" 
END AS time_of_day
FROM sales;

alter table sales add column time_of_day varchar(20);
select * from sales;
update sales set time_of_day = (CASE 
	WHEN `time` BETWEEN "00:00:00" AND "12:00:00" THEN "Morning"
	WHEN `time` BETWEEN "12:01:00" AND "16:00:00" THEN "Afternoon"
	ELSE "Evening" end
    );
    
-- 10 create column day_name
alter table sales add column day_name varchar(40);
update sales set day_name = dayname(date);

-- 11 create column month
alter table sales add column month_no int;
update sales set month_no = month(date);

-- 12 . check total column consistency
SELECT * FROM sales WHERE ABS(total - (unit_price*quantity + vat)) > 0.5
OR ABS(gross_income - vat) > 0.5;
-- only 1 row found out of 1000

-- 13. rating consistency
select * from sales where rating > 10;
-- no recrod found

select count(*) as total from sales; -- check after all clean process done

-- new clean dataset
create table clean_sales as 
select * from sales;