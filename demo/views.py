import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from .utils import PubSubClient


class DemoView(TemplateView):

    template_name = 'demo/demo.html'


@method_decorator(csrf_exempt, name='dispatch')
class APIView(View):

    def get(self, request, *args, **kwargs):

        pubsub = PubSubClient()

        return JsonResponse({
            'message': pubsub.pull()
        })

    def post(self, request, *args, **kwargs):
        pubsub = PubSubClient()

        msg = json.loads(request.body.decode('utf-8'))['data']

        pubsub.push(msg)

        return JsonResponse({
            'message': 'Success',
        })
