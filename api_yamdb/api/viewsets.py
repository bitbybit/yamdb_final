from rest_framework import mixins, viewsets


class CreateModelViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass
