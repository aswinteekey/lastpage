from django.db import models
from django.utils.text import slugify
import uuid
import random
import string


# Create your models here.
class pageuser(models.Model):
    mail_id=models.CharField(max_length=30,primary_key=True)
    password=models.CharField(max_length=20)
    user_name=models.TextField(max_length=20)
    mob=models.CharField(max_length=13,null=True)
    fav_category=models.TextField(max_length=10)
    offer=models.TextField(default='None')
    coin = models.IntegerField(default=2)
    verify=models.TextField(default='None')
    otp = models.IntegerField(null=True, blank=True)

class pageadmin(models.Model):
    mail_id=models.CharField(max_length=30,primary_key=True)
    password=models.CharField(max_length=20)

class collect_point(models.Model):
    coll_id = models.BigAutoField(primary_key=True)
    coll_pname=models.TextField(max_length=30)
    coll_plink=models.TextField()
    coll_pw = models.IntegerField(null=True, blank=True)

class book_table(models.Model):
    book_id = models.BigAutoField(primary_key=True)
    title=models.CharField(max_length=40)
    author=models.TextField(max_length=20)
    review=models.TextField()
    mrp = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    coin = models.IntegerField(null=True, blank=True)
    c_point=models.ForeignKey(collect_point,on_delete=models.CASCADE)
    category=models.TextField(max_length=20)
    image=models.ImageField(upload_to='images/',null=True)
    f_pic=models.ImageField(upload_to='images/',null=True)
    b_pic=models.ImageField(upload_to='images/',null=True)
    user=models.ForeignKey(pageuser,on_delete=models.CASCADE)
    update_time = models.DateTimeField(null=True, blank=True)
    state=models.TextField(default='Active')

    slug = models.SlugField(unique=True, blank=True)  # Add blank=True
    
    def _generate_random_slug(self):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.book_id)
            base_slug = f"{self._generate_random_slug()}{base_slug}{self._generate_random_slug()}"
            unique_slug = base_slug
            while book_table.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{self._generate_random_slug()}"
            self.slug = unique_slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class exchange_table(models.Model):
    exc_id = models.BigAutoField(primary_key=True)
    user=models.ForeignKey(pageuser,on_delete=models.CASCADE)
    book=models.ForeignKey(book_table,on_delete=models.CASCADE)
    req_time = models.DateTimeField(null=True, blank=True)
    acc_time = models.DateTimeField(null=True, blank=True)
    rej_time = models.DateTimeField(null=True, blank=True)
    in_time = models.DateTimeField(null=True, blank=True)
    out_time = models.DateTimeField(null=True, blank=True)
    ret_in_time = models.DateTimeField(null=True, blank=True)
    ret_out_time = models.DateTimeField(null=True, blank=True)
    rej_in_time = models.DateTimeField(null=True, blank=True)
    rej_out_time = models.DateTimeField(null=True, blank=True)
    otp = models.IntegerField(null=True, blank=True)
    user_note=models.TextField(default='Hey...')
    book_user_note=models.TextField(default='Hey...')

class report_table(models.Model):
    report_id = models.BigAutoField(primary_key=True)
    reason=models.TextField(max_length=30)
    note=models.TextField()
    book=models.ForeignKey(book_table,on_delete=models.CASCADE)
    user=models.ForeignKey(pageuser,on_delete=models.CASCADE)

class suggest_table(models.Model):
    sugg_id = models.BigAutoField(primary_key=True)
    type=models.TextField(max_length=10)
    topic=models.TextField(max_length=30)
    desc=models.TextField()
    user=models.ForeignKey(pageuser,on_delete=models.CASCADE)
    status=models.TextField(default='Pending')
class payment_table(models.Model):
    pay_id = models.BigAutoField(primary_key=True)
    user=models.ForeignKey(pageuser,on_delete=models.CASCADE)
    upi_id=models.CharField(max_length=50)
    time = models.DateTimeField(null=True, blank=True)
    status=models.TextField(default='Pending')
    amt = models.IntegerField(null=True, blank=True)


class offer_table(models.Model):
    code=models.TextField(max_length=10)
    coin = models.IntegerField(null=True, blank=True)      
            
        






