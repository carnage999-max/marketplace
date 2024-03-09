from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.log_in, name="login"),
    path('signup/', views.signup, name="register"),
    path('logout/', views.log_out, name="logout"),
    path('user/<str:username>/', views.UserProfile, name='profile'),
    path('update-profile/<str:username>/', views.updateProfile, name='update'),
    path('add-product/', views.AddProduct, name='addproduct'),
    path('delete/<int:pk>', views.deleteAd, name='delete'),
    path('change_password/', views.change_password, name='change_password'),
    path('confirm-delete/<int:pk>', views.confirmDelete, name='confirm-delete'),
    path('view-product/<int:pk>/', views.productDescription, name='desc'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='addtocart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cancel-order/<int:pk>/', views.cancelOrder, name='cancel'),
    path('category/<str:category>/', views.categoryFilter, name='category-filter'),
    path('search/', views.search, name='search'),
    path('faq/', views.faq, name='faq'),
    path('contact-us/', views.contact, name='contact'),
    path('terms-and-conditions/', views.terms, name='terms'),
    path('about-us/', views.about, name='about'),
    path('privacy-policy/', views.privacy, name='privacy'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="main/password_reset.html"), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="main/password_reset_done.html"), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="main/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="main/password_reset_complete.html"), name='password_reset_complete'),
    path('report-issue/', views.reportIssue, name='report'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
