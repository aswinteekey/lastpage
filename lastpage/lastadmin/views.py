from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import  login
from django.db import connection
from django.contrib.auth.models import User
from django.utils import timezone
import random
from django.http import JsonResponse
from user.models import pageuser,collect_point,book_table,exchange_table,report_table,suggest_table,payment_table,pageadmin,offer_table
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.core.mail import send_mail
from django.db.models import Q





# Create your views here.
def lastadminlogin(request):
    if request.session.get('admin_email'):
            return redirect('adminhome')
    if request.method == 'POST':
        mail_id = request.POST.get('form_mail').lower()
        password = request.POST.get('form_password')
        try:
            admin = pageadmin.objects.get(mail_id=mail_id)            
        except pageadmin.DoesNotExist:
            return render(request, 'lastadminlogin.html', {'error': 'Invalid username or password'})
        if (password==admin.password):
            print(admin.mail_id+" logged in --------------------------------------------------")
            request.session['admin_email'] = admin.mail_id
            return redirect('adminhome')
        else:
            return render(request, 'lastadminlogin.html', {'error': 'Invalid username or password'})
    return render(request, 'lastadminlogin.html')

def logout_admin(request):
    # Clear session data
    view_admin=request.session.get('admin_email')
    print(view_admin+" logged out !  --------------------------------------------------")
    request.session.pop('admin_email')
    # Redirect to a different page after logout
    return redirect('lastadminlogin')

def adminhome(request):
    if not request.session.get('admin_email'):
        return redirect('lastadminlogin')
    report = report_table.objects.all().count()
    payment = payment_table.objects.filter(status="Pending").count()
    suggest = suggest_table.objects.filter(status="Pending").count()
    return render(request, 'adminhome.html',{'report':report,'payment':payment,'suggest':suggest})

def addpick(request):
    if not request.session.get('admin_email'):
        return redirect('lastadminlogin')
    collectionpoint=collect_point.objects.all()
    if request.method == 'POST':
        view_col_name = request.POST.get('form_col_name')
        view_col_link = request.POST.get('form_col_link')
        db_obj = collect_point(coll_pname=view_col_name,coll_plink=view_col_link,coll_pw=random.randint(100000, 999999))
        db_obj.save()
        return redirect('addpick')
    return render(request, 'addpick.html',{'key':collectionpoint})

def editpick(request,coll_id):
    if not request.session.get('admin_email'):
        return redirect('lastadminlogin')
    edit_details = collect_point.objects.get(coll_id=coll_id)
    if request.method == 'POST':
        view_col_name = request.POST.get('form_col_name')
        view_col_link = request.POST.get('form_col_link')
        edit_details.coll_pname=view_col_name
        edit_details.coll_plink=view_col_link
        edit_details.save()
        return redirect('addpick')
    return render(request, 'editpick.html',{'edit':edit_details})

def deletepick(request,coll_id):
    if not request.session.get('admin_email'):
        return redirect('lastadminlogin')
    delete_details = collect_point.objects.get(coll_id=coll_id)
    if request.method == 'POST':
        return redirect('addpick')
    return render(request, 'deletepick.html',{'edit':delete_details})

def reportv(request):
    if not request.session.get('admin_email'):
        return redirect('lastadminlogin')
    report=report_table.objects.all()
    return render(request, 'reportv.html',{'report':report})

def reportconfirm(request,report_id):
    if not request.session.get('admin_email'):
        return redirect('lastadminlogin')
    report_details = report_table.objects.get(report_id=report_id)
    return render(request, 'reportconfirm.html',{'report':report_details})

def reportignore(request,report_id):
    rep_req = get_object_or_404(report_table,report_id=report_id)
    rep_req.delete()
    return redirect('reportv')

def reportdelete(request,report_id):
    rep_req = get_object_or_404(report_table,report_id=report_id)
    book_req = get_object_or_404(book_table,book_id=rep_req.book.book_id)
    rep_req.delete()
    book_req.delete()
    return redirect('reportv') 

def acceptpayents(request):
    if not request.session.get('admin_email'):
        return redirect('lastadminlogin')
    pending = payment_table.objects.all().order_by('-pay_id')
    return render(request, 'acceptpayents.html',{'pending':pending})

def Acceptpay(request,pay_id):
    req = get_object_or_404(payment_table,pay_id=pay_id)
    req.status="Accepted"
    req.save()
    coin_req = get_object_or_404(pageuser,mail_id=req.user.mail_id)
    coin_req.coin += req.amt
    coin_req.save()
    return redirect('acceptpayents') 
def Rejectpay(request,pay_id):
    req = get_object_or_404(payment_table,pay_id=pay_id)
    req.status="Rejected"
    req.save()
    return redirect('acceptpayents') 

def suggestv(request):
    if not request.session.get('admin_email'):
        return redirect('lastadminlogin')
    sugg = suggest_table.objects.all().order_by('-sugg_id')
    return render(request, 'suggestv.html',{'key':sugg})

def suggestview(request,sugg_id):
    if not request.session.get('admin_email'):
        return redirect('lastadminlogin')
    req = get_object_or_404(suggest_table,sugg_id=sugg_id)
    req.status="Viewed"
    req.save()
    return render(request, 'suggestview.html',{'key':req})

def offer(request):
    if not request.session.get('admin_email'):
        return redirect('lastadminlogin')
    req = get_object_or_404(offer_table,id=1)
    if request.method == 'POST':
        code = request.POST.get('form_code').lower()
        coin = request.POST.get('form_coin')
        req.code=code
        req.coin=coin
        req.save()
        return redirect('adminhome')
    return render(request,'offer.html',{'key':req})