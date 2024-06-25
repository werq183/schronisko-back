from django.contrib.auth.models import Group, User
from rest_framework import serializers, validators
from app.models import UserProfile, Ogloszenie, Kot, Zdjecie, Rezerwacja

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Usuwam 'password', bo nie chcemy go eksponować
        extra_kwargs = {
            "id": {"read_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        queryset=User.objects.all(), message="A user with that email already exists."
                    )
                ]
            }
        }

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Dołączamy dane użytkownika

    class Meta:
        model = UserProfile
        fields = ['user', 'adres_1', 'adres_2', 'nr_tel']
        
class KotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kot
        fields = '__all__'

class ZdjecieSerializer(serializers.ModelSerializer):
    dane = serializers.SerializerMethodField()  # Używamy SerializerMethodField

    class Meta:
        model = Zdjecie
        fields = '__all__'

    def get_dane(self, obj):
        request = self.context.get('request')
        if obj.dane:
            return request.build_absolute_uri(obj.dane.url)
        return None
   
class OgloszenieSerializer(serializers.ModelSerializer):
    kot = KotSerializer()
    zdjecie_set = ZdjecieSerializer(many=True, read_only=True)
    is_reserved = serializers.SerializerMethodField()
    class Meta:
        model = Ogloszenie
        fields = '__all__'
    def get_is_reserved(self, obj):
        return Rezerwacja.objects.filter(ogloszenie=obj).exists()

'''class RezerwacjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rezerwacja
        fields = ['ogloszenie', 'data', 'user'] # 'user'''''

class RezerwacjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rezerwacja
        fields = ['ogloszenie']

    def create(self, validated_data):
        ogloszenie = self.context['ogloszenie']
        user = self.context['user']
        return Rezerwacja.objects.create(ogloszenie=ogloszenie, uzytkownik=user, **validated_data)


# OOTB
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
# OOTB 
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']