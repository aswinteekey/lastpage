import base64
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import  login
from django.db import connection
from django.contrib.auth.models import User
from django.utils import timezone
import random
from django.http import JsonResponse
from .models import pageuser,collect_point,book_table,exchange_table,report_table,suggest_table,payment_table,offer_table
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.core.mail import send_mail
from django.db.models import Q
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image 



# Login -----------------------------------------------------------------------------------------------------------
def indexpage(request):
    if request.session.get('user_email'):
            return redirect('home')
    if request.method == 'POST':
        mail_id = request.POST.get('form_mail').lower()
        password = request.POST.get('form_password')
        try:
            user = pageuser.objects.get(mail_id=mail_id)            
        except pageuser.DoesNotExist:
            return render(request, 'index.html', {'error': 'Invalid email or password.'})
        if (password==user.password):
            request.session['user_email'] = user.mail_id
            return redirect('home')
        else:
            return render(request, 'index.html', {'error': 'Invalid email or password.'})
    return render(request, 'index.html')

# Signup ------------------------------------------------------------------------------------------------------------
def signup(request):
    if request.method == 'POST':
        view_name = request.POST['form_name']
        view_mail = request.POST['form_mail'].lower()
        view_mob = request.POST['form_mob']
        view_fav_cat = request.POST['form_fav_cat']
        view_password = request.POST['form_password']

        # Check if user with the same email already exists
        if pageuser.objects.filter(mail_id=view_mail).exists():
            return render(request, 'signup.html', {'error_message': 'Email address is already in use.'})
        

        # Create the database object
        db_obj = pageuser(mail_id=view_mail,password=view_password,user_name=view_name,
                          mob=view_mob,fav_category=view_fav_cat)
        db_obj.save()
        return redirect('indexpage')
    return render (request,'signup.html')
#---- create new -------------------------------------------------------------------------------------------
def createnew(request):
    pageuser_instance = pageuser.objects.get(mail_id=request.session.get('user_email'))
    if pageuser_instance.verify != "Verified":
        return redirect('verify')
    data=collect_point.objects.all()
    if request.method == 'POST':
        view_title = request.POST['form_title']
        view_author = request.POST['form_author']
        view_review = request.POST['form_review']
        view_mrp_str = request.POST.get('form_mrp', '0')  # Default value of '0' if 'form_mrp' is not present
        # Convert the string value to a Decimal or float
        view_mrp = Decimal(view_mrp_str) if view_mrp_str else 0  # Assuming 'Decimal' is imported from 'decimal' module
        # Calculate 10% of the 'view_mrp'
        ten_percent = view_mrp * Decimal('0.1')
        # Round the result to the nearest integer
        view_coin = round(ten_percent)
        view_coll_id = request.POST['form_coll_id']
        collect_point_instance = collect_point.objects.get(coll_id=view_coll_id)
        
        if 'form_image' in request.FILES:
            image_file = request.FILES['form_image']
            if image_file.content_type not in ['image/jpeg', 'image/png']:
                return render(request,'createnew.html',{'key':data,'error': 'Only JPEG and PNG images are allowed.'})

        view_image = request.FILES['form_image']
        view_cat = request.POST['form_cat']

        if 'form_pic1' in request.FILES:
            image_file = request.FILES['form_pic1']
            if image_file.content_type not in ['image/jpeg', 'image/png']:
                return render(request,'createnew.html',{'key':data,'error': 'Only JPEG and PNG images are allowed.'})
        if 'form_pic2' in request.FILES:
            image_file = request.FILES['form_pic2']
            if image_file.content_type not in ['image/jpeg', 'image/png']:
                return render(request,'createnew.html',{'key':data,'error': 'Only JPEG and PNG images are allowed.'})

        view_pic1 = request.FILES['form_pic1']
        view_pic2 = request.FILES['form_pic2']
        view_user = request.session.get('user_email')

        pageuser_instance = pageuser.objects.get(mail_id=view_user)
        db_obj = book_table(title=view_title,author=view_author,review=view_review,
                            mrp=view_mrp,coin=view_coin,c_point=collect_point_instance,category=view_cat,
                            image=view_image,f_pic=view_pic1,b_pic=view_pic2,user=pageuser_instance,
                            update_time = timezone.now())
        db_obj.save()
        return redirect('profile')
    return render(request,'createnew.html',{'key':data})
