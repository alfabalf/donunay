from django.test import TestCase
from django.db.utils import DataError

from restapp.models import CustomUser


class CustomUserModelTest(TestCase):

    def test_max_email_address_length_max_100(self):
        CustomUser.objects.create(email='ok@test.com', password='password')

        email = '{}@notok.com'.format('x' * 91)

        with self.assertRaises(DataError):
            CustomUser.objects.create_user(email=email, password='password')



