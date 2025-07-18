-- Versão adaptada para o Streamlit:
SELECT 
    ROUND(AVG(order_delivered_customer_date::date - order_purchase_timestamp::date), 2) AS tempo_medio_entrega_dias
FROM 
    orders
WHERE 
    order_delivered_customer_date IS NOT NULL
    AND order_purchase_timestamp IS NOT NULL
    AND (:estado = 'Todos' OR customer_state = :estado);