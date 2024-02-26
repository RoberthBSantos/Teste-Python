from django.core.exceptions import ValidationError
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.serializers import UserSerializer
from .models import Company
from .serializers import CompanySerializer, CompanyMemberSerializer
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
                serializer.validated_data['corporate_name'],
                serializer.validated_data['trade_name'],
                owner_id=self.request.user.id,
            )
            output_serializer = CompanySerializer(company, context={'request': request})
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyMemberView(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        company_id = request.data.get('company')

        try:
            company_member = services.add_user_to_company(user_id, company_id)
            serializer = CompanyMemberSerializer(company_member)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'message': e.message}, status=status.HTTP_400_BAD_REQUEST)

    def get_companies(self, request):
        try:
            companies = services.get_companies(self.request.user.id)
            print(companies[0])
            serializer = CompanySerializer(companies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'message': e.message}, status=status.HTTP_400_BAD_REQUEST)

    def get_members(self, request):
        try:
            members = services.get_members(request.data['company_id'])
            serializer = UserSerializer(members, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'message': e.message}, status=status.HTTP_400_BAD_REQUEST)
