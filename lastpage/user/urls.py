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
    path('', views.indexpage,name='indexpage'),
    path('signup/', views.signup,name='signup'),
    path('about/', views.about,name='about'),
    path('home/', views.home,name='home'),

    path('profile/', views.profile,name='profile'),
    path('request/', views.request,name='request'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('createnew/', views.createnew,name='createnew'),
    path('bookwait/<int:pass_exc_id>/', views.bookwait,name='bookwait'),
    path('deletereq/<int:pass_exc_id>/', views.deletereq,name='deletereq'),
    


    path('editpost/<slug>/', views.editpost, name='editpost'),
    path('deletepost/<slug>/', views.deletepost, name='deletepost'),
    path('editprofile/', views.editprofile,name='editprofile'),
    path('changepw/', views.changepw,name='changepw'),

    path('booktake/', views.booktake,name='booktake'),
    path('bookaccept/<int:pass_exc_id>/', views.bookaccept,name='bookaccept'),
    path('bookreject/<int:pass_exc_id>/', views.bookreject,name='bookreject'),
    path('bookback/', views.bookback,name='bookback'),
    path('booktrans/', views.booktrans,name='booktrans'),

    path('sugggen/', views.sugggen,name='sugggen'),
    path('suggpick/', views.suggpick,name='suggpick'),
    path('buycoin/', views.buycoin,name='buycoin'),
    path('gateway50/', views.gateway50,name='gateway50'),
    path('gateway100/', views.gateway100,name='gateway100'),
    path('gateway200/', views.gateway200,name='gateway200'),
    path('logout/', views.logout_view, name='logout'),
    path('noteuser/<int:pass_exc_id>/', views.noteuser,name='noteuser'),
    path('notebookuser/<int:pass_exc_id>/', views.notebookuser,name='notebookuser'),
    path('requestvia/<int:book_id>/', views.requestvia, name='requestvia'),
    path('report/<int:book_id>/', views.report, name='report'),
    path('coincheck/', views.coincheck,name='coincheck'),
    path('forgotpw/', views.forgotpw,name='forgotpw'),
    path('verify/', views.verify,name='verify'),
    path('verifyotp/', views.verifyotp,name='verifyotp'),
    
]
