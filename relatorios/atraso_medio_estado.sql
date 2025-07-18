-- Versão adaptada para o Streamlit:
SELECT 
    customer_state,
    ROUND(AVG(order_delivered_customer_date::date - order_estimated_delivery_date::date), 2) AS atraso_medio_dias
FROM 
    orders
WHERE 
    order_delivered_customer_date::date > order_estimated_delivery_date::date
    AND (:estado = 'Todos' OR customer_state = :estado)
GROUP BY
    customer_state
ORDER BY
    atraso_medio_dias DESC;