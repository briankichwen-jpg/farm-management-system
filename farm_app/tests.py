from django.test import TestCase
from django.contrib.auth.models import User
from .models import FarmerProfile, Crop, Livestock
from datetime import date

class FarmerProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testfarmer@test.com',
            email='testfarmer@test.com',
            password='testpass123'
        )
        self.farmer = FarmerProfile.objects.create(
            user=self.user,
            date_of_birth=date(1990, 5, 15)
        )

    def test_farmer_profile_creation(self):
        self.assertEqual(self.farmer.user.email, 'testfarmer@test.com')

class CropTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testfarmer@test.com',
            email='testfarmer@test.com',
            password='testpass123'
        )
        self.farmer = FarmerProfile.objects.create(
            user=self.user,
            date_of_birth=date(1990, 5, 15)
        )
        self.crop = Crop.objects.create(
            farmer=self.farmer,
            crop_type='maize',
            variety='H614',
            planting_date=date(2024, 3, 1),
            land_size=2,
            labour_cost=1000,
            fertilizer_cost=2000,
            herbicide_cost=500,
            pesticide_cost=300,
            quantity_harvested=50,
            selling_price=100
        )

    def test_crop_total_expenses(self):
        self.assertEqual(self.crop.total_expenses(), 3800)

    def test_crop_total_income(self):
        self.assertEqual(self.crop.total_income(), 5000)

    def test_crop_profit(self):
        self.assertEqual(self.crop.profit(), 1200)
