from django.urls import path
from .views import register, login_view, logout_view, tender_list, apply_tender

urlpatterns = [
    path('', tender_list, name='tender_list'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('tender/<int:tender_id>/apply/', apply_tender, name='apply_tender'),




]

