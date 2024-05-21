import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import staff_member_required, login_required
from core.types import UserType


User = get_user_model()


class Query:
    all_users = graphene.List(UserType)
    user = graphene.Field(
        UserType,
        id=graphene.UUID(required=True)
    )

    profile = graphene.Field(UserType)

    @staff_member_required
    def resolve_all_users(root, info):
        return User.objects.all()

    @staff_member_required
    def resolve_user(root, info, id):
        return User.objects.get(id=id)

    @login_required
    def resolve_profile(root, info):
        return info.context.user
