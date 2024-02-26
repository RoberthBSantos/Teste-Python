from django.core.exceptions import ValidationError

from accounts.models import User
from .models import Company, CompanyMember


def create_company(cnpj: str, razao_social: str, nome_fantasia: str, owner_id: int) -> Company:
    user = User.objects.get(id=owner_id)
    print(owner_id)
    company = Company(cnpj=cnpj, razao_social=razao_social, nome_fantasia=nome_fantasia)
    company.save()
    company.owner = user
    company.save()
    return company


def add_user_to_company(user_id: int, company_id: int):
    if CompanyMember.objects.filter(user_id=user_id, company_id=company_id).exists():
        raise ValidationError('User is already a member of the company.')

    try:
        user = User.objects.get(pk=user_id)
        company = Company.objects.get(pk=company_id)
    except (User.DoesNotExist, Company.DoesNotExist) as e:
        raise ValidationError(str(e))

    company_member = CompanyMember.objects.create(user=user, company=company)
    return company_member


def get_companies(user_id: int):
    company_memberships = CompanyMember.objects.filter(user_id=user_id)
    companies = [membership.company for membership in company_memberships]
    return companies


def get_members(company_id: int):
    company_memberships = CompanyMember.objects.filter(company_id=company_id)
    members = [membership.user for membership in company_memberships]
    return members