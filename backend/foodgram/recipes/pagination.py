from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class LimitPagePagination(PageNumberPagination):
    """
    Custom pagination class.

    Take 'limit' and 'page' query parameters:
    -'limit': to use it as pase size.
    If 'limit' query parameter is not fould use 'DEFAULT_PAGE_SIZE'
    constant from settings.py.
    -'page': page number to show.
    """
    def get_page_size(self, request):
        try:
            return abs(int(request.query_params['limit']))
        except (KeyError, ValueError):
            return settings.DEFAULT_PAGE_SIZE
