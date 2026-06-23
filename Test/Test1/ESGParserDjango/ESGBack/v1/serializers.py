from rest_framework import serializers
from .models import *


class ArticleSerializer(serializers.ModelSerializer):
   class Meta:
      model = Article
      fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
   class Meta:
      model = Project
      fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
   class Meta:
      model = Course
      fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
   class Meta:
      model = Event
      fields = '__all__'
