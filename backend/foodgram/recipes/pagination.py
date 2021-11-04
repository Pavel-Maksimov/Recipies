from rest_framework.pagination import PageNumberPagination


class LimitPagePagination(PageNumberPagination):
    def get_page_size(self, request):
        try:
            return abs(int(request.query_params['limit']))
        except (KeyError, ValueError):
            pass
