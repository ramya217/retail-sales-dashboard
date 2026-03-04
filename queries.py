import sqlite3
import pandas as pd

conn = sqlite3.connect("superstore.db")

# Query 1 - Sales & Profit by Region
q1 = """
SELECT 
    Region,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit)/SUM(Sales)*100, 2) AS Profit_Margin_Pct
FROM sales
GROUP BY Region
ORDER BY Total_Sales DESC;
"""

# Query 2 - Sales by Category and Sub-Category
q2 = """
SELECT 
    Category,
    [Sub-Category],
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales
GROUP BY Category, [Sub-Category]
ORDER BY Category, Total_Profit DESC;
"""

# Query 3 - Monthly Sales Trend
q3 = """
SELECT 
    strftime('%Y', substr([Order Date], -4, 4) || '-' || 
    CASE substr([Order Date], instr([Order Date],'/')+1, 
         instr(substr([Order Date], instr([Order Date],'/')+1), '/')-1)
    WHEN '1' THEN '01' WHEN '2' THEN '02' WHEN '3' THEN '03'
    WHEN '4' THEN '04' WHEN '5' THEN '05' WHEN '6' THEN '06'
    WHEN '7' THEN '07' WHEN '8' THEN '08' WHEN '9' THEN '09'
    ELSE substr([Order Date], instr([Order Date],'/')+1,
         instr(substr([Order Date], instr([Order Date],'/')+1),'/')-1)
    END || '-01') AS Year,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales
GROUP BY Year
ORDER BY Year;
"""

# Query 4 - Top 10 Most Profitable Products
q4 = """
SELECT 
    [Product Name],
    Category,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales
GROUP BY [Product Name], Category
ORDER BY Total_Profit DESC
LIMIT 10;
"""

# Query 5 - Customer Segment Performance
q5 = """
SELECT 
    Segment,
    COUNT(DISTINCT [Customer ID]) AS Total_Customers,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Sales)/COUNT(DISTINCT [Customer ID]), 2) AS Avg_Sales_Per_Customer
FROM sales
GROUP BY Segment
ORDER BY Total_Sales DESC;
"""

print("=== 1. Sales & Profit by Region ===")
print(pd.read_sql_query(q1, conn))

print("\n=== 2. Sales by Category & Sub-Category ===")
print(pd.read_sql_query(q2, conn))

print("\n=== 3. Yearly Sales Trend ===")
print(pd.read_sql_query(q3, conn))

print("\n=== 4. Top 10 Most Profitable Products ===")
print(pd.read_sql_query(q4, conn))

print("\n=== 5. Customer Segment Performance ===")
print(pd.read_sql_query(q5, conn))

conn.close()
print("\n✅ All queries complete!")