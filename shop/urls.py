from django.urls import path,re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path('',views.home, name="home"),
    path('register',views.register, name="register"),
    path('login',views.login_page, name="login"),
    path('logout',views.logout_page, name="logout"),
    path('cart',views.cart_page, name="cart"),
    path('fav',views.fav_page, name="fav"),
    path('checkout_page',views.checkout_page, name="checkout_page"), 
    path('fav_view_page',views.fav_view_page, name="fav_view_page"),
    path('remove_cart/<str:cid>',views.remove_cart, name="remove_cart"),
    path('remove_fav/<str:fid>',views.remove_fav, name="remove_fav"),
    path('Collections',views.Collections, name="Collections"),
    path('Collections/<str:name>',views.Collectionsview, name="Collections"),
    path('Collections/<str:cname>/<str:pname>',views.ProductDetails, name="Product_details"),
    path('addtocart',views.add_to_cart, name="addtocart"),
    path('create_checkout_session', views.create_checkout_session, name='checkout'),
    path('success', views.success,name='success'),
    path('cancel', views.cancel,name='cancel'),
    path('webhooks/stripe/',views.webhook,name="webhook")
    
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
