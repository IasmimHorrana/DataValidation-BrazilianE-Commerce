SELECT 
    customer_state,
    ROUND(CAST(AVG(freight_value) AS numeric), 2) AS frete_medio
FROM 
    order_items
GROUP BY 
    customer_state
ORDER BY 
    frete_medio DESC
LIMIT 10;