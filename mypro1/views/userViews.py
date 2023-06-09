from django.shortcuts import render

from pymongo.mongo_client import MongoClient
from django.http import HttpResponse, JsonResponse
from mypro1.models import User
import json
import jwt
from bson import ObjectId
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

uri = "mongodb+srv://rupenjarsaniya:rupenjarsaniya1@cluster0.qqbbgum.mongodb.net/TaskDemo?retryWrites=true&w=majority"
client = MongoClient(uri)
dbname = client['TaskDemo']
userCollection = dbname['user']

def get_user_from_token(request):
    token = JWTAuthentication().get_validated_token(request)
    user = JWTAuthentication().get_user(token)
    return user

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Invalid request parameters.'}, status=400)

        try:
            # user = User.objects.create(username=username,email=email, password=make_password(password))
            received_json_data=json.loads(request.body)
            user = User(
                username = received_json_data["username"],
                password = make_password(received_json_data["password"]),
                email = received_json_data["email"],
            )
            userCollection.insert_one(json.loads(user.__str__()))
            
            # Generate token for the user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return JsonResponse({
                'message': 'User registered successfully.',
                'access_token': access_token,
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Invalid request parameters.'}, status=400)

        try:
            user_details = userCollection.find({"username": username})
            for doc in user_details:
                if check_password(password, doc['password']):
                    user = User(username=username, password=password,email=doc['email'])
                    print(user_details)
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    return JsonResponse({'message': 'User logged in successfully.', 'access_token': access_token}, status=200)
            return JsonResponse({'error': 'Invalid credentials.'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
@login_required
def get_user_data(request):
    if request.method == 'GET':
        try:
            data = json.loads(request.body)
            token = data.get('token')
            decoded_token = jwt.decode(token, algorithms=["HS256"], verify=False)
            print('datatttttt',decoded_token)
            user_id = str(request.user.id)
            user_details = userCollection.find({"_id": ObjectId(user_id)})
            users = []
            for doc in user_details:
                doc['_id'] = str(doc['_id'])
                users.append(doc)
            return JsonResponse({"data": users})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

# def get_user(request): 
#     if request.method=='GET':
#         users = []
#         user_details = userCollection.find({})
#         for doc in user_details:
#             doc['_id'] = str(doc['_id'])
#             users.append(doc)
#         return JsonResponse( {"data":users})


# @csrf_exempt    
# def get_user_by_id(request, id):
#     if request.method=='GET':
#         userId = ObjectId(id)
#         users = []
#         user_details = userCollection.find({"_id":userId})
#         for doc in user_details:
#             doc['_id'] = str(doc['_id'])
#             users.append(doc)
#         return JsonResponse( {"data":users})

#     else:
#         return HttpResponse("Invalid Request")

# @csrf_exempt 
# def create_user(request):
#     if request.method=='POST':
#         received_json_data=json.loads(request.body)
#         user = User(
#             name = received_json_data["name"],
#             email = received_json_data["email"],
#         )
#         userCollection.insert_one(json.loads(user.__str__()))
#         return JsonResponse(json.loads(user.__str__()))
#     else:
#         return HttpResponse("Invalid Request")
        
@csrf_exempt
def update_user(request, id):
    if request.method=='PUT':
        users = []
        try: 
            userId = ObjectId(id)
            received_json_data=json.loads(request.body)
            update = userCollection.update_one({"_id":userId}, {"$set": received_json_data})
            print(update.raw_result, type(update))

            user_details = userCollection.find({"_id":userId})
            for doc in user_details:
                doc['_id'] = str(doc['_id'])
                users.append(doc)
            return JsonResponse( { "data":users})
        except ValueError:
            return HttpResponse("Invalid Request")

    else:
        return HttpResponse("Invalid Request")

@csrf_exempt 
def delete_user(request, id):
    if request.method=='DELETE':
        users = []
        try: 
            userId = ObjectId(id)
            userCollection.delete_one({"_id":userId})
            user_details = userCollection.find({})
            for doc in user_details:
                doc['_id'] = str(doc['_id'])
                users.append(doc)
            return JsonResponse( { "data":users})
        except ValueError:
            return HttpResponse("Invalid Request")
    else:
        return HttpResponse("Invalid Request")

# python manage.py makemigrations 
# python manage.py migrate