from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views


app_name = 'account'

urlpatterns = [
    # post views
    path('login/',
        auth_views.LoginView.as_view(
            template_name='account/login.html'
        ), name='login'),
    path('logout/',
        auth_views.LogoutView.as_view(
            template_name='account/logout.html',
        ), name='logout'),
    path('password_change/',
          auth_views.PasswordChangeView.as_view(
            template_name='account/password_change.html',
            success_url=reverse_lazy('account:password_change_done'),
          ), name='password_change'),
    path('password_change/done/',
          auth_views.PasswordChangeDoneView.as_view(
            template_name='account/password_reset_done.html'
          ), name='password_change_done'),

    # reset password urls
    path('password_reset/',
          auth_views.PasswordResetView.as_view(
            template_name='account/password_reset.html',
            success_url=reverse_lazy('account:password_reset_done'),
          ),
          name='reset_password'),
    path('password_reset/done/',
          auth_views.PasswordResetDoneView.as_view(
            template_name='account/password_reset_from_key.html',
          ), name='password_reset_done'),
    path('reset/done/',
            auth_views.PasswordResetCompleteView.as_view(
            template_name='account/password_reset_from_key_done.html'
        ), name='password_reset_complete'),
    path('reset/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(
            template_name='account/password_reset_from_key_done.html',
          ), name='password_reset_confirm'),

    # signup user url
    path('signup/', views.signup, name='signup'),

    # dashboard urls
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/address/', views.dashboard_change_address,
                                name='dashboard_change_address'),
    path('dashboard/customer/', views.dashoard_customer_edit,
                                name='dashoard_customer_edit'),
    path('dashboard/card/', views.dashboard_credit_card_edit,
                                name='dashboard_credit_card_edit'),
    path('dashboard/password/', views.dashboard_user_password_edit,
                                name='dashboard_user_password_edit'),
]
