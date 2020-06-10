import secrets
import datetime
from .decorators import access_and_errors
from .models import Users
from .exceptions import RequestFatal, RequestWarning
from .utils import parse_data


def add_user(data):
    note, created = Users.objects.get_or_create(
        email=data['email'],
    )

    if not created:
        raise RequestWarning(208, 'Already added')
    Users.objects.filter(email=data['email']).update(**data)


def activate(data):
    note = Users.objects.filter(
        email=data["email"],
    )

    if not note.exists():
        raise RequestFatal(404, 'User not found')
    if note.count() > 1:
        raise RequestFatal(500)
    note = note[0]
    if note.activated:
        raise RequestWarning(208, 'Already activated')
    if note.refresh_token != data["token"]:
        raise RequestFatal(404, 'Wrong token')

    note.activated = True
    note.refresh_token = secrets.token_urlsafe(32)
    note.access_token = secrets.token_urlsafe(20)
    note.save()

def get_tokens(data):
    note = Users.objects.filter(
        email=data["email"],
    )

    if not note.exists():
        raise RequestFatal(404, 'User not found')
    if note.count() > 1:
        raise RequestFatal(500)
    note = note[0]
    if note.password != data["password"]:
        raise RequestFatal(400, 'Wrong password')
    if not note.activated:
        raise RequestFatal(400, 'Account not activated')

    note.refresh_token = secrets.token_urlsafe(32)
    note.access_token = secrets.token_urlsafe(20)
    note.save()
    return note.access_token, note.refresh_token

def update_access_token(token):
    note = Users.objects.filter(
        refresh_token=token,
    )

    if not note.exists():
        raise RequestFatal(404, 'Token not found')
    if note.count() > 1:
        raise RequestFatal(500)
    note = note[0]
    if not note.activated:
        raise RequestFatal(400, 'Account not activated')

    note.refresh_token = secrets.token_urlsafe(32)
    note.access_token = secrets.token_urlsafe(20)
    note.save()
    return note.access_token, note.refresh_token


def validate(token):
    note = Users.objects.filter(
        access_token=token,
    )

    if not note.exists():
        raise RequestFatal(404, 'Token not found')
    if note.count() > 1:
        raise RequestFatal(500)
    note = note[0]
    if not note.activated:
        raise RequestFatal(400, 'Account not activated')
    if note.time_modified.replace(tzinfo=None) <= datetime.datetime.now() - datetime.timedelta(hours=2):
        raise RequestFatal(401, 'Old token')
    return note.email


@access_and_errors
def registration(request):
    if request.method != "POST":
        raise RequestFatal(400, "expected POST request")
    data = parse_data(request, ["email", "password"])
    add_user(data)
    return "{}, account was successfully created"


@access_and_errors
def activation(request):
    if request.method != "GET":
        raise RequestFatal(400, "expected GET request")
    data = parse_data(request, ["email", "token"])
    activate(data)
    return '{}, your account successfully activated'.format(data["email"])


@access_and_errors
def authorization(request):
    if request.method != "POST":
        raise RequestFatal(400, "expected POST request")
    data = parse_data(request, ["email", "password"])
    access, refresh = get_tokens(data)
    return {"access_token": access,
            "refresh_token": refresh}


@access_and_errors
def update_token(request):
    if request.method != "POST":
        raise RequestFatal(400, "expected POST request")
    data = parse_data(request, ["refresh_token"])
    access, refresh = update_access_token(data["refresh_token"])
    return {"access_token": access,
            "refresh_token": refresh}


@access_and_errors
def validation(request):
    if request.method != "POST":
        raise RequestFatal(400, "expected POST request")
    data = parse_data(request, ["token"])
    email = validate(data["token"])
    return {"email": email}
