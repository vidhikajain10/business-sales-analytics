-- Assumes the CSV is loaded into a table named sales_data.

SELECT SUM(Revenue) AS total_revenue
FROM sales_data;

SELECT Region, SUM(Revenue) AS revenue
FROM sales_data
GROUP BY Region
ORDER BY revenue DESC;

SELECT Product, SUM(Revenue) AS revenue, SUM(Profit) AS profit
FROM sales_data
GROUP BY Product
ORDER BY revenue DESC;

SELECT DATE_TRUNC('month', "Order Date") AS month, SUM(Revenue) AS revenue
FROM sales_data
GROUP BY DATE_TRUNC('month', "Order Date")
ORDER BY month;

SELECT Product, SUM(Revenue) AS revenue
FROM sales_data
GROUP BY Product
ORDER BY revenue DESC
LIMIT 10;
