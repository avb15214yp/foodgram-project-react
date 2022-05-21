from rest_framework import mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination


class BaseViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination


class ListCreateViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = LimitOffsetPagination


class ListCreateUpdateViewSet(
                        mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.RetrieveModelMixin, viewsets.GenericViewSet,
                        mixins.UpdateModelMixin, mixins.DestroyModelMixin
        ):
    pagination_class = LimitOffsetPagination


class ListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    pagination_class = LimitOffsetPagination
