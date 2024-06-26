from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

from rest_framework.views import APIView

from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError

from . models import Advocate, Company
from . serializers import AdvocateSerializer, CompanySerializer
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

# @api_view(['GET', 'PUT', 'DELETE'])
# def advocate_detail(request, username):
#     advocate = Advocate.objects.get(username=username)
#     if request.method == 'GET':
#         # data = username
#         serializer = AdvocateSerializer(advocate, many=False)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         advocate.username = request.data['username']
#         advocate.bio = request.data['bio']
        
#         advocate.save()
        
#         serializer = AdvocateSerializer(advocate, many=False)
#         return Response(serializer.data)
    
#     if request.method == 'DELETE':
#         advocate.delete()
#         return redirect('advocates')



# Class based view on the advocate details page
class AdvocateDetail(APIView):
    def get_object(self, username):
        try:
            return Advocate.objects.get(username=username)
        except Advocate.DoesNotExist:
            return JsonResponse('Advocate does not exists!')
    
    def get(self, request, username):
        # advocate = Advocate.objects.get(username=username)
        advocate = self.get_object(username)
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
    
    def put(self, request, username):
        # advocate = Advocate.objects.get(username=username)
        advocate = self.get_object(username)
        
        advocate.username = request.data['username']
        advocate.bio = request.data['bio']
        advocate.save()
        
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
    
    def delete(self, request, username):
        advocate = self.get_object(username)
        advocate.delete()
        return Response('advocates')
    
    
    
@api_view(['GET'])
def companies_list(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)