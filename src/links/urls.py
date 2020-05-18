from django.urls import path

from links.views import *


urlpatterns = [
    path('visited_links', LinksCreateAPI.as_view()),
    path('visited_domains', LinksGetAPI.as_view())
]
