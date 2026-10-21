# -------------kpi -------------
total_sale = '''select round(sum(total),2) as total_sales from clean_sales;'''

total_qty = '''select round(sum(quantity),2) as total_qty from clean_sales;'''

avg_rate = '''select round(avg(rating),2) as avg_rate from clean_sales;'''

total_order = '''select count(*) as total_order from clean_sales;'''

total_profit = '''select round(sum(total - cogs),2) as total_profit,
round(100.0 * sum(total-cogs) / sum(total),2) as profit_margin_pct
from clean_sales;'''

# ----------- sql analysis ------------

category_sale = '''select product_category , round(sum(total),2) as total_sale ,
round(100.0 * sum(total) / sum(sum(total)) over() ,2) as pct_of_total_sale , 
count(*) as total_record
from clean_sales group by product_category order by total_sale desc;'''

product_line_sale = '''select product_line , round(sum(total),2) as total_sale ,
round(100.0 * sum(total) / sum(sum(total)) over() ,2) as pct_of_total_sale , 
count(*) as total_record
from clean_sales group by product_line order by total_sale desc;'''