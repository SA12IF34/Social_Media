from django.http import HttpRequest, HttpResponse
from django import forms
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.status import *
from .models import *
from .serializers import *
from .forms import *


# Cryptographic Functions

def make_password(password, user_id=25, user_name="helloworld"):

    alphabit = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z".split(",")
    numbers = "1,2,3,4,5,6,7,8,9,0".split(",")
    symbols = "!,@,#,$,&,*,%,(,),?,},[,{,],؟,~".split(",")
    rand_num_one = 67
    rand_num_two = 87
    ultra_num = rand_num_one + user_id
    length = len(user_name)

    if ultra_num > length:
        unique_num = ultra_num-length
        encrypted_password = ""

        for l in password.lower():
            if l in alphabit:
                i = alphabit.index(l)
                encrypted_password+= str(unique_num*i)+"-"

            if l in numbers :
                encrypted_password+= str(unique_num*int(l))+"N-"

            if l in symbols:
                i = symbols.index(l)
                encrypted_password+= str(unique_num*i)+"S-" 

        encrypted_password+= ""+ str(int(unique_num*rand_num_two))        
        
        return encrypted_password


def check_password(password, r_password):

    alphabit = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z".split(",")
    symbols = "!,@,#,$,&,*,%,(,),?,},[,{,],؟,~".split(",")
    split_v = r_password.split("-")
    rand_num = 87
    unique_num = int(int(split_v[-1])/rand_num)
    decrypted_password = ""
    i=0

    while i < len(split_v)-1:

        if split_v[i] == "0":
            decrypted_password+="a"
            i+=1
            continue

        elif split_v[i] == "0S":
            decrypted_password+="!"
            i+=1
            continue

        if split_v[i][-1] == "N":
            data = split_v[i].rstrip("N")
            decrypted_password += str(int(int(data)/unique_num))

        elif split_v[i][-1] == "S":
            data = split_v[i].rstrip("S")
            decrypted_password += symbols[int(int(data)/unique_num)]

        else:
            decrypted_password += alphabit[int(int(split_v[i])/unique_num)]

        i+=1
    
    if decrypted_password == password.lower():
        return True
    
    return False


# Accounts System

class AccountsView(APIView):

    def get(self, request, filter=False):
        
        objs = Account.objects.all()
        serializer = AccountsSerializer(objs, many=True)
        return Response(data=serializer.data, status=200)

    def post(self, request):
        
        id = len(Account.objects.all())+1

        request.data['password'] = make_password(request.data['password'], id, request.data['name'])
        serializer = AccountsSerializer(data=request.data)
        serializer2 = FollowSerializer(data={"name": request.data['name'], 
                                    "account_name": request.data['account_name'],
                                    "email": request.data['email']})
        
        if serializer.is_valid() and serializer2.is_valid():
            
            serializer.save()
            serializer2.save()

            request.session['data'] = {
                                        "account": serializer.data['account_name'],
                                        "username": serializer.data['name'],
                                        "email": serializer.data['email'],
                                      }
            request.session['hash'] = serializer.data['password'].split("-")[-1]
            response = Response(data=serializer.data, status=201)
            response.set_cookie("account", {"name": request.data['name'], 
                                    "account_name": request.data['account_name'],
                                    "email": request.data['email']})
            return response

@api_view(['POST', 'GET'])
def login(request):

    if request.method == "POST":
        account = Account.objects.filter(name=request.data['name'], email=request.data['email']).get()
        account_serializer = AccountsSerializer(instance=account)

        if check_password(request.data['password'], account_serializer.data['password']):
            
            request.session['data'] = {
                                        "account": account_serializer.data['account_name'],
                                        "username": account_serializer.data['name'],
                                        "email": account_serializer.data['email'],
                                      }
            request.session['hash'] = account_serializer.data['password'].split("-")[-1]

            return Response(data=request.session, status=HTTP_202_ACCEPTED)
        
        
        return Response(data={"shit0": "shit"}, status=202)
    
    if request.method == "GET":
        
        return Response(data={"hello": "shit"}, status=200)


@api_view(['GET', 'POST'])
def logout(request):
    
    if request.method == 'POST':
        
        if request.session.has_key("data") and request.session.has_key("hash"):
            del request.session['data']
            del request.session['hash']

            return Response(data=request.session ,status=202)
    
    return Response(data={"purpose": "LogOut"}, status=200)

    

@api_view(['GET'])
def linkers(request):

    linkers = Follow.objects.all()
    serializer = FollowSerializer(instance=linkers, many=True)

    return Response(data=serializer.data, status=200)


