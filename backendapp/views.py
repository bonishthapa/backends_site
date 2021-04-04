from django.shortcuts import render, redirect
from rest_framework import status,viewsets,generics
from rest_framework.decorators import  action
from django.conf import settings
from rest_framework.response import Response
from rest_framework.parsers import ParseError
from .serializers import MaintitleSerializer,SubtitleSerializer,NewUserSerializer
from .models import MainTitle,SubTitle,User
from rest_framework import filters
from django.http import HttpResponse
from .utils import Util
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.hashers import make_password
import jwt
from rest_framework.permissions import IsAuthenticated,AllowAny
 


class MaintitleApi(viewsets.ModelViewSet):
    queryset = MainTitle.objects.all()
    serializer_class = MaintitleSerializer
    #permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    #def create(self, request, **kwargs):
    #    if self.request.user.is_active:
    #        serializer = MaintitleSerializer(data=request.data)
    #        if serializer.is_valid():
    #            serializer.save(author=request.user)
    #            return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, **kwargs):
        queryset = MainTitle.objects.all()
        main = MaintitleSerializer(queryset, many=True, context=self.context).data
        return main

class SubtitleApi(viewsets.ModelViewSet):
    queryset = SubTitle.objects.all()
    serializer_class = SubtitleSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


    @action(detail=True, methods=['POST'])
    def upload_image(request):
        try:
            file = request.data['file']
        except KeyError:
            raise ParseError('Request has no resource file attached')
        subtitle = SubTitle.objects.create(image=file)



class RegisterAPIView(generics.GenericAPIView):
    serializer_class = NewUserSerializer

    def post(self,request):
        user = request.data
        serializer  = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save(password=make_password(self.request.data['password']))

        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token
        relativeLink = reverse('email-verify')
        current_site = get_current_site(request).domain
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'hi '+user.username+' Use link below\n' +absurl
        data ={
            'email_body': email_body,
            'email_subject':'Verify Your Email',
            'to_email':user.email
        }
        Util.send_email(data)

        return Response(user_data,status=status.HTTP_201_CREATED)

class Verify_Email(generics.GenericAPIView):
    def get(self,request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
                return Response({'email':'Successfully verified email'},status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'token expired'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)