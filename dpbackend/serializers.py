from rest_framework import serializers
from dpbackend.models import Hrac
from dpbackend.models import Karta
from dpbackend.models import PutovniPredmet
from dpbackend.models import SberatelskyPredmet
from django.contrib.auth import get_user_model



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"


class HracSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hrac
        fields = ['id','username','user','mail','otevrenekese','otevrenekesepoc','putpredmet','putpredmety','sberpredmet','pocetsberpred','vlastnenekese','registrace']

class KartaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Karta
        fields = ['idkarty','nazev','vlastnik','zemdelka', 'zemsirka', 'putpredmet', 'pocetnalezu']

class PutovniPredmetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PutovniPredmet
        fields = ['idputpredmetu', 'pozice', 'idpozice', 'vlastnik','karty', 'cesta']

class SberatelskyPredmetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SberatelskyPredmet
        fields = ['idsberpredmetu','nalezeno']