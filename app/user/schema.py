import graphene
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import staff_member_required, login_required
from .types import UserType, MutationUserType


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


class UserMutationCreate(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        username = graphene.String()
        password = graphene.String()

    user = graphene.Field(MutationUserType)

    @classmethod
    def mutate(
        cls,
        root,
        info,
        name,
        username,
        password
    ):
        user = User.objects.create(
            name=name,
            username=username,
            password=make_password(password)
        )

        return UserMutationCreate(user=user)


class UserMutationUpdate(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        username = graphene.String()
        password = graphene.String()

    user = graphene.Field(MutationUserType)

    @classmethod
    @login_required
    def mutate(
        cls,
        root,
        info,
        name,
        username,
        password
    ):
        user = info.context.user
        if name is not None:
            user.name = name
        if username is not None:
            user.username = username
        if password is not None:
            user.password = make_password(password)

        user.save()

        return UserMutationUpdate(user=user)


class Mutation():
    create_user = UserMutationCreate.Field()
    update_user = UserMutationUpdate.Field()
