import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import staff_member_required, login_required


User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'is_staff')


class Query():
    profile = graphene.Field(UserType)
    all_users = graphene.List(UserType)

    @login_required
    def resolve_profile(root, info):
        return info.context.user

    @staff_member_required
    def resolve_all_users(root, info):
        qs = User.objects.all()
        return qs


class Mutation():
    pass
