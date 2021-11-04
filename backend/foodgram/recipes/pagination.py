from django.conf import settings

from rest_framework.pagination import PageNumberPagination


class LimitPagePagination(PageNumberPagination):
    def get_page_size(self, request):
        try:
            return abs(int(request.query_params['limit']))
        except (KeyError, ValueError):
            return settings.DEFAULT_PAGE_SIZE
