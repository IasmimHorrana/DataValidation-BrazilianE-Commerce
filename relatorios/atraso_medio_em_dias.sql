SELECT 
    ROUND(AVG(order_delivered_customer_date::date - order_estimated_delivery_date::date), 2) AS atraso_medio_dias
FROM 
    orders
WHERE 
    order_delivered_customer_date::date > order_estimated_delivery_date::date;