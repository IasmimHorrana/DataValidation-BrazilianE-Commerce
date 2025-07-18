-- Versão adaptada para o Streamlit:
SELECT 
    customer_state AS estado,
    ROUND(
        100.0 * SUM(
            CASE 
                WHEN order_delivered_customer_date > order_estimated_delivery_date THEN 1 
                ELSE 0 
            END
        ) / COUNT(*), 
    2) AS percentual_atrasos
FROM 
    order_items
WHERE 
    order_status = 'delivered' 
    AND data_ok = TRUE
GROUP BY 
    customer_state
ORDER BY 
    percentual_atrasos DESC;