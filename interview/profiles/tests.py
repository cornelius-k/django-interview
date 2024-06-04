from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class UserManagerTests(TestCase):

    User = get_user_model()

    def test_create_user(self):
        '''
        Test that a normal user can be created
        '''
        user = self.User.objects.create_user(email="test@test.com", password="test")
        self.assertEqual(user.email, 'test@test.com')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
    
    def test_create_super_user(self):
        '''
        Test that a superuser can be created
        '''
        user = self.User.objects.create_superuser(email="test@test.com", password="test")
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_user_email_validation(self):
        '''
        Test that correct exceptions are raised when invalid email is used
        '''
        # test for missing email
        with self.assertRaises(ValidationError):
            self.User.objects.create_user(email="", password="")

        # test for invalid email
        with self.assertRaises(ValidationError):
            self.User.objects.create_user(email="invalid@", password="")

    def test_create_super_user_email_validation(self):
        '''
        Test that correct exceptions are raised when invalid email is used
        '''
        # test for missing email
        with self.assertRaises(ValidationError):
            self.User.objects.create_superuser(email="", password="")

        # test for invalid email
        with self.assertRaises(ValidationError):
            self.User.objects.create_superuser(email="invalid@", password="")

