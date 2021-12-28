from diary_app.models import *
from diary_app.serializers import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from diary_app.views import *
from django.db import transaction
from rest_framework.authtoken.models import Token


def build_response(status,data):
    response = {
        'status' : status,
         'data' : data
    }
    return response


def register_diary(value):
    try:
        username = value.get('username')
        password = value.get('password')
        name = value.get('name')

        with transaction.atomic():
            user = User.objects.create(username = username)
            user.set_password(password)
            user.save()
            token = Token.objects.create(user=user)
            diary = Diary.objects.create(name=name,user=user)
            return_data = {'token':token.key}
            response = build_response('success',return_data)
            return response
    except Exception as e:
        return_data = {
            'error' : str(e)
        }
        response = build_response('Failure',return_data)
        return response

def login_diary(data):
    try:
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username,password=password)

        if user:
            token,created = Token.objects.get_or_create(user=user)
            status = 'success'
            return_data = {'token': token.key}
        else:
            status = 'Failure'
            return_data = {
                'error': "There is no existing user, please register the user first and then try Login"
            }
        response = build_response(status,return_data)
        return response
    except Exception as exc:
        return_data = {
            'error' : str(exc)
        }
        return('Failure', return_data)

def init_note(data,user):
    try:
        note_date = data.get('note_date')
        image = data.get('image')
        diary_note = data.get('note')
        diary = user.diary
        notes = Notes.objects.create(note_date = note_date, image = image, note = diary_note, diary = diary)
        notedata_serializer = NoteSerializer(notes)
        return_data = notedata_serializer.data
        response = build_response('success', return_data)
        return response

    except Exception as e:
        return_data = {
            'error' : str(e)
        }
        response = build_response('Failure',return_data)
        return response

def view_note(data):
    try:
        if data:
            note_date = data.get('note_date')
            diary_note = data.get('note')
            if note_date:
                notes = Notes.objects.get(note_date = note_date)
                notedata_serializer = NoteSerializer(notes)
                return_data = notedata_serializer.data
                response = build_response('success', return_data)
            else:
                notes = Notes.objects.filter(note = diary_note)
                notedata_serializer = NoteSerializer(notes, many = True)
                return_data = notedata_serializer.data
                response = build_response('success', return_data)
        else:
            notes = Notes.objects.all()
            notedata_serializer = NoteSerializer(notes, many=True)
            return_data = notedata_serializer.data
            response = build_response('success', return_data)
        return response

    except Exception as e:
        return_data = {
            'error' : str(e)
        }
        response = build_response('Failure',return_data)
        return response


def init_todo(data):
    try:
        todo = ToDo.objects.create(title = data.get('title') , note_id = data.get('note_id'))
        todo_serializer = ToDoSerializer(todo)
        retun_data = todo_serializer.data
        response = build_response('Success',retun_data)
        return response

    except Exception as e:
        return_data = {
            'error': str(e)
        }
        response = build_response('Failure',return_data)
        return response


def update_todo(data):
    try:
        todolist = ToDo.objects.filter(note_id = data.get('note_id'))
        if todolist:
            for todo in todolist:
                if not todo.done:
                    todo.done = True
                    todo.save()
                    todo_serializer = ToDoSerializer(todolist,many = True)
                    return_data = todo_serializer.data
                    status = 'Success'
                else:
                    status = 'Failure'
                    return_data = {
                    'error': "This todo list is already completed and updated"
                }
        else:
            status = 'Failure'
            return_data = {
                'error' : "There is no todo list for this note, please try with differernt note"
            } 
        response = build_response(status, return_data)
        return response
    except Exception as e:
        return_data ={
            'error' : str(e)
        }
        response = build_response('Failure', return_data)
        return response


def init_event(data,user):
    try:
        event_time = data.get('event_time')
        event_name = data.get('event_name')
        diary = user.diary
        event_datetime = Events.objects.filter(event_time=event_time)
        if not event_datetime:
            events = Events.objects.create(event_time = event_time, event_name = event_name, diary = diary)
            eventdata_serializer = EventSerializer(events)
            return_data = eventdata_serializer.data
            status = 'success'
        else:
            return_data = {
                'error' : "This date and time is already booked for another event, please try for some other time or date"
            }
            status = 'Failure'
        response = build_response(status, return_data)
        return response

    except Exception as e:
        return_data = {
            'error' : str(e)
        }
        response = build_response('Failure',return_data)
        return response


def view_event(data):
    try:
        if data:
            event_time = data.get('event_time')
            event_name = data.get('event_name')
            if event_time:
                events = Events.objects.get(event_time = event_time)
                eventdata_serializer = EventSerializer(events)
                return_data = eventdata_serializer.data
                response = build_response('success', return_data)
            else:
                events = Events.objects.get(event_name = event_name)
                eventdata_serializer = EventSerializer(events)
                return_data = eventdata_serializer.data
                response = build_response('success', return_data)
        else:
            events = Events.objects.all()
            eventdata_serializer = EventSerializer(events, many=True)
            return_data = eventdata_serializer.data
            response = build_response('success', return_data)
        return response

    except Exception as e:
        return_data = {
            'error' : str(e)
        }
        response = build_response('Failure',return_data)
        return response


def update_event(data):
    try:
        events = Events.objects.get(id = data.get('event_id'))
        if not events.remind:
            events.remind = True
            events.save()
            event_serializer = EventSerializer(events)
            return_data = event_serializer.data
            status = 'Success'
        else:
            status = 'Failure'
            return_data = {
                'error': "This Event is already completed and updated"
            }
        response = build_response(status, return_data)
        return response
    except Exception as e:
        return_data ={
            'error' : str(e)
        }
        response = build_response('Failure', return_data)
        return response
