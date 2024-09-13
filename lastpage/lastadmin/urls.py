"""
URL configuration for lastpage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('ad/lastadminlogin/', views.lastadminlogin,name='lastadminlogin'),
    path('ad/adminhome/', views.adminhome,name='adminhome'),
    path('ad/logout_admin/', views.logout_admin,name='logout_admin'),
    path('ad/addpick/', views.addpick,name='addpick'),
    path('ad/editpick/<int:coll_id>/', views.editpick,name='editpick'),
    path('ad/reportv/', views.reportv,name='reportv'),
    path('ad/reportconfirm/<int:report_id>/', views.reportconfirm,name='reportconfirm'),
    path('ad/reportignore/<int:report_id>/', views.reportignore,name='reportignore'),
    path('ad/reportdelete/<int:report_id>/', views.reportdelete,name='reportdelete'),
    path('ad/acceptpayents/', views.acceptpayents,name='acceptpayents'),
    path('ad/Rejectpay/<int:pay_id>/', views.Rejectpay,name='Rejectpay'),
    path('ad/Acceptpay/<int:pay_id>/', views.Acceptpay,name='Acceptpay'),
    path('ad/suggestv/', views.suggestv,name='suggestv'),
    path('ad/suggestview/<int:sugg_id>/', views.suggestview,name='suggestview'),
    path('ad/offer/', views.offer,name='offer'),  
]
