SELECT 
    ROUND(
        COUNT(*) FILTER (WHERE order_delivered_customer_date <= order_estimated_delivery_date) * 100.0 
		/ COUNT(*),2) AS percentual_entregas_no_prazo
FROM 
    orders;