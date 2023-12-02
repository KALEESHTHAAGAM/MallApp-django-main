from http.client import responses
from urllib import response
from django import views
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from payment.models import donar_data
from rest_framework import generics
from .serializers import DonationSerializer
from .models import CollectionData, UserProfile
from django.db.models import Sum
from payment.models import Donation
from django.views import View
from payment.models import CollectionData 
from .models import donar_data
from datetime import datetime
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from djongo import models
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import UserProfileModel
from .serializers import UserProfileSerializer
from rest_framework.decorators import api_view, permission_classes,authentication_classes ,renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.admin.models import LogEntry
from django.middleware.csrf import get_token
from rest_framework.authentication import SessionAuthentication
from .models import UserProfile
from .serializers import UserProfileSerializer
from .models import donar_data
from django.contrib.auth import authenticate, login







 ############################### LOGIN AUTHENTICATION ################################################################
@csrf_exempt
def handle_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        print(f"username: {username}, Password: {password}")

        # Use the email as the username for authentication
        UserProfile = authenticate(request, username=username, password=password)
        print(f"Authenticated User: {UserProfile}")

        if UserProfile is not None:
            # Authentication successful
            login(request, UserProfile)  # Log in the user
            print(f"User {UserProfile.email} has logged in.")
            request.session['user_profile'] = UserProfile.username
            # You can also access other user data, such as username
            print(f"Username: {UserProfile.username}")
            return JsonResponse({'success': True})

    # Return an error response outside of the 'if request.method == 'POST':' block
    return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)
######################################################################################################################

# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def create_razorpay_order(request):
    client = razorpay.Client(auth=("rzp_test_2h8n68Dp5BnsgZ", "RadEymMn08SuR4yGSXsvp4qJ"))
   

    response = client.order.create({
        "amount": '200',
        "currency": "INR",
        "receipt": "receipt#1",
        "notes": {
            "key1": "value3",
            "key2": "value2"
        }
    })
    
    return JsonResponse(response)
#########################################################################################################################
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                Amount = 10000  # Rs. 200
                try:
                    razorpay_client.payment.capture(payment_id, Amount)
                    return JsonResponse({'status': 'success'})
                except:
                    return JsonResponse({'status': 'failure'})
            else:
                return JsonResponse({'status': 'failure'})
        except:
            return JsonResponse({'status': 'failure'})
    else:
        return JsonResponse({'status': 'failure'})

    
def process_payment_api(request):
    if request.method == 'POST':
        # Extract the data from the POST request
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        # Process the payment data here
        # ...

        # Return a JSON response to the React Native app
        return JsonResponse({'message': 'Payment processed successfully'})

    return JsonResponse({'message': 'Invalid request method'}, status=400)
#######################################  handle data ##########################################################
#handle data data save process
@csrf_exempt
def handle_data(request):
 if request.method == 'POST':
    try:
        data = json.loads(request.body)
        print (f"Received data: {data}")
        donardetails = donar_data.objects.create(name=data['name'],
                                             nameOnParcel = data['nameOnParcel'],
                                             mobileNumber=data['mobileNumber'],
                                             selectedCategory=data['selectedCategory'],
                                            
                                             count=data['count'],
                                            enteredAmount=data['enteredAmount'])  # Add other fields
        donardetails.save()
        print (f"saved data: {donardetails}")
        return JsonResponse({'message': 'Success'})
    except json.JSONDecodeError as e:
            return JsonResponse({'error': str(e)}, status=400)
 else:
            return JsonResponse({'message': 'Invalid request method'}, status=400)

def generate_excel(request):
    donar_details = donar_data.objects.all().values('name', 'nameOnParcel', 'mobileNumber', 'selectedCategory', 'count', 'enteredAmount')
    df = pd.DataFrame.from_records(donar_details)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=donar_details.xls'

    df.to_excel(response, index=False)
    return response

def generate_pdf(request):
    donar_details = donar_data.objects.all()
    
    buffer = BytesIO()

    p = canvas.Canvas(buffer)
    p.drawString(100, 750, "Donar Details")

    # Add the rest of your PDF content here
    # Example: Loop through donar_details and add to PDF

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=donar_details.pdf'
    return response     
   
    
    
