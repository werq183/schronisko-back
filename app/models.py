from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    adres_1 = models.CharField(max_length=255, blank=True)
    adres_2 = models.CharField(max_length=255, blank=True)
    nr_tel = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


class Kot(models.Model):
    imie = models.CharField(max_length=255)
    plec = models.CharField(max_length=255)
    kolor = models.CharField(max_length=255)
    siersc = models.CharField(max_length=255)
    rasa = models.CharField(max_length=255)
    wiek = models.IntegerField()


class Ogloszenie(models.Model):
    kot = models.ForeignKey(Kot, on_delete=models.CASCADE)
    opis = models.TextField()
    data = models.DateTimeField()


class Zdjecie(models.Model):
    ogloszenie = models.ForeignKey(Ogloszenie, on_delete=models.CASCADE)
    dane = models.ImageField(upload_to='')


class Rezerwacja(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    ogloszenie = models.OneToOneField(Ogloszenie, on_delete=models.CASCADE)
    data = models.DateTimeField()
