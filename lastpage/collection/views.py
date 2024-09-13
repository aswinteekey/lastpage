import random
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from user.models import pageuser,collect_point,book_table,exchange_table

# Create your views here.
def collectionlogin(request):
    data=collect_point.objects.all()
    if request.method == 'POST':
        view_coll_id = request.POST['form_coll_id']
        password = request.POST.get('form_password')
        c_point = collect_point.objects.get(coll_id=view_coll_id)
        if (c_point.coll_pw==int(password)):
            print(c_point.coll_pname+" logged in --------------------------------------------------")
            request.session['collogin'] = c_point.coll_id
            return redirect('collectionhome')
        else:
            return render(request, 'cindex.html', {'error': 'Invalid collection point or password.','key':data})
    return render (request,'cindex.html',{'key':data})

def collectionhome(request):
    collogin= request.session.get('collogin')
    collogin_instance = collect_point.objects.get(coll_id=collogin)
    return render (request,'chome.html',{'key':collogin_instance})
def drop(request):
    data = exchange_table.objects.filter(book__c_point__coll_id=request.session.get('collogin'), acc_time__isnull=False, in_time__isnull=True)
    data_return = exchange_table.objects.filter(book__c_point__coll_id=request.session.get('collogin'), out_time__isnull=False, ret_in_time__isnull=True)
    return render (request,'drop.html',{'key':data,'key_ret':data_return})
def dropotp(request,pass_exc_id):
    if request.method == 'POST':
        view_otp=request.POST['form_password']
        exc = exchange_table.objects.get(exc_id=pass_exc_id)
        if (exc.otp==int(view_otp)):
            print(str(exc.exc_id)+" otp currect --------------------------------------------------")
            return redirect('doing',pass_exc_id=pass_exc_id)
        else:
            return render(request, 'dropotp.html', {'error': 'Invalid OTP.'})
    return render (request,'dropotp.html')
def doing(request,pass_exc_id):
    if request.method == 'POST':
        req = get_object_or_404(exchange_table,exc_id=pass_exc_id)
        book = get_object_or_404(book_table,book_id=req.book.book_id)
        req.in_time = timezone.now()
        six_digit_number = random.randint(100000, 999999)
        req.otp = six_digit_number
        req.save()  
        book.state='Disable'
        book.save()  
        return redirect('collectionhome')
    return render (request,'doing.html')
def pick(request):
    data = exchange_table.objects.filter(book__c_point__coll_id=request.session.get('collogin'), in_time__isnull=False, out_time__isnull=True,rej_in_time__isnull=True)
    data2 = exchange_table.objects.filter(book__c_point__coll_id=request.session.get('collogin'), ret_in_time__isnull=False, ret_out_time__isnull=True)
    return render (request,'pick.html',{'key':data,'key_ret':data2})
def pickotp(request,pass_exc_id):
    if request.method == 'POST':
        view_otp=request.POST['form_password']
        exc = exchange_table.objects.get(exc_id=pass_exc_id)
        if (exc.otp==int(view_otp)):
            print(str(exc.exc_id)+" otp currect --------------------------------------------------")
            return redirect('doingpick',pass_exc_id=pass_exc_id)
        else:
            return render(request, 'pickotp.html', {'error': 'Invalid OTP.'})
    return render (request,'pickotp.html')
def doingpick(request,pass_exc_id):
    req = get_object_or_404(exchange_table,exc_id=pass_exc_id)
    rec=pageuser.objects.get(mail_id=req.user.mail_id)
    send=pageuser.objects.get(mail_id=req.book.user.mail_id)
    if request.method == 'POST':
        req.out_time = timezone.now()
        six_digit_number = random.randint(100000, 999999)
        req.otp = six_digit_number
        req.save()  
        send.coin += req.book.coin
        send.save()
        rec.coin -= req.book.coin
        rec.save()
        return redirect('collectionhome')
    return render (request,'doingpick.html',{'key':req})
def rejectabook(request,pass_exc_id):
    if request.method == 'POST':
        req = get_object_or_404(exchange_table,exc_id=pass_exc_id)
        req.rej_in_time = timezone.now()
        six_digit_number = random.randint(100000, 999999)
        req.otp = six_digit_number
        req.save()  
        return redirect('collectionhome')
    return render (request,'rejectabook.html')
def reject(request):
    data = exchange_table.objects.filter(book__c_point__coll_id=request.session.get('collogin'),rej_in_time__isnull=False,rej_out_time__isnull=True)
    return render (request,'reject.html',{'key':data})
def rejectotp(request,pass_exc_id):
    if request.method == 'POST':
        view_otp=request.POST['form_password']
        exc = exchange_table.objects.get(exc_id=pass_exc_id)
        if (exc.otp==int(view_otp)):
            return redirect('doingreject',pass_exc_id=pass_exc_id)
        else:
            return render(request, 'rejectotp.html', {'error': 'Invalid OTP.'})
    return render (request,'rejectotp.html')
def doingreject(request,pass_exc_id):
    req = get_object_or_404(exchange_table,exc_id=pass_exc_id)
    if request.method == 'POST':
        req.rej_out_time = timezone.now()
        req.save()  
        return redirect('collectionhome')
    return render (request,'doingreject.html',{'key':req})
def returnotp(request,pass_exc_id):
    if request.method == 'POST':
        view_otp=request.POST['form_password']
        exc = exchange_table.objects.get(exc_id=pass_exc_id)
        if (exc.otp==int(view_otp)):
            return redirect('doingreturin',pass_exc_id=pass_exc_id)
        else:
            return render(request, 'returnotp.html', {'error': 'Invalid OTP.'})
    return render (request,'returnotp.html')
def doingreturin(request,pass_exc_id):
    req = get_object_or_404(exchange_table,exc_id=pass_exc_id)
    if request.method == 'POST':
        req.ret_in_time = timezone.now()
        six_digit_number = random.randint(100000, 999999)
        req.otp = six_digit_number
        req.save()  
        return redirect('collectionhome')
    return render (request,'doingreturin.html')
def returnotpout(request,pass_exc_id):
    if request.method == 'POST':
        view_otp=request.POST['form_password']
        exc = exchange_table.objects.get(exc_id=pass_exc_id)
        if (exc.otp==int(view_otp)):
            return redirect('doingreturnout',pass_exc_id=pass_exc_id)
        else:
            return render(request, 'returnotpout.html', {'error': 'Invalid OTP.'})
    return render (request,'returnotpout.html')
def doingreturnout(request,pass_exc_id):
    req = get_object_or_404(exchange_table,exc_id=pass_exc_id)
    book = get_object_or_404(book_table,book_id=req.book.book_id)
    rec=pageuser.objects.get(mail_id=req.user.mail_id)
    send=pageuser.objects.get(mail_id=req.book.user.mail_id)
    if request.method == 'POST':
        req.ret_out_time = timezone.now()
        req.save()  
        send.coin -= req.book.coin
        send.save()
        rec.coin += req.book.coin
        rec.save()
        book.state='Active'
        book.save() 
        return redirect('collectionhome')
    return render (request,'doingreturnout.html')

