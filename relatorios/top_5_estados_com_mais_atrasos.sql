SELECT 
    customer_state AS estado_do_cliente,
    COUNT(*) FILTER (WHERE order_delivered_customer_date > order_estimated_delivery_date) AS total_atrasos
FROM 
    orders
GROUP BY 
    customer_state
ORDER BY 
    total_atrasos DESC
LIMIT 5;