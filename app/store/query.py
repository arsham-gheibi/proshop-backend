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

    order = graphene.Field(
        OrderType,
        id=graphene.UUID(required=True)
    )

    def resolve_all_products(
        root,
        info,
        name='',
        in_stock=None
    ):
        qs = Product.objects.filter(
            name__icontains=name
        )

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
    def resolve_order(
        root,
        info,
        id
    ):
        return Order.objects.get(
            user=info.context.user,
            id=id
        )
