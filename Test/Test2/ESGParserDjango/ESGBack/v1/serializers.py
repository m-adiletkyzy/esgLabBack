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


class OurArticleSerializer(serializers.ModelSerializer):
   image_url = serializers.ReadOnlyField()
   class Meta:
      model = OurArticle
      fields = '__all__'


class OurEventSerializer(serializers.ModelSerializer):
   image_url = serializers.ReadOnlyField()
   class Meta:
      model = OurEvent
      fields = '__all__'


class OurProjectSerializer(serializers.ModelSerializer):
   image_url = serializers.ReadOnlyField()
   class Meta:
      model = OurProject
      fields = '__all__'


class OurCourseSerializer(serializers.ModelSerializer):
   image_url = serializers.ReadOnlyField()
   class Meta:
      model = OurCourse
      fields = '__all__'


# For telegram bot

class ErrorSerializer(serializers.ModelSerializer):
   class Meta:
      model = ParsingError
      fields = '__all__'

class ArticlesToFilterSerializer(serializers.ModelSerializer):
   class Meta:
      model = ArticleToFilter
      fields = '__all__'
