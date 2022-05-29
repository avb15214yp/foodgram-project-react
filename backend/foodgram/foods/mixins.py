from rest_framework import mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination


class ListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    pagination_class = LimitOffsetPagination


class ListCreateViewSet(mixins.CreateModelMixin,
                        ListViewSet):
    pass


class ListCreateDelViewSet(mixins.DestroyModelMixin, ListCreateViewSet):
    pass


class ListAllViewSet(mixins.UpdateModelMixin, ListCreateDelViewSet):
    pass
