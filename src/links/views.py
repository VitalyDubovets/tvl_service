from redis.exceptions import ConnectionError
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.views import APIView
import pdb

from .services import get_unique_domains_from_links

from core.redis_db import RedisDB


class LinksCreateAPI(APIView):
    db = RedisDB()

    def post(self, request, *args, **kwargs):
        links = request.data.get('links')
        if links and isinstance(links, list):
            try:
                self.db.zadd_with_unix_time('links', links)
                response = {'status': 'ok'}
            except ConnectionError:
                response = {'status': 'Connection to Redis is interrupted'}
        else:
            response = {'status': 'Data is empty or incorrect.'}
        return Response(response)


class LinksGetAPI(APIView):
    db = RedisDB()

    def get(self, request, *args, **kwargs):
        if request.GET.get('from') and request.GET.get('to'):
            try:
                links = self.db.zrange_by_unix_time('links', int(request.GET.get('from')), int(request.GET.get('to')))
            except ValueError:
                raise ValidationError({'status': 'Incorrect get params'})
        else:
            links = self.db.zrange_decoded('links')
        unique_domains = get_unique_domains_from_links(links)
        if not unique_domains:
            raise NotFound({'status': 'The last visited domains were not found'})
        response = {'domains': unique_domains, 'status': 'ok'}
        return Response(response)
