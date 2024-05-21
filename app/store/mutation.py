import graphene
from django.utils import timezone
from graphql_jwt.decorators import login_required
from core.models import Product, Order, OrderItem, ShippingAddress
from core.types import OrderType, OrderItemType, ShippingAddressType


class OrderMutation(graphene.Mutation):
    """
    Create a New Order for Logged-in User
    """

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
        order = Order.objects.create(
            user=info.context.user,
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
                raise ValueError(
                    f"there isn't enough quantity for {product.name}"
                )

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


class OrderUpdateToPaidMutation(graphene.Mutation):
    """
    Update Order isPaid Value to True
    """

    class Arguments:
        id = graphene.UUID(required=True)

    order = graphene.Field(OrderType)

    @classmethod
    @login_required
    def mutate(
        cls,
        root,
        info,
        id
    ):
        order = Order.objects.get(id=id)
        order.is_paid = True
        order.paid_at = timezone.now()
        order.save()

        return OrderUpdateToPaidMutation(order=order)


class Mutation:
    create_order = OrderMutation.Field()
    update_order_to_paid = OrderUpdateToPaidMutation.Field()
