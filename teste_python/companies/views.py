from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer
from . import services


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            company = services.create_company(
                serializer.validated_data['cnpj'],
                serializer.validated_data['razao_social'],
                serializer.validated_data['nome_fantasia'],
                serializer.validated_data.get('users', []),
                owner_id=self.request.user.id,
            )
            output_serializer = CompanySerializer(company, context={'request': request})
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
