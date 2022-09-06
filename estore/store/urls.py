from django.urls import path
from . import views
from store.forms import LoginForm, SetPasswordForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth import views as auth_views

app_name = 'store'

urlpatterns = [
    # Home URL
    path('', views.home, name="home"),

    # Cart and Checkout URL
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('incr-cart/<int:cart_id>/', views.incr_cart_item, name='incr-cart'),
    path('decr-cart/<int:cart_id>/', views.decr_cart_item, name='decr-cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),

    # Products URL
    path('product/<slug:slug>/', views.detail, name='product-detail'),
    path('categories/', views.all_categories, name='all-categories'),
    path('<slug:slug>/', views.category_products, name='category-products'),
    path('shop/', views.shop, name='shop'),

    # Authentication URL
    path('accounts/register/', views.RegistrationView.as_view(), name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account/login.html', authentication_form=LoginForm), name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/add-address/', views.AddressView.as_view(), name='add-address'),
    path('accounts/remove-address/<int:id>/', views.remove_address, name='remove-address'),
    path('accounts/logout', auth_views.LogoutView.as_view(next_page='store:login'), name='logout'),

    path('accounts/password-change', auth_views.PasswordChangeView.as_view(template_name='account/password_change.html', form_class=PasswordChangeForm, success_url='/accounts/password-change-done/'), name='password-change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password-change-done'),

    path('accounts/password-reset', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html', form_class=PasswordResetForm, success_url='/accounts/password-reset-done/'), name='password-reset'),
    path('accounts/password-reset-done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_reset_done.html'), name='password-reset-done'),
    path('account/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html', form_class=SetPasswordForm, success_url='/accounts/password-reset-complete'), name='password-reset-confirm'),
    path('account/password-reset-complete', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html')),
]