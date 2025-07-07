from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from unittest.mock import patch
from datetime import date

from .models import Receipt

class ReceiptAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="p")
        self.token = Token.objects.create(user=self.user)

    def auth(self):
        return {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}

    @patch("receipts.api_views.extract_receipt_data")
    def test_upload_receipt(self, mock_extract):
        mock_extract.return_value = (
            {"vendor": "Store", "total": 5.50, "date": date(2024, 1, 1)},
            "RAW",
        )
        img = SimpleUploadedFile("test.png", b"file", content_type="image/png")
        response = self.client.post("/api/upload/", {"image": img}, **self.auth())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Receipt.objects.count(), 1)
        r = Receipt.objects.first()
        self.assertEqual(r.vendor, "Store")
        self.assertEqual(float(r.total), 5.50)
        self.assertEqual(r.date, date(2024, 1, 1))

    def test_upload_receipt_no_file(self):
        response = self.client.post("/api/upload/", {}, **self.auth())
        self.assertEqual(response.status_code, 400)

    def test_update_receipt(self):
        r = Receipt.objects.create(user=self.user)
        payload = {"vendor": "New", "total": "12.34", "date": "2024-02-02"}
        response = self.client.put(
            f"/api/receipts/{r.id}/edit/",
            payload,
            content_type="application/json",
            **self.auth(),
        )
        self.assertEqual(response.status_code, 200)
        r.refresh_from_db()
        self.assertEqual(r.vendor, "New")
        self.assertEqual(float(r.total), 12.34)
        self.assertEqual(str(r.date), "2024-02-02")

    def test_monthly_summary(self):
        Receipt.objects.create(user=self.user, total=10, date=date(2024, 1, 5))
        Receipt.objects.create(user=self.user, total=5, date=date(2024, 2, 1))
        Receipt.objects.create(user=self.user, total=7, date=date(2024, 2, 18))
        response = self.client.get("/api/summary/monthly/", **self.auth())
        self.assertEqual(response.status_code, 200)
        data = response.json()
        months = {item["month"]: float(item["total"]) for item in data}
        self.assertEqual(months["2024-01-01"], 10.0)
        self.assertEqual(months["2024-02-01"], 12.0)

