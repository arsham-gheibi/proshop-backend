import graphene
from graphql_jwt.decorators import login_required
from core.models import Product, Order, OrderItem, ShippingAddress
from ..types import OrderType, OrderItemType, ShippingAddressType


class OrderMutation(graphene.Mutation):
    class Arguments:
        order_items = graphene.JSONString(required=True)
        payment_method = graphene.String(required=True)
        tax_price = graphene.String(required=True)
        shipping_price = graphene.String(required=True)
        total_price = graphene.String(required=True)
        country = graphene.String(required=True)
        city = graphene.String(required=True)
        address = graphene.String(required=True)
        postal_code = graphene.String(required=True)

    order = graphene.Field(OrderType)
    orderitems = graphene.List(OrderItemType)
    shipping_address = graphene.Field(ShippingAddressType)

    @classmethod
    @login_required
    def mutate(
        cls,
        root,
        info,
        order_items,
        payment_method,
        tax_price,
        shipping_price,
        total_price,
        country,
        city,
        address,
        postal_code
    ):
        user = info.context.user
        order = Order.objects.create(
            user=user,
            payment_method=payment_method,
            tax_price=tax_price,
            shipping_price=shipping_price,
            total_price=total_price
        )

        for order_item in order_items:
            product = Product.objects.get(id=order_item['id'])
            qty = int(order_item['qty'])

            if product.count_in_stock >= qty:
                product.count_in_stock -= qty
                product.save()

                OrderItem.objects.create(
                    product=product,
                    order=order,
                    name=product.name,
                    qty=qty,
                    price=product.price
                )

            else:
                return False

        shipping_address = ShippingAddress.objects.create(
            order=order,
            country=country,
            city=city,
            address=address,
            postal_code=postal_code,
            shipping_price=shipping_price
        )

        order_items = order.orderitem_set.all()

        return OrderMutation(
            order=order,
            orderitems=order_items,
            shipping_address=shipping_address
        )


class Mutation():
    create_order = OrderMutation.Field()