@method_decorator(csrf_exempt, name='dispatch')
class TodayCollection(View):
    def post(self, request, *args, **kwargs):
        # Get today's date
        now = datetime.now()
        today = now.date()
        # Get all collection data
        collection_data = CollectionData.objects.all()
        
          # Filter data for today
        today_collection_data = [entry for entry in collection_data if entry.timestamp.date() == today]

        # Calculate total collection in Python code
        today_collection = sum(entry.enteredAmount for entry in today_collection_data)
        
        if today_collection ==0:
            today_collection = 100  # Set to 100 if no data is found for today
        
        return JsonResponse({'TodayCollection': today_collection})
    
class ThisMonthCollection():
    def Post(self, request, *args, **kwargs):
        # Get this month's collection data (replace with your actual logic)
        this_month_collection = 5000  # Example data
        return responses({'this_month_collection': this_month_collection})
    
class DonationListCreateView(generics.ListCreateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    
################################################## User creation ################################################################
# class UserProfileCreateView(View):
#    @api_view(['POST'])  
#    def create_user_profil(self, request, *args, **kwargs):
#         try:
#             print(f"Received data: {request.data}")
#             data = json.loads(request.body)
#             username = data.get('username')
#             email = data.get('email')
#             password = data.get('password')
#             print ("Received data: {data}")
#             # Create a new user
#             user = get_user_model().objects.create_user(username=username, email=email, password=password)

#             # Create a user profile
#             user_profile = UserProfile.objects.create(user=user)

#             return JsonResponse({'message': 'User registered successfully'}, status=201)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)   
        
@csrf_exempt
def create_user_profile(request):
    print(f"Received data: {request.body}")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON data", status=400)

        serializer = UserProfileSerializer(data=data)
        if serializer.is_valid():
            user_profile = serializer.save()
           
            print(f"User profile created successfully: {user_profile}")
            return HttpResponse("Profile created successfully.")
        else:
            print(f"Validation errors: {serializer.errors}")
            return HttpResponse("Invalid data", status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_profile(request, user_id):
    user_profile = UserProfileModel.objects.get(pk=user_id)
    serializer = UserProfileSerializer(instance=user_profile, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'message': 'User profile updated successfully'})
    return JsonResponse({'error': serializer.errors}, status=400)


class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK) 
    
#####################################################################################################################################
     
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 
def homepage(request):
    donar_details = donar_data.objects.all()
    currency = 'INR'
    Amount = 60000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(Amount=Amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = Amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    
    # response = requests.get('http://127.0.0.1:8081/paymenthandler/')

    # if response.status_code == 200:
    #     data = response.json()
    #     context = {
    #         'details_data': data,
    #     }

    return render(request, 'homepage.html', {'donar_details': donar_details, **context})


    ##########################################################update user data########################################################################
  
@csrf_exempt
@require_POST
def update_profile(request, user_id=None):
    try:
        if user_id:
            # If user_id is provided, update the profile based on the user_id
            user_profile = get_object_or_404(UserProfile, pk=user_id)
        else:
            # If user_id is not provided, assume it's in the JSON data
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('user_id')
            user_profile = get_object_or_404(UserProfile, pk=user_id)

        # Handle profile update logic based on your requirements
        # For simplicity, let's assume you receive JSON data with updated fields
        user_profile.username = data.get('username', user_profile.username)
        user_profile.profile_image = data.get('profile_image', user_profile.profile_image)
        user_profile.coins = data.get('coins', user_profile.coins)
        user_profile.save()

        return JsonResponse({'success': True, 'updatedUserData': {'user_id': user_id, 'username': user_profile.username, 'profile_image': user_profile.profile_image, 'coins': user_profile.coins}})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
@require_POST
def sign_out(request):
    # Implement sign-out logic (e.g., clear authentication token, session)
    return JsonResponse({'message': 'User signed out'})

def csrf_token(request):
    csrf_token = get_token(request)
    print(f'CSRF Token Length: {len(csrf_token)}')
    return HttpResponse()

def get_donar_data(request):
    donor_data = list(donar_data.objects.values())  # Convert QuerySet to list for serialization
    return JsonResponse({'donor_data': donor_data})