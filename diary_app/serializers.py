
from django.db.models import fields
from diary_app.models import *
from rest_framework import serializers

class AuthenticationSerializer(serializers.Serializer):
    name = serializers.CharField(required=False) 
    username = serializers.CharField()
    password = serializers.CharField()

class ToDoSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    note_id = serializers.IntegerField()
    
    class Meta:
        model = ToDo
        fields  = ('id','title','done','note_id','cdate','udate')

class NoteSerializer(serializers.ModelSerializer):
    note_date = serializers.CharField()
    todo_list = serializers.SerializerMethodField()
    
    def get_todo_list(self,instance):
        to_dos = instance.todo_set.all()
        todo_ser = ToDoSerializer(to_dos, many = True)
        return todo_ser.data

    class Meta:
        model = Notes
        fields = ('id', 'note_date', 'note', 'image','cdate','udate','todo_list')


class EventSerializer(serializers.ModelSerializer):
    event_time = serializers.CharField()
    event_name = serializers.CharField()
    
    class Meta:
        model = Events
        fields  = ('id','event_time','event_name','remind','cdate','udate')





