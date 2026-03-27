from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Tender(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    winner = models.ForeignKey(
        Company, on_delete=models.SET_NULL, blank=True, null=True, related_name='won_tenders'
    )
    status = models.CharField(
        max_length=20,
        choices=[('open', 'Відкритий'), ('awarded', 'Призначено')],
        default='open'
    )

    def __str__(self):
        return self.title

class Proposal(models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.company.name} → {self.tender.title}"

class Winner(models.Model):
    tender = models.OneToOneField(
        Tender,
        on_delete=models.CASCADE,
        related_name='winner_record'  # <- додаємо унікальне ім'я
    )
    proposal = models.OneToOneField(Proposal, on_delete=models.CASCADE)
    selected_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # оновлюємо тендер
        self.tender.winner = self.proposal.company
        self.tender.status = 'awarded'
        self.tender.save()