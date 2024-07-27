"""EcommWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from shop import views
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = "Ecomm Web Admin"
admin.site.site_title = "Ecomm Web Admin Portal"
admin.site.index_title = "Welcome to Ecomm Web Researcher Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("shop.urls")),
    path('shop/', include("shop.urls")),
    path('about/', views.about,name="AboutUs"),
    path('contact/', views.contact,name="ContactUs"),
    path('tracker', views.tracker,name="TrackingStatus"),
    path('search/', views.search,name="Search"),
    path('productview/', views.productView,name="TrackingStatus"),
    path('checkout/', views.checkout,name="Checkout"),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)