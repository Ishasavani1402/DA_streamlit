# --------kpi--------- 
overall_layoff_kpi = '''select sum(layoffs_count) as layoff_count from clean_dataset'''

layoff_pct_kpi = '''select round(avg(layoff_percentage),2) as layoff_pct from clean_dataset'''

total_company_kpi = '''select count(distinct company_name) as total_company from clean_dataset'''

total_industry_kpi = '''select count(distinct industry) as total_industry from clean_dataset'''

# ----------sql analysis------------

yearly_layoff = '''select year , sum(layoffs_count) as total_layoff from clean_dataset group by year order by year'''

yerly_hiring_pct_for_cmpny = '''with a as (SELECT year,company_name,
COUNT(case when hiring_trend = 'Moderate Hiring' then 1 end) AS Moderate_Hiring,
COUNT(case when hiring_trend = 'Aggressive Hiring' then 1 end) AS Aggressive_Hiring 
FROM clean_dataset GROUP BY year,company_name)
select * , ROUND(Moderate_Hiring * 100.0 /nullif(SUM(Moderate_Hiring) OVER (PARTITION BY year),0),2)
AS distribution_pct_moderate , 
ROUND(Aggressive_Hiring * 100.0 /nullif(SUM(Aggressive_Hiring) OVER (PARTITION BY year),0),2)
AS distribution_pct_aggresive from a order by year ;'''

company_layoff = '''select company_name , sum(layoffs_count) as total_layoff from clean_dataset group by company_name order by total_layoff desc'''

yearly_company_layoff = '''with layoff as (select year , company_name , sum(layoffs_count) as total_layoff , 
dense_rank() over(partition by year order by sum(layoffs_count) desc) as higest_layoff
from clean_dataset group by year , company_name)
select * from layoff where higest_layoff = 1;'''

yearly_company_open_roles = '''with open_role_sum as (select company_name , top_hiring_role , sum(open_roles) as total_open_role , 
dense_rank() over(partition by company_name order by sum(open_roles) desc) as higest_open_role
from clean_dataset group by company_name , top_hiring_role)
select * from open_role_sum where higest_open_role = 1;'''

industry_layoff = '''select industry , sum(layoffs_count) as total_layoff from clean_dataset group by industry order by total_layoff desc'''

country_layoff = '''select country , sum(layoffs_count) as total_layoff from clean_dataset group by country order by total_layoff desc'''

industry_common_reason_layoff = '''with reson_count as (select industry , reason_for_layoffs , count(*) as layoff_record , 
dense_rank() over(partition by industry order by count(*) desc) as rnk
from clean_dataset group by industry , reason_for_layoffs)
select * from reson_count where rnk = 1;'''

company_size_layoff = '''select company_size , sum(layoffs_count) as total_layoff from clean_dataset group by company_size order by total_layoff desc'''

hiring_trend_analysis = '''select hiring_trend , round(avg(open_roles) , 2) as avg_open_role from clean_dataset where hiring_trend in ('Moderate Hiring', 'Aggressive Hiring')
group by hiring_trend'''

hiring_role_analysis = '''select top_hiring_role , round(sum(open_roles) , 2) as total_open_role from clean_dataset group by top_hiring_role order by total_open_role desc'''

market_condition_layoff = '''select market_condition , round(sum(layoffs_count) , 2) as total_layoff from clean_dataset group by market_condition order by total_layoff desc'''

market_condition_hiring_trend = '''select market_condition , hiring_trend , round(sum(open_roles) , 2) as total_open_role from clean_dataset where hiring_trend in ('Aggressive Hiring', 'Moderate Hiring')group by market_condition , hiring_trend order by total_open_role desc'''

ai_adoption_vs_layoff = ''' select case when ai_adoption_level < 3 then 'very low (0-2)' 
when ai_adoption_level < 5 then 'low (3-4)' 
when ai_adoption_level < 7 then 'moderate (5-6)'
when ai_adoption_level < 9 then 'high (7-8)'
else 'very high (9+)' end as ai_adoption_bucket , 
round(avg(layoffs_count),2) as avg_layoff from clean_dataset group by ai_adoption_bucket order by avg_layoff desc ;
'''