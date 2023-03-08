from django.shortcuts import render

from decimal import *
import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from dpbackend.models import Hrac
from dpbackend.serializers import HracSerializer
from dpbackend.serializers import KartaSerializer, PutovniPredmetSerializer, SberatelskyPredmetSerializer, UserSerializer
from dpbackend.models import Karta, PutovniPredmet, SberatelskyPredmet




# Class views pro modely

class hrac_list(viewsets.ModelViewSet):
    queryset = Hrac.objects.all()
    serializer_class = HracSerializer
    
    

    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        hrac = Hrac.objects.get(username= params['pk'])
        serializer = HracSerializer(hrac)
        return Response(serializer.data)

        
class karta_list(viewsets.ModelViewSet):
    queryset = Karta.objects.all()
    serializer_class = KartaSerializer

    def list(self, request):
        karty = Karta.objects.all()
        serializer = KartaSerializer(karty, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        karta = Karta.objects.get(vlastnik= params['pk'])
        serializer = KartaSerializer(karta)
        return Response(serializer.data)


class putovni_predmet_list(viewsets.ModelViewSet):
    queryset = PutovniPredmet.objects.all()
    serializer_class = PutovniPredmetSerializer
    filter_fields = ('vlastnik')


    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        predmet = PutovniPredmet.objects.get(idpozice= params['pk'])
        serializer = PutovniPredmetSerializer(predmet)
        return Response(serializer.data)

class sberatelsky_predmet_list(viewsets.ModelViewSet):
    queryset = SberatelskyPredmet.objects.all()
    serializer_class = SberatelskyPredmetSerializer


# Běžné class based views
class cesta_predmetu(APIView):
    def get(self, request, *args, **kwargs):
        vlastnikpredmetu = kwargs.get('vlastnik')
        predmet = PutovniPredmet.objects.get(vlastnik=vlastnikpredmetu)
        serializerpredmetu = PutovniPredmetSerializer(predmet)
        kartydict = []

        for karta in serializerpredmetu.data['karty']:
            cache = Karta.objects.get(idkarty=karta)
            serializerkarty = KartaSerializer(cache)
            pozice = {'position':{'lng':Decimal(serializerkarty.data['zemdelka']), 'lat':Decimal(serializerkarty.data['zemsirka'])}}
            kartydict.append(pozice)

        return Response(kartydict)
    

class get_all_cards(APIView):
    def get(self, request, *args, **kwargs):
        karty = Karta.objects.all()
        cardserializer = KartaSerializer(karty, many=True)
        kartydict = []

        for karta in cardserializer.data:
            
            pozice = {'position':{'lng':Decimal(karta['zemdelka']), 'lat':Decimal(karta['zemsirka'])}}
            kartydict.append(pozice)

        return Response(kartydict)
    

class order_card(APIView):

    def get(self, request):
        return Response("POST only")

    def post(self, request):
        f = open("objednavky/"+request.data["lastname"]+"_"+request.data["firstname"]+".txt", "w+")
        f.write(json.dumps(request.data))
        f.close()

        return Response("{isItDone:Yes}")
    

class user_register(APIView):
    
    

    def get(self, request):
        queryset = get_user_model().objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user = get_user_model().objects.create_user(username=request.data["username"], email=request.data["email"], password=request.data["password"])
        serializer = UserSerializer(user)
        return Response(serializer.data)
