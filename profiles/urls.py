from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetView
from django.contrib.auth.forms import SetPasswordForm

from .forms import UserPasswordResetForm, UserNewPasswordForm

urlpatterns = [
    path('profile/<str:name>', views.profile, name='profiles'),
    path('profile/<str:name>/settings', views.settings, name='settings'),
    path('profile/<str:name>/delete', views.delete, name='delete'),
    path('profile/<str:name>/cart', views.cart, name='cart'),
    path('profile/<str:name>/stats', views.stats, name='stats'),
    #password changeing

    path('change-password/success', PasswordChangeDoneView.as_view(template_name = 'profiles/change_password_success.html'), name = 'password_change_done'),
    path('profile/<str:name>/change-password', PasswordChangeView.as_view(
        template_name = 'profiles/change_password.html',
        success_url = reverse_lazy('password_change_done'),
    ), name='password_change'),

    #password reseting

    path('reset-password/', views.password_reset_request ,name='reset_password'),
    path('reset-password/sent', PasswordResetDoneView.as_view(template_name ='profiles/password_reset_done.html'), name = 'password_reset_done'),
    path('reset-password/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name = 'profiles/password_reset_confirm.html', form_class = SetPasswordForm), name='password_reset_confirm'),
    path('reset-password/complete', PasswordResetCompleteView.as_view(template_name ='profiles/password_reset_complete.html'), name='password_reset_complete'),
    
    path('profile/<str:name>/payment-result', views.payment_result, name='payment_result')
]