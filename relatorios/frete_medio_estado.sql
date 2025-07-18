-- Versão adaptada para o Streamlit:
SELECT 
    o.customer_state,
    ROUND(CAST(AVG(oi.freight_value) AS numeric), 2) AS frete_medio
FROM 
    order_items oi
JOIN
    orders o ON oi.order_id = o.order_id
WHERE
    (:estado = 'Todos' OR o.customer_state = :estado)
GROUP BY
    o.customer_state
ORDER BY
    frete_medio DESC;