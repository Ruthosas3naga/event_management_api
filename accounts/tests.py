from django.test import TestCase
from django.test import TestCase
from .models import CustomUser

class CustomUserModelTests(TestCase):
    
    def setUp(self):
        """Create a test user."""
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='password123',
            phone_number='1234567890',
            bio='This is a test user.',
            email='testuser@example.com'
        )

    def test_user_creation(self):
        """Test that the user was created successfully."""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.phone_number, '1234567890')
        self.assertEqual(self.user.bio, 'This is a test user.')

    def test_str_method(self):
        """Test the string representation of the user."""
        self.assertEqual(str(self.user), 'testuser')

    def test_blank_fields(self):
        """Test that blank fields are handled correctly."""
        user = CustomUser.objects.create_user(username='blankuser', password='password')
        self.assertIsNone(user.phone_number)  # This will be None as expected
        self.assertIsNone(user.bio)           # This will be None as expected
        self.assertIsNone(user.email)         # This will be None as expected

    def test_user_update(self):
        """Test that the user can be updated."""
        self.user.phone_number = '0987654321'
        self.user.save()
        self.assertEqual(self.user.phone_number, '0987654321')

    def test_user_authentication(self):
        """Test that the user can authenticate."""
        user = CustomUser.objects.get(username='testuser')
        self.assertTrue(user.check_password('password123'))
