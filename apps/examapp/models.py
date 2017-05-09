from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z.-]+$')
PW_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')

class UserManager(models.Manager):
    def register(self, PostData):
        errors = []
        if len(PostData['name']) < 1 or len(PostData['email']) < 1 or len(PostData['password']) < 1:
            errors.append("Opps! something went wrong, Check your info!")
        if not EMAIL_REGEX.match(PostData['email']):
            errors.append("Invalid Email address")
        if not NAME_REGEX.match(PostData['name']):
            errors.append("Name only can contain letters!")
        if not PW_REGEX.match(PostData['password']):
            errors.append("password not strong!")
        if PostData['conf_password'] != PostData['password']:
            errors.append("password not match!")
        if User.objects.filter(email = PostData['email']):
            errors.append("User already exist!")
        return errors
    def create_user(self, PostData):
        hashed_pw = bcrypt.hashpw(PostData['password'].encode('utf-8'), bcrypt.gensalt())
        new_user = User.objects.create(name=PostData['name'], email=PostData['email'], password = hashed_pw)
        return new_user.id
    def login(self, PostData):
        errors = []
        if len(PostData['email']) < 1 or len(PostData['password']) < 1:
            errors.append("You forgot to enter your email/password")
        if not User.objects.filter(email=PostData['email']):
            errors.append('Invlaild User!')
        else:
            if bcrypt.hashpw(PostData['password'].encode('utf-8'), User.objects.get(email=PostData['email']).password.encode('utf-8')) != User.objects.get(email=PostData['email']).password:
                errors.append('incorrect user name or password')
        return errors
class QuoteManager(models.Manager):
    def validation(self, PostData):
        errors = []
        if len(PostData['quote']) < 1:
            errors.append("you got to type something.")
        if len(PostData['quoted_by']) < 1:
            errors.append('Quoted by who?')
        return errors

    def create_quote(self, PostData):
        quote = Quote.objects.create(content= PostData['quote'], quoted_by = PostData['quoted_by'], posted_by=PostData['added_by'])
        return quote.id
    def add_to_my_list(self, PostData):
        user = User.objects.get(id=PostData['user'])
        quote = Quote.objects.get(id=PostData['quote'])
        quote.fav_list.add(user)
class User(models.Model):
    name = models.CharField(max_length=225)
    email = models.CharField(max_length = 225)
    password = models.CharField(max_length = 225)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Quote(models.Model):
    content = models.TextField(max_length = 2000)
    quoted_by = models.CharField(max_length = 200)
    posted_by = models.ForeignKey(User)
    fav_list = models.ManyToManyField(User, related_name="quotes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = QuoteManager()


# Create your models here.
