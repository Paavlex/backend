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
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import SuspiciousOperation

from django.contrib.auth import get_user_model

from dpbackend.models import Hrac
from dpbackend.serializers import HracSerializer
from dpbackend.serializers import KartaSerializer, PutovniPredmetSerializer, SberatelskyPredmetSerializer, UserSerializer
from dpbackend.models import Karta, PutovniPredmet, SberatelskyPredmet


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from . import idhelper

# Class views pro modely

class hrac_viewset(viewsets.ModelViewSet):
    queryset = Hrac.objects.all()
    serializer_class = HracSerializer
    
    
    # Retrieve pomocí .get získává jeden daný objekt v databázi
    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        hrac = Hrac.objects.get(id= params['pk'])
        serializer = HracSerializer(hrac)
        return Response(serializer.data)

        
class karta_viewset(viewsets.ModelViewSet):
    queryset = Karta.objects.all()
    serializer_class = KartaSerializer

    # Vrací všechny objekty v databázi
    def list(self, request):
        karty = Karta.objects.all()
        serializer = KartaSerializer(karty, many=True)
        return Response(serializer.data)

    # Retrieve pomocí .filter získává několik daných objektů v databázi
    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        print("trying")
        
        try:

            karta = Karta.objects.filter(vlastnik= params['pk'])
            serializer = KartaSerializer(karta, many=True)
            return Response(serializer.data)
        except:
            dict = {
                'putpredmet': 'TG0000000000000000000000000000'
            }
            return Response(dict)
        
           

# Retrieve získává jeden, nebo několik daných objektů v databázi
class putovni_predmet_viewset(viewsets.ModelViewSet):
    queryset = PutovniPredmet.objects.all()
    serializer_class = PutovniPredmetSerializer

    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        
        try:
            try:
                predmety = PutovniPredmet.objects.filter(vlastnik= params['pk'])
            except:
                predmety = PutovniPredmet.objects.get(vlastnik= params['pk'])
                
                
            serializer = PutovniPredmetSerializer(predmety, many=True)
            return Response(serializer.data)
        except:
            
            # Pokud objekt neexistuje, vrací prázný sběratelský předmět
            dict = {
                'idputpredmetu': 'TG0000000000000000000000000000',
                'cesta': 'assets/img/putpred2.jpg'
            }
            return Response(dict)
        
        
    def post(self, request, *args, **kwargs):
        obrazek = request.data['obrazek']
        vlastnik = request.data['vlastnik']
        idpozice = request.data['idpozice']
        
        
        PutovniPredmet.objects.create(vlastnik=vlastnik,obrazek=obrazek,idpozice=idpozice)
        return Response({"Created": True})

class sberatelsky_predmet_list(viewsets.ModelViewSet):
    queryset = SberatelskyPredmet.objects.all()
    serializer_class = SberatelskyPredmetSerializer



# Běžné class based views

class put_predmet_pozice(APIView):
    
    # Zídkání putovního předmětu na dané pozici
    def get(self, params, *args, **kwargs):
        params = kwargs
        predmet = PutovniPredmet.objects.get(idpozice=params['pk'])
        serializer = PutovniPredmetSerializer(predmet)
        
        return Response(serializer.data)
    




class cesta_predmetu(APIView):
    
    # Zídkání pozic všech karet, kterými putovní předmět prošel
    
    def post(self, request, *args, **kwargs):
        cardstoget = []
        cardstoget = request.data
        cardstosend = []
        
        for card in cardstoget:
            
            tmp = Karta.objects.get(idkarty = card)
            serializer = KartaSerializer(tmp)
            pozice = {
                'id':serializer.data['id'],
                'position':{'lng':Decimal(serializer.data['zemdelka']), 'lat':Decimal(serializer.data['zemsirka'])}}
            cardstosend.append(pozice)
        return Response(cardstosend)
    
    
    
    
    
    
class card_info(APIView):
    
    # Získání informací o několika kartách
    def post(self, request, *args, **kwargs):
        cardstoget = []
        cardstoget = request.data['cards']
        cardstosend = []
        
        for card in cardstoget:
            tmp = Karta.objects.get(idkarty = card)
            serializer = KartaSerializer(tmp)
            cardstosend.append(serializer.data)
        
        return Response(cardstosend)
    

class get_all_cards(APIView):
    
    # Zídkání informací o všech kartách
    def get(self, request, *args, **kwargs):
        karty = Karta.objects.all()
        cardserializer = KartaSerializer(karty, many=True)
        kartydict = []

        for karta in cardserializer.data:
            
            pozice = {'id': karta['id'],'nazev':karta['nazev'],'position':{'lng':Decimal(karta['zemdelka']), 'lat':Decimal(karta['zemsirka'])}}
            kartydict.append(pozice)

        return Response(kartydict)
    
class get_all_cards_andoid(APIView):
    def get(self, request, *args, **kwargs):
        karty = Karta.objects.all()
        cardserializer = KartaSerializer(karty, many=True)
        kartydict = []

        for karta in cardserializer.data:
            
            pozice = {'id': karta['id'],'nazev':karta['nazev'],'position':{'lng':Decimal(karta['zemdelka']), 'lat':Decimal(karta['zemsirka'])}}
            kartydict.append(pozice)

        return Response({"cards": kartydict})

