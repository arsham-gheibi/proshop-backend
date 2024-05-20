import json
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from graphene_django.views import GraphQLView


class AbstractGraphQLView(GraphQLView):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        query = json.loads(body_unicode).get('query', '')

        if 'mutation' in query:
            return csrf_protect(super().dispatch)(request, *args, **kwargs)

        return super().dispatch(request, *args, **kwargs)
