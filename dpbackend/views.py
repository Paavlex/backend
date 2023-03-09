from django.shortcuts import render

from decimal import *
import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from dpbackend.models import Hrac
from dpbackend.serializers import HracSerializer
from dpbackend.serializers import KartaSerializer, PutovniPredmetSerializer, SberatelskyPredmetSerializer, UserSerializer
from dpbackend.models import Karta, PutovniPredmet, SberatelskyPredmet


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



# Class views pro modely

class hrac_viewset(viewsets.ModelViewSet):
    queryset = Hrac.objects.all()
    serializer_class = HracSerializer
    
    

    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        hrac = Hrac.objects.get(id= params['pk'])
        serializer = HracSerializer(hrac)
        return Response(serializer.data)

        
class karta_viewset(viewsets.ModelViewSet):
    queryset = Karta.objects.all()
    serializer_class = KartaSerializer

    def list(self, request):
        karty = Karta.objects.all()
        serializer = KartaSerializer(karty, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        
        try:

            karta = Karta.objects.get(vlastnik= params['pk'])
            serializer = KartaSerializer(karta)
            return Response(serializer.data)
        except:
            dict = {
                'putpredmet': 'TG0000000000000000000000000000'
            }
            return Response(dict)
        
           


class putovni_predmet_viewset(viewsets.ModelViewSet):
    queryset = PutovniPredmet.objects.all()
    serializer_class = PutovniPredmetSerializer
    filter_fields = ('vlastnik')


    def retrieve(self, request, *args, **kwargs):
        params = kwargs

        try:
            predmet = PutovniPredmet.objects.get(idpozice= params['pk'])
            serializer = PutovniPredmetSerializer(predmet)
            return Response(serializer.data)
        except:
            dict = {
                'idputpredmetu': 'TG0000000000000000000000000000',
                'cesta': 'assets/img/putpred2.jpg'
            }
            return Response(dict)

class sberatelsky_predmet_list(viewsets.ModelViewSet):
    queryset = SberatelskyPredmet.objects.all()
    serializer_class = SberatelskyPredmetSerializer


# Běžné class based views
class cesta_predmetu(APIView):
    def get(self, request, *args, **kwargs):
        params = kwargs
        predmet = PutovniPredmet.objects.get(vlastnik=params['vlastnik'])
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
        print(serializer.data)
        
        hrac = {
            'username': request.data["username"],
            'mail': request.data["email"],
            'user': serializer.data['id']
        }
        print(hrac)
        hrac_serializer = HracSerializer(data=hrac)
        
        hrac_serializer.is_valid(raise_exception=True)
        hrac_serializer.save()

        return Response(hrac_serializer.data)



# Vytvoření tokenu s vlastními poli
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer