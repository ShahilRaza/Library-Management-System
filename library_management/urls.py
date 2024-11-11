from django.contrib import admin
from django.urls import path, include 
from django.urls import path
# from graphene_django.views import GraphQLView







urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("library.urls")),    
]