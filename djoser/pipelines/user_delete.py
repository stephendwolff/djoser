from django.contrib.auth import get_user_model

from djoser import signals
from djoser import utils
from djoser.conf import settings
from djoser.pipelines.base import BasePipeline

User = get_user_model()


def serialize_request(request, context):
    serializer_class = settings.SERIALIZERS.user_delete
    serializer = serializer_class(data=request.data, **{'context': context})
    serializer.is_valid(raise_exception=True)
    return {'user_data': serializer.validated_data}


def perform(request, context):
    user = request.user
    utils.logout_user(request)
    request.user.delete()
    return {'user': user}


class Pipeline(BasePipeline):
    steps = settings.PIPELINES.user_delete
