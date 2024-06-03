from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q


from . models import Advocate
from . serializers import AdvocateSerializer
# Create your views here.

@api_view(['GET'])
def endpoints(request):
    data = ['/advocates', 'advocates/:username']
    return Response(data)

@api_view(['GET', 'POST']) 
def advocate_list(request):
    # Handles GET requests
    if request.method == 'GET':
        # data = ['Dennis', 'Tadas', 'Max']
        query = request.GET.get('query')
        
        if query == None:
            # print('Query nai')
            query = ''
            
        # advocates = Advocate.objects.all()
        # advocates = Advocate.objects.filter(username__icontains=query, bio__icontains=query) 
        
        # for advanced queries
        advocates = Advocate.objects.filter(Q(username__icontains=query) | Q(bio__icontains=query)) 
        serializer = AdvocateSerializer(advocates, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        print(request.data)
        # return Response('Done')
        advocate = Advocate.objects.create(
            username = request.data['username'],
            bio = request.data['bio']
        )
        
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)

@api_view(['GET'])
def advocate_detail(request, username):
    # data = username
    advocates = Advocate.objects.get(username=username)
    serializer = AdvocateSerializer(advocates, many=False)
    return Response(serializer.data)