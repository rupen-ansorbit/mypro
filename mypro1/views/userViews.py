from django.shortcuts import render

from pymongo.mongo_client import MongoClient
from django.http import HttpResponse, JsonResponse
from mypro1.models import User
import json
from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt

uri = "mongodb+srv://rupenjarsaniya:rupenjarsaniya1@cluster0.qqbbgum.mongodb.net/TaskDemo?retryWrites=true&w=majority"
client = MongoClient(uri)
dbname = client['TaskDemo']
userCollection = dbname['user']

def get_user(request): 
    if request.method=='GET':
        users = []
        user_details = userCollection.find({})
        for doc in user_details:
            doc['_id'] = str(doc['_id'])
            users.append(doc)
        return JsonResponse( {"data":users})


@csrf_exempt    
def get_user_by_id(request, id):
    if request.method=='GET':
        userId = ObjectId(id)
        users = []
        user_details = userCollection.find({"_id":userId})
        for doc in user_details:
            doc['_id'] = str(doc['_id'])
            users.append(doc)
        return JsonResponse( {"data":users})

    else:
        return HttpResponse("Invalid Request")

@csrf_exempt 
def create_user(request):
    if request.method=='POST':
        received_json_data=json.loads(request.body)
        user = User(
            name = received_json_data["name"],
            email = received_json_data["email"],
        )
        userCollection.insert_one(json.loads(user.__str__()))
        return JsonResponse(json.loads(user.__str__()))
    else:
        return HttpResponse("Invalid Request")
        
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