-- Versão adaptada para o Streamlit:
SELECT 
    ROUND(100.0 * SUM(CASE WHEN order_delivered_customer_date::date <= order_estimated_delivery_date::date THEN 1 ELSE 0 END) / COUNT(*), 2) AS entregas_no_prazo_pct
FROM 
    orders
WHERE 
    order_delivered_customer_date IS NOT NULL
    AND order_estimated_delivery_date IS NOT NULL
    AND (:estado = 'Todos' OR customer_state = :estado);