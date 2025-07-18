SELECT 
    customer_state AS estado,
    ROUND(AVG(order_delivered_customer_date::date - order_estimated_delivery_date::date), 2) AS atraso_medio_dias
FROM 
    orders
WHERE 
    order_delivered_customer_date IS NOT NULL
    AND order_estimated_delivery_date IS NOT NULL
    AND order_delivered_customer_date::date > order_estimated_delivery_date::date  -- só pedidos atrasados
GROUP BY 
    customer_state
ORDER BY 
    atraso_medio_dias DESC;