#---profile-------------------------------------------------
def profile(request):
    view_user=request.session.get('user_email')
    dataprofile = pageuser.objects.get(mail_id=view_user)
    databook = book_table.objects.filter(user=dataprofile) 

    book_loc = []
    for book in reversed(databook):
        coll_pname_get = book.c_point.coll_pname
        book_loc.append((book, coll_pname_get))

    return render(request, 'profile.html',{'keyprofile':dataprofile,'keycoll': book_loc})
#------------home------------------------
def home(request):
    view_user=request.session.get('user_email')
    dataprofile = pageuser.objects.get(mail_id=view_user)
    databook = book_table.objects.exclude(user=dataprofile).exclude(state='Disable')
    disable_button = exchange_table.objects.filter(user=dataprofile).values_list('book_id', flat=True)
    disable_report = report_table.objects.filter(user=dataprofile).values_list('book_id', flat=True)


    book_all=[]
    for book in reversed(databook):
        person_get = book.user.user_name
        pickup_get = book.c_point.coll_pname
        book_all.append((book, person_get,pickup_get))

    if request.method == 'POST':
         if 'current_book_id' in request.POST:
             view_book_id = request.POST.get('current_book_id')
             book_instance = book_table.objects.get(book_id=view_book_id)
             pageuser_instance = pageuser.objects.get(mail_id=view_user)
             if pageuser_instance.verify != "Verified":
                 return redirect('verify')
             if book_instance.coin <= pageuser_instance.coin:
                 db_obj = exchange_table(user=pageuser_instance,book=book_instance,req_time=timezone.now())
                 db_obj.save()      
                 exchange_instance = exchange_table.objects.filter(user=pageuser_instance,book=book_instance).first()
                 pass_exc_id = exchange_instance.exc_id
                 return redirect('bookwait',pass_exc_id=pass_exc_id)
             else:
                 return redirect('coincheck')
         else:
             search_term = request.POST.get('form_search')
             databook = book_table.objects.exclude(user=dataprofile).exclude(state='Disable').filter(Q(title__icontains=search_term) | Q(author__icontains=search_term))
             book_all=[]
             for book in reversed(databook):
                 person_get = book.user.user_name
                 pickup_get = book.c_point.coll_pname
                 book_all.append((book, person_get,pickup_get))
             return render (request,'home.html',{'keybook':book_all,'disable':disable_button,'disablereport':disable_report,'check': "True"})
    return render (request,'home.html',{'keybook':book_all,'disable':disable_button,'disablereport':disable_report})

def coincheck(request):
    return render (request,'coincheck.html')

#...edit profile-----------------------------------------------
def editprofile(request):
    view_user=request.session.get('user_email')
    user = pageuser.objects.get(mail_id=view_user)
    dataprofile = pageuser.objects.get(mail_id=view_user)
    if request.method == 'POST':
        view_name = request.POST.get('form_name')
        view_mob = request.POST.get('form_mob')
        view_PW = request.POST.get('form_PW')
        view_user = request.session.get('user_email')
        if user.password == view_PW:
            user.user_name = view_name
            user.mob = view_mob
            user.save()
        else:
            message = "Incorrect password. Profile not updated."
            return render(request, 'editprofile.html',{'username': dataprofile.user_name, 'mob': dataprofile.mob,'message': message})
        return redirect('profile')
    return render(request, 'editprofile.html', {'username': dataprofile.user_name, 'mob': dataprofile.mob})
