from django.test import TestCase
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import ScoreEvent  # Adjust the import path if needed

User = get_user_model()


class ScoreEventUniqueConstraintTests(TestCase):
    def setUp(self):
        # Create a test user that will be used for all events.
        self.user = User.objects.create_user(
            phone_number="1234567890", password="password")
        # Set up some default dates and values for testing.
        self.today = timezone.now().date()
        self.yesterday = self.today - timezone.timedelta(days=1)

    def test_unique_daily_login_per_user_per_day(self):
        daily_value = 10
        # Create a daily login event for today.
        event1 = ScoreEvent.objects.create(
            user=self.user,
            score_title="daily_login",
            value=daily_value,
            # You can rely on auto_now_add but here we set it explicitly.
            event_date=self.today
        )
        self.assertIsNotNone(event1)

        # Duplicate daily login event for the same day should fail.
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ScoreEvent.objects.create(
                    user=self.user,
                    score_title="daily_login",
                    value=daily_value,
                    event_date=self.today  # Same date as event1.
                )

        # Creating a daily login for a different day should succeed.
        event2 = ScoreEvent.objects.create(
            user=self.user,
            score_title="daily_login",
            value=daily_value,
            event_date=self.yesterday
        )
        self.assertIsNotNone(event2)

    def test_unique_order_constraint(self):
        order_value = 30
        order_id = "order123"
        # Create an order event.
        order_event1 = ScoreEvent.objects.create(
            user=self.user,
            score_title="order",
            value=order_value,
            order_id=order_id
        )
        self.assertIsNotNone(order_event1)

        # Attempting to create a duplicate order event (same order_id) for the same user should fail.
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ScoreEvent.objects.create(
                    user=self.user,
                    score_title="order",
                    value=order_value,
                    order_id=order_id
                )

        # An order event with a different order_id should succeed.
        order_event2 = ScoreEvent.objects.create(
            user=self.user,
            score_title="order",
            value=order_value,
            order_id="order456"
        )
        self.assertIsNotNone(order_event2)

    def test_unique_referral_constraint(self):
        referral_value = 20
        referral_phone = "5551234567"
        # Create a referral event.
        referral_event1 = ScoreEvent.objects.create(
            user=self.user,
            score_title="referral",
            value=referral_value,
            referral_phone_number=referral_phone
        )
        self.assertIsNotNone(referral_event1)

        # Duplicate referral events using the same referral_phone_number for the same user should fail.
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ScoreEvent.objects.create(
                    user=self.user,
                    score_title="referral",
                    value=referral_value,
                    referral_phone_number=referral_phone
                )

        # Creating a referral event with a different referral phone number should work.
        referral_event2 = ScoreEvent.objects.create(
            user=self.user,
            score_title="referral",
            value=referral_value,
            referral_phone_number="5559876543"
        )
        self.assertIsNotNone(referral_event2)
