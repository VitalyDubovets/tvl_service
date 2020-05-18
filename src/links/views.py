from redis.exceptions import ConnectionError
from rest_framework.exceptions import NotFound, ValidationError, APIException
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.views import APIView

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
                raise APIException({'status': 'Connection to Redis is interrupted'})
        else:
            raise ValidationError({'status': 'Data is empty or incorrect'})
        return Response(response, status=HTTP_201_CREATED)


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
        return Response(response, status=HTTP_200_OK)