#---change pw ---------------------------------------------------------------------------------
def changepw(request):
    if request.method == 'POST':
        view_password = request.POST.get('form_password')
        view_PW = request.POST.get('form_PW')
        view_user=request.session.get('user_email')
        user = pageuser.objects.get(mail_id=view_user)
        if user.password == view_PW:
            user.password = view_password
            user.save()
        else:
            message = "Incorrect password. New password not updated."
            return render(request, 'changepw.html',{'message': message})
        return redirect('profile')
    return render (request,'changepw.html')


def about(request):
    return render (request,'about.html')

# Home

def request(request):
    view_user=request.session.get('user_email')
    send_details = exchange_table.objects.filter(user=view_user).order_by('-exc_id')
    receive_details = exchange_table.objects.filter(book__user=view_user).order_by('-exc_id')
    return render(request,'request.html',{"send":send_details,"receive":receive_details})
def dashboard(request):
    view_user=request.session.get('user_email')
    read = exchange_table.objects.filter(user=view_user).exclude(ret_out_time__isnull=True).count()
    share = exchange_table.objects.filter(book__user=view_user).exclude(out_time__isnull=True).count()
    coin = get_object_or_404(pageuser,mail_id=view_user).coin
    reject = exchange_table.objects.filter(book__user=view_user).exclude(rej_in_time__isnull=True).count()
    report = report_table.objects.filter(user=view_user).count()
    post = book_table.objects.filter(user=view_user).count()
    return render (request,'dashboard.html',{'read':read,'share':share,'coin':coin,'reject':reject,
                                             'report':report,'post':post})
def bookwait(request,pass_exc_id):
    req = get_object_or_404(exchange_table,exc_id=pass_exc_id)
    return render (request,'bookwait.html',{'req_details': req})
def bookaccept(request,pass_exc_id):
    req = get_object_or_404(exchange_table,exc_id=pass_exc_id)
    if request.method == 'POST':
         req.acc_time = timezone.now()
         six_digit_number = random.randint(100000, 999999)
         req.otp = six_digit_number
         req.save()  
         return redirect('bookaccept',pass_exc_id=pass_exc_id)
    return render (request,'bookaccept.html',{'req_details': req})
def bookreject(request,pass_exc_id):
    if request.method == 'POST':
        req = get_object_or_404(exchange_table,exc_id=pass_exc_id)
        req.rej_time = timezone.now()
        req.save()  
        return redirect('bookaccept',pass_exc_id=pass_exc_id)
    return render (request,'bookreject.html')
def deletereq(request,pass_exc_id):
    if request.method == 'POST':
        req = get_object_or_404(exchange_table,exc_id=pass_exc_id)
        req.delete()
        return redirect('request')
    return render (request,'deletereq.html')


# Profile
def editpost(request,slug):
    book = get_object_or_404(book_table, slug=slug)
    data=collect_point.objects.all()
    if request.method == 'POST':
        book.title = request.POST['form_title']
        book.author = request.POST['form_author']
        book.review = request.POST['form_review']
        view_mrp_str = request.POST.get('form_mrp', '0')  # Default value of '0' if 'form_mrp' is not present
        # Convert the string value to a Decimal or float
        temp = Decimal(view_mrp_str) if view_mrp_str else 0  # Assuming 'Decimal' is imported from 'decimal' module
        # Calculate 10% of the 'view_mrp'
        book.mrp = temp
        ten_percent = temp * Decimal('0.1')
        # Round the result to the nearest integer
        book.coin = round(ten_percent)
        view_coll_id = request.POST['form_coll_id']
        book.c_point = collect_point.objects.get(coll_id=view_coll_id)
        book.category = request.POST['form_cat']
        if 'form_pic1' in request.FILES:
            image_file = request.FILES['form_pic1']
            if image_file.content_type not in ['image/jpeg', 'image/png']:
                return render(request, 'editpost.html', {'book': book,'coll':data,'error': 'Only JPEG and PNG images are allowed.'})
            book.f_pic = request.FILES['form_pic1']
        if 'form_pic2' in request.FILES:
            image_file = request.FILES['form_pic2']
            if image_file.content_type not in ['image/jpeg', 'image/png']:
                return render(request, 'editpost.html', {'book': book,'coll':data,'error': 'Only JPEG and PNG images are allowed.'})
            book.b_pic = request.FILES['form_pic2']

        view_user = request.session.get('user_email')
        book.user = pageuser.objects.get(mail_id=view_user)
        book.update_time = timezone.now()
        book.save()
        return redirect('profile')
    return render(request, 'editpost.html', {'book': book,'coll':data})

