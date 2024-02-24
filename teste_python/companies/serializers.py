from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'owner', 'cnpj', 'razao_social', 'nome_fantasia', 'users')

    def validate_cnpj(self, value):
        # Aqui você pode adicionar validação para CNPJ, por exemplo:
        if Company.objects.filter(cnpj=value).exists():
            raise serializers.ValidationError("Uma empresa com este CNPJ já existe.")
        return value
