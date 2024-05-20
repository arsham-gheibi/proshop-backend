import graphene
import graphql_jwt
from django.middleware.csrf import get_token
from core.types import CSRFTokenType
from user.query import Query as UserQuery
from user.mutation import Mutation as UserMutation
from store.query import Query as StoreQuery
from store.mutation import Mutation as StoreMutation


class Query(
    graphene.ObjectType,
    UserQuery,
    StoreQuery
):
    csrf_token = graphene.Field(CSRFTokenType)

    def resolve_csrf_token(root, info):
        return CSRFTokenType(csrf_token=get_token(info.context))


class Mutation(
    graphene.ObjectType,
    UserMutation,
    StoreMutation
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
