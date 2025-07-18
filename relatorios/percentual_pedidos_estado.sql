-- Versão adaptada para o Streamlit:
SELECT
    customer_state AS estado,
    COUNT(*) AS total_pedidos
FROM
    orders
WHERE
    (:estado = 'Todos' OR customer_state = :estado)
GROUP BY
    customer_state
ORDER BY
    total_pedidos DESC;