from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.models import Patient
from accounts.serializers import *
from accounts.services import *
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import  *
from django.db.models import Prefetch
from django_filters import rest_framework as filters
from accounts.filters         import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters

from visit.models.models import Visit
from accounts.pagination import CustomPagination
from safedelete import HARD_DELETE, HARD_DELETE_NOCASCADE

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage Patient model.
    """
    queryset = Patient.objects.all()

    serializer_class = PatientSerializer
    pagination_class = CustomPagination

    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_class =  PatientFilter

    permission_classes = [IsAuthenticated,CustomPermission]
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Patient.objects.all()
        else:
            doctor=Doctor.objects.filter(user=self.request.user).first()
            if doctor:
                patients=Visit.objects.filter(doctors__in=[doctor]).values('patient').distinct()
                return Patient.objects.filter(id__in=patients)
            
            return Patient.objects.filter(user=self.request.user)
        
    def create(self , request, *args, **kwargs):

        serializer = PatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient=serializer.save()

        user=User.objects.create_user(username=serializer.data['national_id'],password=serializer.data['national_id'])
        patient.user=user
        patient.save()
        
        
        return Response(PatientSerializer(patient).data, status=status.HTTP_201_CREATED)
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'method', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=['soft', 'hard'],
                description='Specify the delete method (soft or hard). Default is soft.'
            )
        ]
    )
    def destroy(self, request, *args, **kwargs):
        if  request.query_params.get('method')=='hard':
                instance = self.get_object()
                instance.delete(force_policy=HARD_DELETE)
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return super().destroy(request, *args, **kwargs)
    

    def get_deleted(self, request, *args, **kwargs):
        paginator = self.pagination_class()
        deleted_patients = Patient.deleted_objects.all()
        result_page = paginator.paginate_queryset(deleted_patients, request)
        serializer = self.get_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    

from rest_framework import viewsets
class DeletedPatientView(viewsets.ViewSet):
    serializer_class = RestorePatientSerializer
    queryset = Patient.deleted_objects.all()
    permission_classes = [IsAuthenticated,CustomPermission]
    def restore(self, request, *args, **kwargs):
        serializer = RestorePatientSerializer(data={'id':kwargs['pk']})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        instance = serializer.validated_data['id']
        instance.undelete()
        return Response(status=status.HTTP_200_OK)
    def destroy(self, request, *args, **kwargs):
        serializer = RestorePatientSerializer(data={'id':kwargs['pk']})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        instance = serializer.validated_data['id']
        instance.delete(force_policy=HARD_DELETE)
        return Response(status=status.HTTP_204_NO_CONTENT)