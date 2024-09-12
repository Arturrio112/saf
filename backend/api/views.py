from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
import os

def load_json(filename):
    filepath = os.path.join(os.path.dirname(__file__), 'data', filename)
    with open(filepath, 'r') as file:
        return json.load(file)

def metrics(request):
    data = load_json('metrics.json')
    return JsonResponse(data)

def sensors(request):
    data = load_json('sensors.json')
    return JsonResponse(data)

def sensor_types(request):
    data = load_json('sensorTypes.json')
    return JsonResponse(data)
