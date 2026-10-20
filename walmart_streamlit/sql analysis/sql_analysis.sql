select * from clean_sales;

-- A . KPI --
-- 1 . total sales --
select round(sum(total),2) as total_sales from clean_sales;

-- 2 . total quanity available in wallmrt --
select round(sum(quantity),2) as total_qty from clean_sales;

-- 3 . overall avg rate --
select round(avg(rating),2) as avg_rate from clean_sales;

-- 4 . total orders -- 
select count(*) as total_order from clean_sales;

-- 5 . total profit --
select round(sum(total - cogs),2) as total_profit,
round(100.0 * sum(total-cogs) / sum(total),2) as profit_margin_pct
from clean_sales;

-- B . sql analysis --
-- 1 . category wise total sale --
select product_category , round(sum(total),2) as total_sale ,
round(100.0 * sum(total) / sum(sum(total)) over() ,2) as pct_of_total_sale , 
count(*) as total_record
from clean_sales group by product_category order by total_sale desc;

-- 2 . product_line wise total sale --
select product_line , round(sum(total),2) as total_sale ,
round(100.0 * sum(total) / sum(sum(total)) over() ,2) as pct_of_total_sale , 
count(*) as total_record
from clean_sales group by product_line order by total_sale desc;

-- 3 . total sale by products --
select product_name , round(sum(total),2) as total_sale ,
round(100.0 * sum(total) / sum(sum(total)) over() ,2) as pct_of_total_sale
from clean_sales group by product_name order by total_sale desc;

-- 4 . city wise sale --
select city , round(sum(total),2) as total_sale ,
round(100.0 * sum(total) / sum(sum(total)) over() ,2) as pct_of_total_sale
from clean_sales group by city order by total_sale desc;

-- 5 . gender wise customer type  distribuution --
select customer_type , count(case when gender = 'Male' then 1 end) as male,
count(case when gender = 'Female' then 1 end) as female from clean_sales
group by customer_type;

-- 6 . product wise total qty sale --
select product_name , round(sum(quantity),2) as total_qty , 
count(*) as total_record
from clean_sales  group by product_name order by total_qty desc;

-- 7 . payment mode wise sale distribution --
select payment , count(*) as total_transactions , 
round(sum(total),2) as total_sale
from clean_sales
group by payment order by total_sale desc;

-- 8 . montly sale distribution -- 
select month_no , round(sum(total),2) as total_sale
from clean_sales group by month_no order by month_no;

-- 9 . time_of_day wise total sale -- 
select time_of_day , round(sum(total),2) as total_sale 
from clean_sales group by time_of_day order by total_sale desc;

-- 10 . top 10 higest rated products
select product_name , round(avg(rating),2) as avg_rate ,
count(*) as total_record
from clean_sales group by product_name
having count(*) >=20 
order by avg_rate desc limit 10;

-- 11 . higest sales product each and every product line --
with overall_sale as (select product_line , product_name , round(sum(total),2) as total_sale
from clean_sales group by  product_line , product_name) , 
sale_rank as (select * , dense_rank() over(partition by product_line order by total_sale desc) as higest_sale_rnk
from overall_sale)
select * from sale_rank where higest_sale_rnk = 1;

-- 12 . from which branch generate highest sale from each and every city
with overall_sale as (select city , branch , round(sum(total),2) as total_sale
from clean_sales group by  city , branch) , 
sale_rank as (select * , dense_rank() over(partition by city order by total_sale desc) as higest_sale_rnk
from overall_sale)
select * from sale_rank where higest_sale_rnk = 1;

-- 13 .product line wise incurred the highest GST
select product_line , sum(vat) as total_vat , 
count(*) as total_record
from clean_sales 
group by product_line order by total_vat desc;

-- 14 . month over month sale comparision and growth pct -- 
with sale as (select month_no , round(sum(total),2) as total_sale 
from clean_sales group by month_no),
previous_sale as (select * , lag(total_sale) over(order by month_no) as previous_month_sale
from sale)
select * , round((total_sale - previous_month_sale) / nullif(previous_month_sale , 0) * 100 , 2) as growth_pct
from previous_sale;

-- 15 . day-wise sales trend
select day_name, round(sum(total),2) as total_sale, count(*) as total_record
from clean_sales
group by day_name
order by field(day_name,'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday');

-- 16 . avg basket size by customer_type
select customer_type, round(avg(total),2) as avg_basket_size, count(*) as total_record
from clean_sales group by customer_type order by avg_basket_size desc;