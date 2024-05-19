import graphene
from graphene_django import DjangoObjectType
from core.models import Product


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'image', 'price', 'brand', 'category',
            'description', 'rating', 'num_reviews', 'count_in_stock'
        )


class Query():
    all_products = graphene.List(
        ProductType,
        name=graphene.String(),
        in_stock=graphene.Boolean()
    )

    product = graphene.Field(
        ProductType,
        id=graphene.UUID()
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


class Mutation():
    pass
