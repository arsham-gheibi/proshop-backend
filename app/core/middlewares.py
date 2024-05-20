import json
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from graphene_django.views import GraphQLView


class AbstractGraphQLView(GraphQLView):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        try:
            body_unicode = request.body.decode('utf-8')
            query = json.loads(body_unicode).get('query', '')

            if 'mutation' in query.lower():
                return csrf_protect(super().dispatch)(request, *args, **kwargs)

        except (json.JSONDecodeError, UnicodeDecodeError):
            # Handle decoding errors and log them if necessary
            pass

        return super().dispatch(request, *args, **kwargs)
