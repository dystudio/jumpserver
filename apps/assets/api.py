# ~*~ coding: utf-8 ~*~

from rest_framework import viewsets, generics, mixins

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin, ListBulkCreateUpdateDestroyAPIView
from django.shortcuts import get_object_or_404

from common.mixins import IDInFilterMixin
from common.utils import get_object_or_none, signer
from .hands import IsSuperUserOrAppUser, IsSuperUser
from .models import AssetGroup, Asset, IDC, SystemUser, AdminUser
from . import serializers


class AssetViewSet(IDInFilterMixin, viewsets.ModelViewSet):
    """API endpoint that allows Asset to be viewed or edited."""
    queryset = Asset.objects.all()
    serializer_class = serializers.AssetSerializer
    filter_fields = ('id', 'ip', 'hostname')
    permission_classes = (IsSuperUserOrAppUser,)

    def get_queryset(self):
        queryset = super(AssetViewSet, self).get_queryset()
        idc_id = self.request.query_params.get('idc_id', '')
        asset_group_id = self.request.query_params.get('asset_group_id', '')
        if idc_id:
            queryset = queryset.filter(idc__id=idc_id)

        if asset_group_id:
            queryset = queryset.filter(groups__id=asset_group_id)
        return queryset


class AssetGroupViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows AssetGroup to be viewed or edited.
        some other comment
    """
    queryset = AssetGroup.objects.all()
    serializer_class = serializers.AssetGroupSerializer


class AssetUpdateGroupApi(generics.RetrieveUpdateAPIView):
    queryset = Asset.objects.all()
    serializer_class = serializers.AssetUpdateGroupSerializer
    permission_classes = (IsSuperUser,)


class IDCViewSet(viewsets.ModelViewSet):
    """API endpoint that allows IDC to be viewed or edited."""
    queryset = IDC.objects.all()
    serializer_class = serializers.IDCSerializer
    permission_classes = (IsSuperUser,)


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = AdminUser.objects.all()
    serializer_class = serializers.AdminUserSerializer
    permission_classes = (IsSuperUser,)


class SystemUserViewSet(viewsets.ModelViewSet):
    queryset = SystemUser.objects.all()
    serializer_class = serializers.SystemUserSerializer
    permission_classes = (IsSuperUser,)


class SystemUserUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = Asset.objects.all()
    serializer_class = serializers.AssetUpdateSystemUserSerializer
    permission_classes = (IsSuperUser,)


# class IDCAssetsApi(generics.ListAPIView):
#     model = IDC
#     serializer_class = serializers.AssetSerializer
#
#     def get(self, request, *args, **kwargs):
#         filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
#         self.object = get_object_or_404(self.model, **filter_kwargs)
#         return super(IDCAssetsApi, self).get(request, *args, **kwargs)
#
#     def get_queryset(self):
#         return self.object.assets.all()


class AssetListUpdateApi(IDInFilterMixin, ListBulkCreateUpdateDestroyAPIView):
    queryset = Asset.objects.all()
    serializer_class = serializers.AssetSerializer
    permission_classes = (IsSuperUser,)


class SystemUserAuthInfoApi(generics.RetrieveAPIView):
    queryset = SystemUser.objects.all()
    permission_classes = (IsSuperUserOrAppUser,)

    def retrieve(self, request, *args, **kwargs):
        system_user = self.get_object()
        data = {
            'id': system_user.id,
            'name': system_user.name,
            'username': system_user.username,
            'password': system_user.password,
            'private_key': system_user.private_key,
            'auth_method': system_user.auth_method,
        }
        return Response(data)

