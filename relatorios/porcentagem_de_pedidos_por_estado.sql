SELECT 
    customer_state AS estado,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentual_pedidos -- Conta os pedidos por estado.
	-- Soma total de pedidos (usando janela para manter o agrupamento).
FROM 
    orders
GROUP BY 
    customer_state
ORDER BY 
    percentual_pedidos DESC;