import graphene
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import staff_member_required, login_required
from core.types import UserType


User = get_user_model()


class UserMutationCreate(graphene.Mutation):
    """
    Create a New User
    """

    class Arguments:
        name = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

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
    """
    Update Current User Detail
    """

    class Arguments:
        name = graphene.String()
        username = graphene.String()
        password = graphene.String()

    user = graphene.Field(UserType)

    @classmethod
    @login_required
    def mutate(
        cls,
        root,
        info,
        name=None,
        username=None,
        password=None
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


class UserMutationDelete(graphene.Mutation):
    """
    Delete an Specefice User
    """

    class Arguments:
        id = graphene.UUID(required=True)

    user = graphene.Field(UserType)

    @classmethod
    @staff_member_required
    def mutate(
        cls,
        root,
        info,
        id
    ):
        User.objects.get(id=id).delete()
        return True


class Mutation:
    create_user = UserMutationCreate.Field()
    update_user = UserMutationUpdate.Field()
    delete_user = UserMutationDelete.Field()
