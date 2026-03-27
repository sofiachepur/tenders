from django.contrib import admin
from .models import Tender, Proposal, Company, Winner


class WinnerAdmin(admin.ModelAdmin):
    list_display = ['tender', 'proposal', 'get_winner']

    def get_winner(self, obj):
        return obj.proposal.company.name

    get_winner.short_description = "Переможець"


admin.site.register(Tender)
admin.site.register(Proposal)
admin.site.register(Company)
admin.site.register(Winner, WinnerAdmin)