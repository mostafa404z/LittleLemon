from django.shortcuts import render ,redirect
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.authtoken.models import Token
from .models import Menu ,Booking
from .serializers import MenuItemSerializer , BookingSerializer
from django.contrib.auth.models import User , Group 
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
# Create your views here. 
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token



# afetr running server open "http://127.0.0.1:8000/login" and register then 
# but the user name and password you made 
# the token will appear front of you take it and test in insomnia
#  http://127.0.0.1:8000/menu
#  http://127.0.0.1:8000/bookings open those with token you have


def login(request):
    token_to_show = None  
    
    if request.method == 'POST':
        uname = request.POST.get('username')
        pword = request.POST.get('password')
        
        user = authenticate(username=uname, password=pword)
        
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            token_to_show = token.key 
        else:
            return render(request, 'index.html', {'error': 'Invalid username or password'})
        
    return render(request, 'index.html', {'display_token': token_to_show})

@api_view(['POST' , 'GET'])
@permission_classes([IsAuthenticated])
def MenuItemsView(request):
    if request.method == 'GET':
        items = Menu.objects.all()
        serializer_item = MenuItemSerializer(items, many=True)
        return Response(serializer_item.data)
    if request.method == 'POST':
        serializer_items = MenuItemSerializer(data = request.data)
        serializer_items.is_valid()
        serializer_items.save()
        return Response({"message" : "the new item is added"},serializer_items.data,status.HTTP_201_CREATED)
    
@api_view(['POST' , 'GET'])
@permission_classes([IsAuthenticated])    
def BookingViewSet(request):
    if request.method == 'GET':
        bookings = Booking.objects.all()
        bookings_serializered = BookingSerializer(bookings ,many = True)
        return Response(bookings_serializered.data)
    if request.method == 'POST':
        serializer_items = BookingSerializer(data = request.data)
        serializer_items.is_valid()
        serializer_items.save()
        return Response({"message" : "the new book is added"},serializer_items.data,status.HTTP_201_CREATED)




def create_userview(request):
    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        e_mail = request.POST.get('email')
        user_name = request.POST.get('username')
        passw = request.POST.get('password')

        new_user = User.objects.create_user(
            username = user_name,
            password = passw,
            email = e_mail,
            first_name = firstname
        )
        try :
            costumer_group = Group.objects.get(name = 'Customers')
            new_user.groups.add(costumer_group)
        except Group.DoesNotExist:
            pass
        new_user.save()
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')
    return render(request,'create_account.html')






# @api_view(['POST','GET'])
# def SingleMenuItemView(request):
#     queryset = Menu.objects.all()
#     serializer_class = MenuItemSerializer


