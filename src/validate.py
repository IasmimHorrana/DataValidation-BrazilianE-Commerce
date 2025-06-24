from datetime import datetime
from typing import Literal, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    confloat,
    conint,
    constr,
    field_validator,
)


class Customer(BaseModel):
    customer_id: constr(min_length=32, max_length=32) = Field(
        ..., description="ID único do cliente, deve bater com orders"
    )
    customer_unique_id: constr(min_length=32, max_length=32) = Field(
        ..., description="ID anonimizado, pode se repetir"
    )
    customer_zip_code_prefix: conint(ge=1000, le=99999) = Field(
        ..., description="Prefixo do CEP entre 1000 e 99999"
    )
    customer_city: constr(min_length=3, max_length=32) = Field(
        ..., description="Cidade do cliente, campo não-nulo"
    )
    customer_state: constr(min_length=2, max_length=2) = Field(
        ..., description="Sigla do estado (UF) com 2 letras"
    )

    model_config = ConfigDict(validate_default=True, validate_assignment=True)


class Order(BaseModel):
    order_id: constr(min_length=32, max_length=32) = Field(
        ..., description="ID único do pedido (não nulo)"
    )
    customer_id: constr(min_length=32, max_length=32) = Field(
        ..., description="ID do cliente (deve existir no customers_dataset)"
    )
    order_status: Literal[
        "delivered",
        "invoiced",
        "shipped",
        "processing",
        "unavailable",
        "approved",
        "canceled",
        "created",
    ] = Field(..., description="Status do pedido")
    order_purchase_timestamp: datetime = Field(
        ..., description="Data e hora da compra (não nulo)"
    )
    order_approved_at: Optional[datetime] = Field(
        None, description="Data da aprovação (pode ser nulo)"
    )
    order_delivered_carrier_date: Optional[datetime] = Field(
        None, description="Data de envio para a transportadora (pode ser nulo)"
    )
    order_delivered_customer_date: Optional[datetime] = Field(
        None, description="Data de entrega ao cliente (pode ser nulo)"
    )
    order_estimated_delivery_date: datetime = Field(
        ..., description="Data estimada de entrega (não nulo, >= purchase)"
    )

    # Validação extra: data estimada deve ser >= data da compra

    @field_validator("order_estimated_delivery_date")
    def valida_estimativa_maior_que_compra(cls, v, info):
        purchase = info.data.get("order_purchase_timestamp")
        if purchase and v < purchase:
            raise ValueError(
                "order_estimated_delivery_date deve ser >="
                "order_purchase_timestamp"
            )
        return v

    model_config = ConfigDict(
        validate_default=True,
        validate_assignment=True,
    )


class OrderItem(BaseModel):
    order_id: constr(min_length=32, max_length=32) = Field(
        ...,
        description="ID do pedido, deve existir em orders",
    )
    order_item_id: conint(ge=1) = Field(
        ..., description="ID do item do pedido, inteiro >= 1"
    )
    product_id: constr(min_length=1) = Field(
        ..., description="ID do produto, string não nula"
    )
    seller_id: constr(min_length=1) = Field(
        ..., description="ID do vendedor, string não nula"
    )
    shipping_limit_date: datetime = Field(
        ...,
        description=(
            "Data limite para envio, " "deve ser >= order_purchase_timestamp"
        ),
    )
    price: confloat(ge=0) = Field(
        ..., description="Preço do produto, float >= 0"
    )
    freight_value: confloat(ge=0) = Field(
        ..., description="Valor do frete, float >= 0"
    )

    # Validador extra para shipping_limit_date >= order_purchase_timestamp
    @field_validator("shipping_limit_date")
    def valida_shipping_limit_date(cls, v, info):
        purchase_date = info.data.get("order_purchase_timestamp")
        if purchase_date and v < purchase_date:
            raise ValueError(
                "shipping_limit_date deve ser >=" " order_purchase_timestamp"
            )
        return v

    model_config = ConfigDict(
        validate_default=True,
        validate_assignment=True,
    )
