import factory
import factory.fuzzy

from django.contrib.auth.models import User

from .. import models


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.fuzzy.FuzzyText()
    password = factory.fuzzy.FuzzyText()
    email = factory.Sequence(lambda n: 'user-%d@example.com' % n)
    first_name = factory.fuzzy.FuzzyText()
    last_name = factory.fuzzy.FuzzyText()

    @classmethod
    def _create(cls, target_class, **kwargs):
        """
        Use create_user, which performs some validation and normalizes
        the user's email address.
        """
        manager = cls._get_manager(target_class)
        username = kwargs.pop('username')
        email = kwargs.pop('email')
        password = kwargs.pop('password')
        user = manager.create_user(username, email, password)
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save(update_fields=kwargs.keys())
        return user
