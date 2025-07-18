SELECT 
        AVG(
            CAST(order_delivered_customer_date AS timestamp) - 
            CAST(order_purchase_timestamp AS timestamp)
        )
    , 2 AS tempo_medio_entrega
FROM 
    orders
WHERE 
    order_delivered_customer_date IS NOT NULL
    AND order_purchase_timestamp IS NOT NULL;

*/