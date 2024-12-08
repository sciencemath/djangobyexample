from django.db.models import Count
from rest_framework import serializers
from courses.models import Content, Course, Module, Subject

class ItemRelatedField(serializers.RelatedField):
  def to_representation(self, value):
    return value.render()
  
class ContentSerializer(serializers.ModelSerializer):
  item = ItemRelatedField(read_only=True)
  class Meta:
    model = Content
    fields = ['order', 'item']

class ModuleWithContentsSerializer(serializers.ModelSerializer):
  contents = ContentSerializer(many=True)
  class Meta:
    model = Module
    fields = ['order', 'title', 'description', 'contents']

class CourseWithContentsSerializer(serializers.ModelSerializer):
  modules = ModuleWithContentsSerializer(many=True)
  class Meta:
    model = Course
    fields = [
      'id',
      'subject',
      'title',
      'slug',
      'overview',
      'created',
      'owner',
      'modules'
    ]

class ModuleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Module
    fields = ['order', 'title', 'description']

class CourseSerializer(serializers.ModelSerializer):
  # To get related models (many2many) instead of just the primary keys
  # however this does introduce another query, we can reduce SQL requets 
  # by using `prefetch_related()`
  # modules = serializers.StringRelatedField(many=True, read_only=True)
  modules = ModuleSerializer(many=True, read_only=True)

  class Meta:
    model = Course
    fields = [
      'id',
      'subject',
      'title',
      'slug',
      'overview',
      'created',
      'owner',
      'modules'
    ]

class SubjectSerializer(serializers.ModelSerializer):
  total_courses = serializers.IntegerField()
  popular_courses = serializers.SerializerMethodField()

  def get_popular_courses(self, obj):
    courses = obj.courses.annotate(
      total_students=Count('students')
    ).order_by('total_students')[:3]
    if courses:
      return [
        f'{c.title} ({c.total_students})' for c in courses
      ]
    return [
      'no students enrolled in this course (0 students)'
    ]

  class Meta:
    model = Subject
    fields = ['id', 'title', 'slug', 'total_courses', 'popular_courses']