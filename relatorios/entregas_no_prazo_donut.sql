-- Versão adaptada para o Streamlit:
SELECT
    CASE 
        WHEN order_delivered_customer_date <= order_estimated_delivery_date THEN 'No Prazo'
        ELSE 'Fora do Prazo'
    END AS status_entrega,
    COUNT(*) AS total
FROM
    orders
WHERE
    (:estado = 'Todos' OR customer_state = :estado)
GROUP BY
    status_entrega;