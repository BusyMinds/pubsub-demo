import json

from django.http import Http404
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from .utils import PubSubClient


class DemoView(TemplateView):

    template_name = 'demo/demo.html'


@method_decorator(csrf_exempt, name='dispatch')
class APIView(View):

    def get(self, request, pk, *args, **kwargs):

        pubsub = PubSubClient()

        try:
            data = pubsub.pull(pk)
        except Http404:
            return JsonResponse({
                'error': 'No more data to pull.'
            }, status=404)

        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        pubsub = PubSubClient()

        payload = json.loads(request.body.decode('utf-8'))

        if payload.get('mailing_id') and payload.get('name'):
            pubsub.push(**payload)

            return JsonResponse({
                'message': 'Success',
                'payload': payload,
            })

        else:
            return JsonResponse({
                'error': 'The fields "mailing_id" and "name" are required.'
            }, status=400)
