from django.contrib.auth.models import Group, User
from rest_framework import serializers, validators
from app.models import UserProfile, Ogloszenie, Kot, Zdjecie, Rezerwacja

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), f"A user with that Email already exists."
                    )
                ]
            }
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['adres_1', 'adres_2', 'nr_tel'] # 'user'
        
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

class RezerwacjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rezerwacja
        fields = ['ogloszenie', 'data'] # 'user'

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