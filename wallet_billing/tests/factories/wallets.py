import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from core.apps.wallets.models.transaction import WalletTransaction
from core.apps.wallets.models.wallets import Wallet


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    id = factory.Sequence(lambda n: n*2)
    username = factory.Faker("user_name")
    password = factory.LazyFunction(lambda: make_password('defaultpassword'))


class WalletFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Wallet

    id = factory.Faker("uuid4")
    balance = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    user = factory.SubFactory(UserFactory)
    is_active = factory.Faker("pybool")

class WalletTransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WalletTransaction

    id = factory.Faker("uuid4")
    balance_after = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    balance_before = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    operation_type = factory.Faker("random_element", elements=["deposit", "withdrawal"])
    amount = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    wallet = factory.SubFactory(WalletFactory)
    status = factory.Faker("random_element", elements=["success",])