@api_view(['POST', 'GET'])
def follow(request):
    
    if request.method == 'POST':
        account = Follow.objects.get(account_name=request.data['account_name'])
        target_account = Account.objects.get(account_name=request.data['target_account'])

        account.follow_accounts.add(target_account)
        target_account.followers_accounts.add(account)
        target_account.followers_number += 1

        target_account.save()
        
        serializer = AccountsSerializer(instance=target_account)

        return Response(data=serializer.data, status=202)
    

    data = AccountsSerializer(instance=Account.objects.get(account_name="@saleem"))

    return Response(data={"hello": "world"}, status=200)


@api_view(['GET', 'POST'])
def unfollow(request):
    
    if request.method == 'POST':
        account = Follow.objects.get(account_name=request.data['account_name'])
        target_account = Account.objects.get(account_name=request.data['target_account'])
        
        account.follow_accounts.remove(target_account)
        target_account.followers_accounts.remove(account)
        target_account.followers_number -=1

        target_account.save()

        return Response(data={"consequance": "Done"}, status=202)
    
    return Response(data={"world": "hello"}, status=200)



# Single Account System

class AccountView(APIView):
    

    def get(self, request, account_name=False):
        
        account = Account.objects.get(account_name=account_name)
        serializer = AccountsSerializer(instance=account)

        return Response(data=serializer.data, status=200)

    def patch(self, request, account_name):
        
        account = Account.objects.get(account_name=account_name)
        serializer = AccountsSerializer(instance=account, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=202)

    def delete(self, request, account_name):
        
        Account.objects.get(account_name=account_name).delete()
        
        if request.session.has_key("data") and request.session.has_key("hash"):
            del request.session['data']
            del request.session['hash']

            return Response(data=request.session ,status=202)

        return Response(data={"purpose": "delete account"})


@api_view(['GET'])
def get_followers(request, account_name):

    account = Account.objects.get(account_name=account_name)
    followers = account.followers_accounts.all()

    serializer = FollowSerializer(instance=followers, many=True)

    return Response(data=serializer.data ,status=200)



# Posts System

class MyForm(forms.Form):
    desc= forms.CharField(max_length=150)
    file = forms.FileField()

class PostsView(APIView):



    def get(self, request):
        posts = Post.objects.all()
        serializer = PostsSerializer(instance=posts, many=True)
        return Response(data=serializer.data)
    
    def post(self, request):

        if request.session.has_key("hash"):
            # try:
            post = Post(desc=request.data['desc'], file=request.data['file'])
            account = Account.objects.get(account_name=request.session['data']['account'])
        
            post.author = account
            post.save()
            serializer = PostsSerializer(instance=post)
            return Response(data=serializer.data, status=202)
            # except BaseException as err:
            #     return Response(status=500)

        return Response(data={"detail": "You Are Not Authenticated"}, status=400)
 
class AccountPostsView(APIView):

    def get(self, request, owner):
        account = Account.objects.get(account_name=owner)
        posts = Post.objects.filter(author=account.id)
        serializer = PostsSerializer(instance=posts, many=True)

        return Response(data=serializer.data, status=200)


class PostView(APIView):
    def get(self, request, id):
        try:
            post = Post.objects.get(id=id)
            serializer = PostsSerializer(instance=post)

            return Response(data=serializer.data, status=200)
        except Post.DoesNotExist:
            
            return Response(status=204)
    
    def patch(self, request, id):
        post = Post.objects.get(id=id)
        serializer = PostsSerializer(instance=post, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=202)

    def delete(self, request, id):
        post = Post.objects.get(id=id)
        post.file.delete(save=False)
        post.delete()

        return Response(status=204)



# Comments System

class CommentsView(APIView):

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentsSerializer(instance=comments, many=True)

        return Response(data=serializer.data, status=200)

    def post(self, request):
        
        serializer = CommentsSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=201)

class PostCommentsView(APIView):

    def get(self, request, post):
        post = Post.objects.get(id=post)
        comments = Comment.objects.filter(post=post)
        serializer = CommentsSerializer(instance=comments, many=True)

        return Response(data=serializer.data, status=200)


class CommentView(APIView):

    def get(self, request, id):
        comment = Comment.objects.get(id=id)
        serializer = CommentsSerializer(instance=comment)

        return Response(data=serializer.data, status=200)

    def patch(self, request, id):
        comment = Comment.objects.get(id=id)
        serializer = CommentsSerializer(instance=comment, data=request.data, patrial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=202)

    def delete(self, request, id):
        Comment.objects.get(id=id).delete()

        return Response(status=202)
    

class AccountComment(APIView):

    def get(self, request, id):

        account = Account.objects.get(id=id)
        comments = Comment.objects.filter(account=account)
        account_serializer = AccountsSerializer(instance=account).data
        comments_serializer = CommentsSerializer(instance=comments, many=True).data

        data = {
            "account": account_serializer,
            "comments": comments_serializer
        }

        return Response(data=data, status=200)