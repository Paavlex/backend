from rest_framework import serializers
from dpbackend.models import Hrac
from dpbackend.models import Karta
from dpbackend.models import PutovniPredmet
from dpbackend.models import SberatelskyPredmet
from django.contrib.auth import get_user_model


# Serializer Uživatele, serializace všech polí v modelu
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"

# Serializer Hráče, serializuje vybraná pole
class HracSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hrac
        fields = ['id','username','user','mail','otevrenekese','otevrenekesepoc','putpredmet','putpredmety','sberpredmet','pocetsberpred','vlastnenekese','registrace','player_id']

# Serializer Uživatele, serializace všech polí v modelu
class KartaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Karta
        fields = "__all__"

# Serializer Uživatele, serializace všech polí v modelu
class PutovniPredmetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PutovniPredmet
        fields = "__all__"

# Serializer Uživatele, použití všech polí v modelu
class SberatelskyPredmetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SberatelskyPredmet
        fields = ['idsberpredmetu','nalezeno']