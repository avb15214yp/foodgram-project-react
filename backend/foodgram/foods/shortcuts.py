from rest_framework import status
from rest_framework.response import Response


def _get_queryset(klass):
    if hasattr(klass, "_default_manager"):
        return klass._default_manager.all()
    return klass


def get_object_or_response400(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    if not hasattr(queryset, "get"):

        if isinstance(klass, type):
            klass__name = klass.__name__
        else:
            klass__name = klass.__class__.__name__

        raise ValueError(
            "First argument to get_object_or_400() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return (True, queryset.get(*args, **kwargs))
    except queryset.model.DoesNotExist:
        object_name = queryset.model._meta.object_name
        error = {
            'errors': f'No {object_name} matches the given query.'
        }
        return (
            False,
            Response(status=status.HTTP_400_BAD_REQUEST, data=error)
        )
