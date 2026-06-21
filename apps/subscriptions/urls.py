from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.SubscriptionManageView.as_view(), name='manage'),
    path('upgrade/<int:plan_id>/', views.upgrade_subscription, name='upgrade'),
    path('cancel/', views.cancel_subscription, name='cancel'),
    path('payment/<int:subscription_id>/', views.process_payment, name='payment'),
]