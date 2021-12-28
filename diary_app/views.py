from django.http import response
from django.shortcuts import render
from rest_framework.views import APIView
from diary_app.serializers import *
from diary_app.services import *
from rest_framework.response import Response


class RegisterDiary(APIView):
    serializer_class = AuthenticationSerializer

    def post(self,request):
        serializer = AuthenticationSerializer(data=request.POST)
        if serializer.is_valid():
            response = register_diary(serializer.validated_data)
            return Response(response)
        else:
            return(serializer.errors)

class LoginDiary(APIView):
    serializer_class = AuthenticationSerializer
    def post(self,request):
        serializer = AuthenticationSerializer(data = request.POST)
        if serializer.is_valid():
            response = login_diary(serializer.validated_data)
            return Response(response)
        else:
            return Response((serializer.errors))

class Notes(APIView):
    serializer_class = NoteSerializer
    def get(self,request):
        response = view_note(data = request.GET)
        return Response(response)

    def post(self,request):
        user = request.user
        serializer = NoteSerializer(data = request.POST)
        if serializer.is_valid():
            response = init_note(serializer.validated_data,user)
            return Response(response)
        else:
            return Response(serializer.errors)

class ToDo(APIView):
    def post(self,request):
        serializer = ToDoSerializer(data = request.POST)
        if serializer.is_valid():
            response = init_todo(serializer.validated_data)
            return Response(response)
        else:
            return Response(serializer.errors)

class UpdateToDo(APIView):
    def post(self,request):
        response = update_todo(data = request.POST)
        return Response(response)

class Events(APIView):
    def get(self,request):
        response = view_event(data = request.GET)
        return Response(response)

    def post(self,request):
        user = request.user
        serializer = EventSerializer(data = request.POST)
        if serializer.is_valid():
            response = init_event(serializer.validated_data,user)
            return Response(response)
        else:
            return Response(serializer.errors)


class UpdateEvents(APIView):
    def post(self,request):
        response = update_event(data = request.POST)
        return Response(response)
