from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination


class ListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    pagination_class.page_size_query_param = 'limit'


class ListCreateViewSet(mixins.CreateModelMixin,
                        ListViewSet):
    pass


class ListCreateDelViewSet(mixins.DestroyModelMixin, ListCreateViewSet):
    pass


class ListAllViewSet(mixins.UpdateModelMixin, ListCreateDelViewSet):
    pass