def deletepost(request,slug):
    if request.method == 'POST':
        post = get_object_or_404(book_table, slug=slug)
        post.delete()
        return redirect('profile')
    return render (request,'deletepost.html')

# Request
def booktake(request):
    return render (request,'booktake.html')

def bookback(request):
    return render (request,'bookback.html')
def booktrans(request):
    return render (request,'booktrans.html')

# Dashboard
def sugggen(request):
    if request.method == 'POST':
        view_topic = request.POST['form_topic']
        view_desc = request.POST['form_desc']
        db_obj = suggest_table(type="Genaral",topic=view_topic,desc=view_desc,
                              user=pageuser.objects.get(mail_id=request.session.get('user_email')))
        db_obj.save()
        return redirect('dashboard')
    return render (request,'sugggen.html')
def suggpick(request):
    if request.method == 'POST':
        view_topic = request.POST['form_topic']
        view_desc = request.POST['form_desc']
        db_obj = suggest_table(type="Location",topic=view_topic,desc=view_desc,
                              user=pageuser.objects.get(mail_id=request.session.get('user_email')))
        db_obj.save()
        return redirect('dashboard')
    return render (request,'suggpick.html')
def buycoin(request):
    mail=request.session.get('user_email')
    pageuser_instance = pageuser.objects.get(mail_id=mail)
    if pageuser_instance.verify != "Verified":
        return redirect('verify')
    if request.method == 'POST':
        redirect_url = reverse('dashboard')
        view_user=request.session.get('user_email')
        dataprofile = pageuser.objects.get(mail_id=view_user)
        view_code = request.POST['red_form_code'].lower()
        req = get_object_or_404(offer_table,id=1)
        target_value = req.code
        if view_code == target_value and dataprofile.offer != req.code:
            dataprofile.offer=req.code
            dataprofile.coin += req.coin
            dataprofile.save()
            json_data = {'success': True, 'redirect_url': redirect_url}
            return JsonResponse(json_data)
        else:
            json_data = {'success': False}
            return JsonResponse(json_data)
    return render (request,'buycoin.html')
def gateway50(request):
    if request.method == 'POST':
        view_user=request.session.get('user_email')
        view_upi = request.POST['upi_form']
        db_obj = payment_table(upi_id=view_upi,user=pageuser.objects.get(mail_id=view_user),
                            time = timezone.now(),amt=50)
        db_obj.save()
        return redirect('dashboard')
    return render (request, 'gateway.html', {'key': 'img/scan50.png'})
def gateway100(request):
    if request.method == 'POST':
        view_user=request.session.get('user_email')
        view_upi = request.POST['upi_form']
        db_obj = payment_table(upi_id=view_upi,user=pageuser.objects.get(mail_id=view_user),
                            time = timezone.now(),amt=100)
        db_obj.save()
        return redirect('dashboard')
    return render (request, 'gateway.html', {'key': 'img/scan100.png'})
def gateway200(request):
    if request.method == 'POST':
        view_user=request.session.get('user_email')
        view_upi = request.POST['upi_form']
        db_obj = payment_table(upi_id=view_upi,user=pageuser.objects.get(mail_id=view_user),
                            time = timezone.now(),amt=200)
        db_obj.save()
        return redirect('dashboard')
    return render (request, 'gateway.html', {'key': 'img/scan200.png'})


