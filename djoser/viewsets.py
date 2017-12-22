from django.contrib.auth import get_user_model
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from djoser import pipelines

User = get_user_model()


class UserViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        pipeline = pipelines.user_create.Pipeline(request)
        response_data = pipeline.run()['response']
        return Response(response_data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        pipeline = pipelines.user_delete.Pipeline(request)
        pipeline.run()
        return Response(status=status.HTTP_204_NO_CONTENT)
