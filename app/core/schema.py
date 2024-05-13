import graphene
import graphql_jwt
from user.schema import (
    Query as UserQuery,
    Mutation as UserMutation
)

from store.schema import (
    Query as StoreQuery,
    Mutation as StoreMutation
)


class Query(
    graphene.ObjectType,
    UserQuery,
    StoreQuery
):
    pass


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
