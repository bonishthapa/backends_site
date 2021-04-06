from rest_framework import serializers
from .models import MainTitle,SubTitle,User
from django.template.defaultfilters import slugify
from django.contrib.auth.hashers import make_password


class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username','first_name','last_name','password']
        read_only_fields = ('is_active','is_verified')
        

        def create(self, validated_data):
            user = User(
                email=validated_data['email'],
                username=validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user



class SubtitleSerializer(serializers.ModelSerializer):
    #maintitle = serializers.SlugRelatedField(
    #    many=True,
    #    read_only=True,
    #    slug_field='title'
    #)
    #maintitle = serializers.CharField( source="maintitle.title", read_only=True)
    slug = serializers.SerializerMethodField()
    def get_slug(self, instance):
        return slugify(instance.title)

    image = serializers.ImageField(required = False)
    class Meta:
        model = SubTitle
        fields = ['id','title','slug','image','description','created_on','available_on','maintitle']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class MaintitleSerializer(serializers.ModelSerializer):
    author = serializers.CharField( source="author.username", read_only=True)
    subtitle = SubtitleSerializer(many=True,read_only=True)
    slug = serializers.SerializerMethodField()
    def get_slug(self, instance):
        return slugify(instance.title)

    image = serializers.ImageField(required = False)
    class Meta:
        tracks = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
     )
        model = MainTitle
        fields=['id','author','title','slug','image','description','created_on','subtitle']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
