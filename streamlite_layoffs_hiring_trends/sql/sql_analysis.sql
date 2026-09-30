create database tech_layoffs_hiring_trends;
use tech_layoffs_hiring_trends;
select * from clean_dataset;

-- 1 . total record --
select count(distinct record_id) as total_record from clean_dataset;

-- 2 . ai_automation_impact and job security and employee sentiment
select case when ai_automation_impact <4 then 'low impact'  
when ai_automation_impact < 7.4 then 'moderate impact'
when ai_automation_impact < 10.8 then 'high impact'
else 'very high impact' end as ai_automation_bucket , 
round(avg(job_security_score),2) as avg_job_security_score , 
round(avg(employee_sentiment) ,2) as avg_employee_sentiment , 
count(*) as total_record from clean_dataset 
group by ai_automation_bucket order by avg_job_security_score desc , avg_employee_sentiment desc ;

-- 3 . in each year which company have higest layoff??
with layoff as (select year , company_name , sum(layoffs_count) as total_layoff , 
dense_rank() over(partition by year order by sum(layoffs_count) desc) as higest_layoff
from clean_dataset group by year , company_name)
select * from layoff where higest_layoff = 1;

-- 4 . in each industry which is common reason for layoff ??
with reson_count as (select industry , reason_for_layoffs , count(*) as layoff_record , 
dense_rank() over(partition by industry order by count(*) desc) as rnk
from clean_dataset group by industry , reason_for_layoffs)
select * from reson_count where rnk = 1;

-- 5 . Which country had the highest total layoffs each year (2024, 2025, 2026)?
with a as (select year , country , sum(layoffs_count) as total_layoff ,
 dense_rank() over(partition by year order by sum(layoffs_count) desc) as rnk
from clean_dataset group by country , year)
select  year,country  , total_layoff from a where rnk = 1;

-- 6 . in each company which hiring role have higest open role??
with open_role_sum as (select company_name , top_hiring_role , sum(open_roles) as total_open_role , 
dense_rank() over(partition by company_name order by sum(open_roles) desc) as higest_open_role
from clean_dataset group by company_name , top_hiring_role)
select * from open_role_sum where higest_open_role = 1;

-- 7 . For each year, what percentage of a company's Moderate and Aggressive Hiring activity belongs to that company?
with a as (SELECT year,company_name,
COUNT(case when hiring_trend = 'Moderate Hiring' then 1 end) AS Moderate_Hiring,
COUNT(case when hiring_trend = 'Aggressive Hiring' then 1 end) AS Aggressive_Hiring 
FROM clean_dataset GROUP BY year,company_name)
select * , ROUND(Moderate_Hiring * 100.0 /nullif(SUM(Moderate_Hiring) OVER (PARTITION BY year),0),2)
AS distribution_pct_moderate , 
ROUND(Aggressive_Hiring * 100.0 /nullif(SUM(Aggressive_Hiring) OVER (PARTITION BY year),0),2)
AS distribution_pct_aggresive from a order by year ;

-- 8 . AI adoption vs layoffs
select case when ai_adoption_level < 3 then 'very low (0-2)' 
when ai_adoption_level < 5 then 'low (3-4)' 
when ai_adoption_level < 7 then 'moderate (5-6)'
when ai_adoption_level < 9 then 'high (7-8)'
else 'very high (9+)' end as ai_adoption_bucket , 
round(avg(layoffs_count),2) as avg_layoff from clean_dataset group by ai_adoption_bucket order by avg_layoff desc ;