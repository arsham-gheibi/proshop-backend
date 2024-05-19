import graphene
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required
from ..types import MutationUserType


User = get_user_model()


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
