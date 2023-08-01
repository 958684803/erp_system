import logging

from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger('erp')

class Hello(APIView):

    def get(self, request):
        logger.info('hello info')
        logger.debug('hello debug')
        logger.error('hello error')
        return Response({
            'message': 'test'
        })