import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import staff_member_required, login_required
from .types import UserType


User = get_user_model()


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
