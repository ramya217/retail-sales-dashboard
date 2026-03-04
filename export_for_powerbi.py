import sqlite3
import pandas as pd

conn = sqlite3.connect("superstore.db")

# 1. Region Summary
region = pd.read_sql_query("""
SELECT Region,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit)/SUM(Sales)*100, 2) AS Profit_Margin_Pct
FROM sales
GROUP BY Region
ORDER BY Total_Sales DESC
""", conn)

# 2. Category & Sub-Category
category = pd.read_sql_query("""
SELECT Category, [Sub-Category],
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales
GROUP BY Category, [Sub-Category]
ORDER BY Category, Total_Profit DESC
""", conn)

# 3. Yearly Trend (cleaned)
yearly = pd.read_sql_query("""
SELECT 
    substr([Order Date], -4, 4) AS Year,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales
WHERE substr([Order Date], -4, 4) IN ('2014','2015','2016','2017')
GROUP BY Year
ORDER BY Year
""", conn)

# 4. Top 10 Products
top_products = pd.read_sql_query("""
SELECT [Product Name], Category,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales
GROUP BY [Product Name], Category
ORDER BY Total_Profit DESC
LIMIT 10
""", conn)

# 5. Segment Performance
segment = pd.read_sql_query("""
SELECT Segment,
    COUNT(DISTINCT [Customer ID]) AS Total_Customers,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Sales)/COUNT(DISTINCT [Customer ID]), 2) AS Avg_Sales_Per_Customer
FROM sales
GROUP BY Segment
ORDER BY Total_Sales DESC
""", conn)

# 6. Full cleaned dataset
full = pd.read_sql_query("SELECT * FROM sales", conn)

# Export all to one Excel file with multiple sheets
with pd.ExcelWriter("superstore_analysis.xlsx", engine="openpyxl") as writer:
    full.to_excel(writer, sheet_name="Raw Data", index=False)
    region.to_excel(writer, sheet_name="Region Summary", index=False)
    category.to_excel(writer, sheet_name="Category Summary", index=False)
    yearly.to_excel(writer, sheet_name="Yearly Trend", index=False)
    top_products.to_excel(writer, sheet_name="Top Products", index=False)
    segment.to_excel(writer, sheet_name="Segment Summary", index=False)

conn.close()
print("✅ Excel file created: superstore_analysis.xlsx")
print("📊 Ready to open in Power BI!")