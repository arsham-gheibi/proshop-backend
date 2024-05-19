import graphene
import graphql_jwt
from user.query import Query as UserQuery
from user.mutation import Mutation as UserMutation
from store.query import Query as StoreQuery
from store.mutation import Mutation as StoreMutation


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
