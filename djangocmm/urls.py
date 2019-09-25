"""djangocmm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,re_path,include
from django.contrib.auth import views as auth_views

from store_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('product/<int:id>', views.product_detail, name='product_detail'),
    path('',views.product_detail),
    path('search/', views.product_search, name='product_search'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('logout/',auth_views.logout,name='logout'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('my_cart/', views.my_cart, name='my_cart'),
    #path('my_order/', views.my_order, name='my_order'),
    path('delete_order_detail/<int:id>/', views.delete_order_detail, name='delete_order_detail'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
