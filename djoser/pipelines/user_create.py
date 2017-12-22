from django.contrib.auth import get_user_model

from djoser import signals
from djoser import utils
from djoser.conf import settings
from djoser.pipelines.base import BasePipeline

User = get_user_model()


def serialize_request(request, context):
    serializer_class = settings.SERIALIZERS.user_create
    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    return {'user_data': serializer.validated_data}


def perform(request, context):
    assert 'user_data' in context

    try:
        username_field = User.USERNAME_FIELD
        username = context['user_data'][username_field]
        user = User.objects.get(**{username_field: username})
    except User.DoesNotExist:
        user = User.objects.create_user(**context['user_data'])

    return {'user': user}


def signal(request, context):
    assert context['user']
    user = context['user']

    signals.user_created.send(sender=None, user=user, request=request)


def activation_email(request, context):
    utils.validate_context_user_for_email(context)
    user = context['user']

    user_email = utils.get_user_email(user)
    assert user_email is not None
    to = [user_email]
    settings.EMAIL.activation(request, context).send(to)

    user.is_active = False
    user.save(update_fields=['is_active'])


def confirmation_email(request, context):
    utils.validate_context_user_for_email(context)
    user = context['user']

    user_email = utils.get_user_email(user)
    assert user_email is not None
    to = [user_email]
    settings.EMAIL.confirmation(request, context).send(to)


def serialize_instance(request, context):
    assert context['user']

    serializer_class = settings.SERIALIZERS.user_create
    serializer = serializer_class(context['user'])
    return {'response': serializer.data}


class Pipeline(BasePipeline):
    steps = settings.PIPELINES.user_create
