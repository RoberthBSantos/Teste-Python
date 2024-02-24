from accounts.models import User
from .models import Company


def create_company(cnpj: str, razao_social: str, nome_fantasia: str, user_ids: list, owner_id: int) -> Company:
    user = User.objects.get(id=owner_id)
    print(owner_id)
    company = Company(cnpj=cnpj, razao_social=razao_social, nome_fantasia=nome_fantasia)
    company.save()
    company.owner = user
    company.users.set(user_ids)
    company.save()
    return company
