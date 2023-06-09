from django.http import HttpResponse, JsonResponse
from mypro1.models import Task
from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import json

uri = "mongodb+srv://rupenjarsaniya:rupenjarsaniya1@cluster0.qqbbgum.mongodb.net/TaskDemo?retryWrites=true&w=majority"
client = MongoClient(uri)
dbname = client['TaskDemo']
taskCollection = dbname['task']

@csrf_exempt
def create_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        name = data.get('name')
        status = data.get('status')


        if user_id and name and status:
            task = Task(user=user_id, name=name, status=status)
            taskCollection.insert_one(json.loads(task.__str__()))
            return JsonResponse({'message': 'Task created successfully.'})
        else:
            return JsonResponse({'error': 'Invalid request parameters.'}, status=400)
    else:
        return HttpResponse("Invalid Request")

def get_task(request):
    if request.method == 'GET':
        user_id = request.GET.get('user')

        if user_id:
            tasks = []
            task_details = taskCollection.find({"user": user_id})
            for doc in task_details:
                doc['_id'] = str(doc['_id'])
                print(doc)
                tasks.append(doc)
            return JsonResponse({"data": tasks})
        else:
            return JsonResponse({"error": "userId parameter is required."}, status=400)
    else:
        return HttpResponse("Invalid Request")


@csrf_exempt
def delete_task(request, id):
    if request.method == 'DELETE':
        try:
            task_id = ObjectId(id)
            taskCollection.delete_one({"_id": task_id})
            return JsonResponse({'message': 'Task deleted successfully.'})
        except ValueError:
            return JsonResponse({'error': 'Invalid task ID.'}, status=400)
    else:
        return HttpResponse("Invalid Request")

@csrf_exempt
def update_task(request, id):
    if request.method == 'PUT':
        try:
            task_id = ObjectId(id)
            data = json.loads(request.body)
            taskCollection.update_one({"_id": task_id}, {"$set": data})
            return JsonResponse({'message': 'Task updated successfully.'})
        except ValueError:
            return JsonResponse({'error': 'Invalid task ID or request body.'}, status=400)
    else:
        return HttpResponse("Invalid Request")

def get_task_by_id(request, id):
    if request.method == 'GET':
        try:
            task_id = ObjectId(id)
            task = taskCollection.find_one({"_id": task_id})
            if task:
                task['_id'] = str(task['_id'])
                return JsonResponse({"data": task})
            else:
                return JsonResponse({'error': 'Task not found.'}, status=404)
        except ValueError:
            return JsonResponse({'error': 'Invalid task ID.'}, status=400)
    else:
        return HttpResponse("Invalid Request")
