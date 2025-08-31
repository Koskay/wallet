import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from core.apps.wallets.models.wallets import Wallet


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    id = factory.Sequence(lambda n: n*2)
    username = factory.Faker("user_name")
    password = factory.LazyFunction(lambda: make_password('defaultpassword'))


class WalletFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания тестовых категорий продуктов

    Генерирует:
    - случайное название категории
    - уникальный slug
    - случайный URL изображения
    """

    class Meta:
        model = Wallet

    id = factory.Faker("uuid4")
    balance = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    user = factory.SubFactory(UserFactory)
    is_active = factory.Faker("pybool")
