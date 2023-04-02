from django.db import models
from django.contrib.postgres.fields import ArrayField
import datetime
#from django.contrib.auth.base_user import BaseUserManager
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

##########   Vytvareni modelu, podle kterych se vytvori tabulky v databazi   #########

# Vytvoreni sberatelskeho predmetu pro hrace
class SberatelskyPredmet(models.Model):
    # id predmetu
    idsberpredmetu = models.CharField(max_length=30)

    # zda byl jiz nalezen (T/F)
    nalezeno = models.BooleanField()


# Vytvoreni modelu hrace



class Hrac(models.Model):

    # funkce pro určení defaultních hodnot polí
    def otevrenekese_default():
        default = []
        return default
    
    def putpredmety_default():
        default = []
        return default
    
    def sberpredmet_default():
        default = {"one": False, "two": False, "three": False, "four": False}
        return default
    
    def vlastnenekese_default():
        default = []
        return default
    def player_id_default():
        default = "P000000000000000000000"
        return default
    def putovni_predmet_default():
        return "TG00000000000000000000"

    # jmeno hrace
    username = models.CharField(max_length=30)

    # email hrace
    mail = models.EmailField()

    # heslo hrace
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    # id hrace
    player_id = models.CharField(max_length=22, default=player_id_default)

    # seznam otevrenych kesi
    otevrenekese = ArrayField(models.TextField(), default=otevrenekese_default, blank=True)

    otevrenekesepoc = models.IntegerField(default=0)
    # aktualni putovni predmet
    putpredmet = models.CharField(max_length=30, default=putovni_predmet_default)

    # koupene putovni predmety
    putpredmety = ArrayField(models.CharField(max_length=30), default=putpredmety_default, blank=True)

    # sberatelske predmety
    sberpredmet = models.JSONField(default=sberpredmet_default, blank=True)

    pocetsberpred = models.IntegerField(default=0)

    # seznam vlastnenych kesi
    vlastnenekese = ArrayField(models.CharField(max_length=12), default=vlastnenekese_default, blank=True)

    registrace = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.jmeno
    
    


# Vytovreni modelu karty
class Karta(models.Model):

    def card_id_default():
        return "GC0000000000"

    def putovni_predmet_default():
        return "TG00000000000000000000"
    
    
    # id karty
    idkarty = models.CharField(max_length=12)

    # nazev karty
    nazev = models.CharField(max_length=30, default='beef')

    # id vlastnika karty
    vlastnik = models.CharField(max_length=30)

    # souradnice karty
    zemdelka = models.DecimalField(max_digits=9, decimal_places=6)
    zemsirka = models.DecimalField(max_digits=9, decimal_places=6)

    # putovni predmet na karte
    putpredmet = models.CharField(max_length=30, default=putovni_predmet_default)

    # pocet nalezu karty
    pocetnalezu = models.IntegerField(default=0)
    
    popis = models.TextField(default='')
    
    
    

# Vytvoreni modelu putovniho predmetu
class PutovniPredmet(models.Model):
    
    def putovni_predmet_default():
        return "TG00000000000000000000"
    def upload_path(instance, filename):
        return '/'.join(['predmety', str(instance.vlastnik), filename])
    
    
    # id putocniho predmetu
    idputpredmetu = models.CharField(max_length=30, default=putovni_predmet_default)

    # kde se predmet nachazi: karta nebo aplikace (T/F) {Karta - True; Aplikace - False}
    pozice = models.BooleanField(default=False)

    # id karty nebo aplikace kde se predmet nachazi
    idpozice = models.CharField(max_length=30)

    # vlastnik predmetu (kdo ho vytvoril)
    vlastnik = models.CharField(max_length=30)

    # kde vsude se predmet nachazel
    karty = ArrayField(models.CharField(max_length=12, default=''), default=list, blank=True)

    # cesta k ulozenemu obrazku
    cesta = models.CharField(max_length = 100, default="images/")
    
    obrazek = models.ImageField(blank=True, null=True, upload_to="images/")

    #def __str__(self):
    #    return self.vlastnik


