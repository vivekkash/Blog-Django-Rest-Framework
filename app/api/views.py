from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from . serializers import RegisterUserSerializer, LoginSerializer, BlogSerializer
from . models import Blog
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from . permissions import IsResourceOwner
from django.core.paginator import Paginator


class RegisterView(APIView):
    
    def post(self, request, format=None):
        
        serializer = RegisterUserSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data, 'message': 'User created'}, status=status.HTTP_200_OK)
        
        return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
    
    
    
class LoginView(APIView):
    
    def post(self, request, format=None):
        
        serializer = LoginSerializer(data = request.data)
        
        if serializer.is_valid():
            
                token = serializer.get_jwt_token(serializer.data)
                
                if token:
                    
                    return Response({'data': {'token':str(token.access_token), 'refresh_token':str(token)}}, status=status.HTTP_200_OK)
                
                else:
                    
                    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        
        return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 

class BlogListView(APIView):
    
    def get(self, request):
        
        if request.GET.get('s'):
            blogs = Blog.objects.filter(Q(title__icontains=request.GET.get('s')) | Q (description__icontains=request.GET.get('s')))
        else:
            blogs = Blog.objects.all()
        
        try:    
            page = request.GET.get('page',1)
            paginator = Paginator(blogs,3)    
            blogs = paginator.page(page)
        except:
            
            return Response({'error': 'Thank you! No more blogs'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BlogSerializer(blogs, many=True)
        
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    
       
class BlogDetailsView(APIView):
    
    permission_classes=[IsAuthenticated,IsResourceOwner]
    authentication_classes=[JWTAuthentication]
    
    
    def post(self, request):
        
        try:
            data = request.data
            
            data['user'] = request.user.id
            
            serializer = BlogSerializer(data = data)
            
            if serializer.is_valid():
                
                serializer.save()
                
                return Response({
                    'data': serializer.data,
                    'message': 'Blog created Successfully'
                }, status=status.HTTP_201_CREATED)
        
            else:
                
                return Response({
                    'error': serializer.errors,
                    'message': 'Blog creation failed',
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:

                return Response({
                    'error': str(e),
                    'message': 'Something went wrong',
                }, status=status.HTTP_400_BAD_REQUEST)
            
            
    def get(self, request):
        
        try:
            
            if request.GET.get('s'):
                    blogs = Blog.objects.filter(Q(user=request.user.id), Q(title__icontains=request.GET.get('s')) | Q(description__icontains=request.GET.get('s'))).order_by('-updated_at')
            else:             
                    blogs = Blog.objects.filter(user=request.user.id).order_by('-updated_at')
            
            serializer = BlogSerializer(blogs, many=True)
            
            return Response({'data':serializer.data},status=status.HTTP_200_OK)    
        
        except Exception as e:

                return Response({
                    'error': str(e),
                    'message': 'Something went wrong',
                }, status=status.HTTP_400_BAD_REQUEST)
            
                     

    def put(self, request, pk=None):
        
        try: 
            data = request.data
            
            blog = Blog.objects.filter(uid=data['uid']).first()
            
            
            if request.user.id != blog.user.id:
                
                return Response({
                        'error': 'Unauthorized',
                        'message': 'Blog is not owned by you',
                    }, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                
                
                serializer = BlogSerializer(blog, data=data, partial=True)
                
                if serializer.is_valid():
                    serializer.save()    
                    
                    return Response({
                        'data': serializer.data,
                        'message': 'Blog updated Successfully'
                    }, status=status.HTTP_200_OK)
            
                else:
                    
                    return Response({
                        'error': serializer.errors,
                        'message': 'Blog updation failed',
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
        except Exception as e:
            
              return Response({
                    'error': str(e),
                    'message': 'Something went wrong',
                }, status=status.HTTP_400_BAD_REQUEST)
            
                     
                     
    def delete(self, request):
        
        data = request.data
        
        blog = Blog.objects.filter(uid=data['uid']).first()
            
        if request.user.id != blog.user.id:
                
            return Response({
                        'error': 'Unauthorized',
                        'message': 'Blog is not owned by you',
                }, status=status.HTTP_400_BAD_REQUEST)
                
        else:
                
            blog.delete()
                    
            return Response({
                            'data': [],
                            'message': 'Blog deleted Successfully'
                        }, status=status.HTTP_200_OK)
                
        