class card_detail(APIView):
    
    # Získání informací o jedné dané kartě
    def get(self, request, *args, **kwargs):
        params = kwargs
        karta = Karta.objects.get(id = params['id'])
        serializer = KartaSerializer(karta)
        return Response(serializer.data)
    
    # Úprava informací o dané kartě
    def put(self, request, *args, **kwargs):
        print(request.data)
        data = request.data
        karta = Karta.objects.get(id = data['id'])
        karta.nazev = data['nazev']
        karta.zemdelka = data['zemdelka']
        karta.zemsirka = data['zemsirka']
        karta.popis = data['popis']
        
        karta.save()
        
        serializer = KartaSerializer(karta)
        return Response(serializer.data)
        
    # Získání informací o jedné dané kartě
    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        
        try:

            karta = Karta.objects.get(id= params['pk'])
            serializer = KartaSerializer(karta)
            return Response(serializer.data)
        except:
            raise Exception


class order_card(APIView):

    # Zabránení POST
    def get(self, request):
        return Response("POST only")

    # Vytvoření objednávky karty
    def post(self, request):
        f = open("objednavky/"+request.data["lastname"]+"_"+request.data["firstname"]+".txt", "w+")
        f.write(json.dumps(request.data))
        f.close()

        return Response("{isItDone:Yes}")
    

class user_register(APIView):
    
    # Povolení pro přístup k tomuto endpointu, nsataveno volné pro všechny
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = get_user_model().objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # Vytvoření nového uživatele
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
        user_id = Hrac.objects.get(id = hrac_serializer.data['id'])
        user_id.player_id = idhelper.getplayerid(hrac_serializer.data['id'])
        user_id.save()
        
        returnPLayer = Hrac.objects.get(id=hrac_serializer.data['id'])
        newSer = HracSerializer(returnPLayer)
        
        # TODO: certifikát

        return Response(newSer.data)


class item_upload(APIView):
    
    # vytvoření putovního předmětu
    def post(self, request, *args, **kwargs):
        
        
        
        
        
        image = request.data['obrazek']
        player = request.data['idpozice']
        vlas = request.data['vlastnik']
        cesta = request.data['cesta']
        player = Hrac.objects.get(id = player)
        playerSerializer = HracSerializer(player)
        
        # Kontrola zda již hráč nemá u sebe putovní předmět
        if (playerSerializer.data['putpredmet'] == "TG00000000000000000000"):
        
            item ={
                'vlastnik':vlas,
                'obrazek':image,
                'idpozice':player,
                'cesta':"images/"+cesta}
            
            itemserializer = PutovniPredmetSerializer(data=item)
            itemserializer.is_valid(raise_exception=True)
            itemserializer.save()
            print(itemserializer.data['id'])
            newItem = PutovniPredmet.objects.get(id = itemserializer.data['id'])
            newItem.idputpredmetu = idhelper.getitemid(itemserializer.data['id'])
            newItem.save()
            
            
            player.putpredmety.append(newItem.idputpredmetu)
            player.putpredmet = newItem.idputpredmetu
            player.save()
            itemserializer = PutovniPredmetSerializer(newItem)
            
            return Response(itemserializer.data)
        else:
            return Response({'canCreate': False})
        
class open_cache(APIView):
    
    # Otevření keše, hlavně přepsání informací v databázi dle poskytnutých informací
    def post(self, request, *args, **kwargs):
        player_id = request.data['player_id']
        cache_id = request.data['cache_id']
        
        cache = Karta.objects.get(idkarty=cache_id)
        player = Hrac.objects.get(id=player_id)
        
        #ziskani predmetu
        cacheitem = cache.putpredmet
        playeritem = player.putpredmet
        #vymena predmetu
        cache.putpredmet = playeritem
        player.putpredmet = cacheitem
        
        cache.pocetnalezu = cache.pocetnalezu+1
        player.otevrenekese.append(cache_id)
        player.otevrenekesepoc = player.otevrenekesepoc+1
        cache.save()
        player.save()
        
        #try:
        putpredmet1 = PutovniPredmet.objects.get(idpozice=player_id)
        putpredmet2 = PutovniPredmet.objects.get(idpozice=cache_id)
        putpredmet1.idpozice = cache_id
        putpredmet2.idpozice = player_id
        putpredmet1.pozice = True
        putpredmet2.pozice = False
        putpredmet1.karty.append(cache_id)
        putpredmet1.save()
        putpredmet2.save()
        #except:
        #    pass
        
        #try:
        
        
        
        
        #except:
        #    pass
        
        # zvyseni poctu nalezu karty a hrace
        # U hrace take zarazeni kese do seznamu nalezenych kesi
        
        
        # TODO funkce pro odemknuti sber. predmetu
        return Response({"success": True})



# Vytvoření tokenu s vlastními poli
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

# Defaultní metoda z simpleJWT
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer