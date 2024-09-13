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
    path('co/collectionlogin/', views.collectionlogin,name='collectionlogin'),
    path('co/collectionhome/', views.collectionhome,name='collectionhome'),
    path('co/drop/', views.drop,name='drop'),
    path('co/dropotp/<int:pass_exc_id>/', views.dropotp,name='dropotp'),
    path('co/doing/<int:pass_exc_id>/', views.doing,name='doing'),
    path('co/pick/', views.pick,name='pick'),
    path('co/pickotp/<int:pass_exc_id>/', views.pickotp,name='pickotp'),
    path('co/doingpick/<int:pass_exc_id>/', views.doingpick,name='doingpick'),
    path('co/rejectabook/<int:pass_exc_id>/', views.rejectabook,name='rejectabook'),
    path('co/reject/', views.reject,name='reject'),
    path('co/rejectotp/<int:pass_exc_id>/', views.rejectotp,name='rejectotp'),
    path('co/doingreject/<int:pass_exc_id>/', views.doingreject,name='doingreject'),
    path('co/returnotp/<int:pass_exc_id>/', views.returnotp,name='returnotp'),
    path('co/doingreturin/<int:pass_exc_id>/', views.doingreturin,name='doingreturin'),
    path('co/returnotpout/<int:pass_exc_id>/', views.returnotpout,name='returnotpout'),
    path('co/doingreturnout/<int:pass_exc_id>/', views.doingreturnout,name='doingreturnout'),
    
    
    
    
    
    
    
     
    
    
 
    
]
