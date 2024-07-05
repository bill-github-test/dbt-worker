{{ config(materialized='table') }}

WITH customers as (
    SELECT * FROM {{ ref('stg_customer') }}
),

orders as (
    SELECT * FROM {{ ref('stg_order') }}
)

SELECT
    c.[Name],
    SUM(o.Amount) AS TotalAmount,
    COUNT(o.OrderId) AS NumberOfOrders
FROM orders AS o 
INNER JOIN customers AS c ON c.CustomerId = o.CustomerId
GROUP BY c.[Name]        
