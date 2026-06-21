from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Plan, Subscription

class SubscriptionManageView(LoginRequiredMixin, TemplateView):
    template_name = 'subscriptions/manage.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plans'] = Plan.objects.all()
        context['current_subscription'] = Subscription.objects.filter(
            business=self.request.user.business,
            is_active=True
        ).first()
        return context

@login_required
def upgrade_subscription(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)
    messages.success(request, f'Upgraded to {plan.name} plan successfully!')
    return redirect('subscriptions:manage')

@login_required
def cancel_subscription(request):
    messages.success(request, 'Subscription cancelled successfully!')
    return redirect('subscriptions:manage')

@login_required
def process_payment(request, subscription_id):
    return render(request, 'subscriptions/payment.html')