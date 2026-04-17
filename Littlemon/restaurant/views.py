from django.shortcuts import render ,redirect
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.authtoken.models import Token
from .models import Menu ,Booking ,Categories ,Feedback
from .serializers import MenuItemSerializer , BookingSerializer
from django.contrib.auth.models import User , Group 
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render
from django.db.models import Case, When, Value, IntegerField
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re
from datetime import date
from django.contrib.auth import authenticate, login , logout 


def login_view(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pword = request.POST.get('password')
        
        user = authenticate(request,username=uname, password=pword)
        
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request,"Incorrect username or password")
            return render(request, 'index.html')
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def create_userview(request):
    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        e_mail = request.POST.get('email')
        user_name = request.POST.get('username')
        passw = request.POST.get('password')

        if not all([firstname, e_mail, user_name, passw]):
            messages.error(request, "All fields are required.")
            return render(request, 'create_account.html')

        if User.objects.filter(username = user_name).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'create_account.html')
        
        try:
            validate_password(passw, user=User(username=user_name))
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, 'create_account.html')  

        if User.objects.filter(email = e_mail).exists():
            messages.error(request, "email already exists.")
            return render(request, 'create_account.html')   

        if not re.findall(r'[A-Z]', passw) or not re.findall(r'[0-9]', passw) or not re.findall(r'[^a-zA-Z0-9]', passw):
            messages.error(request, "Password must contain at least one uppercase letter, one number, and one special character.")
            return render(request, 'create_account.html')       

        try:
            new_user = User.objects.create_user(
                username=user_name,
                password=passw,
                email=e_mail,
                first_name=firstname
            )
            
            try:
                customer_group = Group.objects.get(name='Customers')
                new_user.groups.add(customer_group)
            except Group.DoesNotExist:
                pass
            
            new_user.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
    return render(request,'create_account.html')


def home(request):
    return render(request, 'home_page.html')

def about(request):
    if request.method == 'POST':
        # التأكد أولاً أن المستخدم سجل دخوله
        if request.user.is_authenticated:
            # سحب البيانات من الفورم الـ HTML العادي الخاص بك
            name = request.POST.get('name')
            email = request.POST.get('email')
            m_type = request.POST.get('message_type')
            message = request.POST.get('message')

            # إنشاء السجل وربطه بـ request.user تلقائياً
            Feedback.objects.create(
                user=request.user, # هنا نأخذ المستخدم الذي سجل الدخول
                name=name,
                email=email,
                message_type=m_type,
                message=message
            )
            messages.success(request,"thank you for your message.")
            return redirect('about')
            
    return render(request, 'about.html')

def reservations(request):
    if request.user.groups.filter(name='Manager').exists():
        now = timezone.now()
        bookings = Booking.objects.annotate(
            is_expired_sort=Case(
                When(booking_date__lt=now.date(), then=Value(1)),
                When(booking_date=now.date(), booking_time__lt=now.hour, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by('is_expired_sort', 'booking_date', 'booking_time')
        return render(request, 'bookings.html',{"bookings":bookings})
    
    bookings = Booking.objects.filter(user = request.user).order_by('id')
    return render(request, 'bookings.html',{"bookings":bookings})

def book(request): 
    # form = BookingForm()
    if request.method == 'POST':
        name = request.POST.get("name")
        number_of_guest = int(request.POST.get("n_o_guset"))
        res_date = request.POST.get("res_date")
        slot = request.POST.get("reservation_slot")     

        if res_date < str(date.today()):
            messages.error(request,"Please choose a valid date (today or in the future).")
            return render(request,"book.html")
        
        day_bookings = Booking.objects.filter(booking_date = res_date)
        if day_bookings.exists():
            guests_perday = day_bookings.aggregate(Sum('no_of_guest'))['no_of_guest__sum'] or 0
            if number_of_guest + guests_perday > 50:
                messages.error(request,"sorry! restaurant is full this day.")
                return render(request,"book.html")
            
        try:
            Booking.objects.create(
                name = name,
                no_of_guest = number_of_guest,
                booking_date = res_date,
                booking_time = slot,
                user = request.user
            )
            messages.success(request,"Your booking has been successfully confirmed!")
            return redirect("reservations")
        
        except Exception as e:
            messages.error(request,f"system error! {e}")

    return render(request, 'book.html')

def menu(request):
    all_categories = Categories.objects.all() 
    selected_category = request.GET.get('category')
    
    if selected_category:
        menu_items = Menu.objects.filter(category__name=selected_category)
    else:
        menu_items = Menu.objects.all()
        
    return render(request, 'menu.html', {
        'menu_items': menu_items,
        'categories': all_categories,
        'selected_category': selected_category
      })  







