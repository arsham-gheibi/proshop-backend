import graphene
from graphql_jwt.decorators import login_required
from core.models import Product, Order
from core.types import ProductType, OrderType


class Query():
    all_products = graphene.List(
        ProductType,
        name=graphene.String(),
        in_stock=graphene.Boolean()
    )

    product = graphene.Field(
        ProductType,
        id=graphene.UUID(required=True)
    )

    all_orders = graphene.List(
        OrderType,
        is_paid=graphene.Boolean()
    )

    order = graphene.Field(
        OrderType,
        id=graphene.UUID(required=True)
    )

    def resolve_all_products(
        root,
        info,
        name=None,
        in_stock=None
    ):
        qs = Product.objects.all()

        if name is not None:
            qs = qs.filter(name__icontains=name)

        if in_stock is not None:
            if in_stock:
                qs = qs.exclude(count_in_stock=0)

            elif not in_stock:
                qs = qs.filter(count_in_stock=0)

        return qs

    def resolve_product(
        root,
        info,
        id
    ):
        return Product.objects.get(id=id)

    @login_required
    def resolve_all_orders(
        root,
        info,
        is_paid=None
    ):
        user = info.context.user
        if user.is_staff:
            qs = Order.objects.all()
        else:
            qs = Order.objects.filter(user=user)

        if is_paid is not None:
            qs = qs.filter(is_paid=is_paid)

        return qs

    @login_required
    def resolve_order(
        root,
        info,
        id
    ):
        user = info.context.user
        order = Order.objects.get(id=id)
        return order if user.is_staff or order.user == user else None
