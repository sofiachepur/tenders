# tenders/tests.py
from django.test import TestCase
from django.core import mail

class EmailTestCase(TestCase):
    def test_send_email(self):
        # Надсилаємо лист
        mail.send_mail(
            'Тестовий лист',
            'Перевірка роботи пошти',
            'your_email@gmail.com',
            ['recipient_email@gmail.com'],
        )
        # Перевірка, що лист відправлено
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Тестовий лист')