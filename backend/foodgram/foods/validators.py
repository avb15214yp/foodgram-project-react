from rest_framework import serializers


def validate_array_duplicates(value, err_message):
    if not isinstance(value, list):
        return value
    if len(value) < 2:
        return value
    if True in set([value.count(tag) > 1 for tag in value]):
        raise serializers.ValidationError(
            err_message)
    return value
