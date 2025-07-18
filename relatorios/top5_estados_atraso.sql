-- Versão adaptada para o Streamlit:
SELECT 
    customer_state AS estado,
    ROUND(AVG(EXTRACT(DAY FROM order_delivered_customer_date - order_estimated_delivery_date)), 2) AS atraso_medio_dias
FROM 
    orders
WHERE 
    order_delivered_customer_date > order_estimated_delivery_date
    AND (:estado = 'Todos' OR customer_state = :estado)
GROUP BY 
    customer_state
ORDER BY 
    atraso_medio_dias DESC
LIMIT 5;