def logout_view(request):
    # Clear session data
    view_user=request.session.get('user_email')
    request.session.pop('user_email')   
    # Redirect to a different page after logout
    return redirect('indexpage')


def noteuser(request,pass_exc_id):
    note = get_object_or_404(exchange_table, exc_id=pass_exc_id)
    user_note=note.user_note
    if request.method == 'POST':
        note.user_note=request.POST['form_update']
        note.save()
        return redirect('bookwait',pass_exc_id=pass_exc_id)
    return render(request, 'note.html', {'key': user_note})

def notebookuser(request,pass_exc_id):
    note = get_object_or_404(exchange_table, exc_id=pass_exc_id)
    user_note=note.book_user_note
    if request.method == 'POST':
        note.book_user_note=request.POST['form_update']
        note.save()
        return redirect('bookaccept',pass_exc_id=pass_exc_id)
    return render(request, 'note.html', {'key': user_note})

def requestvia(request,book_id):
    res= get_object_or_404(exchange_table, book_id=book_id,user_id=request.session.get('user_email'))
    pass_exc_id=res.exc_id
    return redirect('bookwait',pass_exc_id=pass_exc_id)
def report(request,book_id):
    if request.method == 'POST':
        view_reason = request.POST['form_reason']
        view_note = request.POST['form_note']
        db_obj = report_table(reason=view_reason,note=view_note,book=book_table.objects.get(book_id=book_id),
                              user=pageuser.objects.get(mail_id=request.session.get('user_email')))
        db_obj.save()
        return redirect('home')
    return render (request,'report.html')

def forgotpw(request):
    if request.method == 'POST':
        mail_id = request.POST.get('form_mail').lower()
        try:
            user = pageuser.objects.get(mail_id=mail_id)   
            recipient_email = user.mail_id
            sender_email = 'lastpageproject2024@gmail.com'
            subject = 'Lastpage password'
            message_body = f"Your password is: {user.password}\n\nFor security reasons, we recommend changing your password after logging in to your account. You can do this by navigating to the 'Profile' section of our website.\n\n If you did not request this password change or have any concerns about the security of your account, please contact our support team immediately.\n\nTeam Lastpage\nShare Stories, Exchange Worlds !"
            send_mail(subject, message_body, sender_email, [recipient_email])
            return redirect('indexpage')      
        except pageuser.DoesNotExist:
            return render(request, 'forgotpw.html', {'error': 'Invalid email.please enter mail id which you use while sign up.'})
    return render (request,'forgotpw.html')

def verify(request):
    mail=request.session.get('user_email')
    if request.method == 'POST':
        user = pageuser.objects.get(mail_id=mail)   
        six_digit_number = random.randint(100000, 999999)
        user.otp = six_digit_number
        user.save() 
        recipient_email = user.mail_id
        sender_email = 'lastpageproject2024@gmail.com'
        subject = 'Lastpage email verification'
        message_body = f"Your verification code is: {user.otp}\n\nIf you did not request this verification code or have any concerns about the security of your account, please contact our support team immediately.\n\nTeam Lastpage\nShare Stories, Exchange Worlds !"
        send_mail(subject, message_body, sender_email, [recipient_email])
        return redirect('verifyotp')
    return render (request,'verify.html',{'mail': mail})

def verifyotp(request):
    mail=request.session.get('user_email')
    if request.method == 'POST':
        try:
            view_otp=request.POST['form_otp']
            user = pageuser.objects.get(mail_id=mail)
            if (user.otp==int(view_otp)):
                user.verify="Verified"
                user.save()
                return redirect('profile')
            else:
                return render(request, 'verifyotp.html', {'error': 'Invalid verification code'})
        except:
            return render(request, 'verifyotp.html', {'error': 'Invalid verification code'})
    return render (request,'verifyotp.html',{'mail': mail})