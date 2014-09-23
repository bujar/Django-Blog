from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, render_to_response
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from blog.models import *

# used for confirmation email
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from mimetypes import guess_type
from django.http import HttpResponse, Http404


def index(request):
    # Sets up list of just the logged-in user's (request.user's) items
    if request.user.is_authenticated():
        context = sidebar(request)
        return render(request, 'blog/index.html', context)
    else:
        users = userList.objects.all()
        return render(request, 'blog/index.html', {'users' : users})

def sidebar(request):
    items = []
    items_t = list(followList.objects.filter(username=request.user.username))
    i=0
    for item in items_t:    #iterate through each follows for this user
        items.extend(list(blogPost.objects.filter(username=items_t[i])))
        i += 1
    items.sort(key=lambda r: r.created, reverse=True )

    #items = list(userList.objects.filter(username=request.user))
    users = userList.objects.all().exclude(username__in=items_t)
    del items_t[0]  #first index got filled with null, need to deletes
    context = {'items' : items, 'users' : users, 'following': items_t}
    return context;

def getUserList(request):
    if request.user.is_authenticated():
        context = sidebar(request)
        return render(request, 'blog/users.xml', context, content_type='application/xml');    
    else:
        context = {'users':userList.objects.all()}
        return render(request, 'blog/users.xml', context, content_type='application/xml');
    
@login_required
def manage(request):
    items = []
    items_t = list(followList.objects.filter(username=request.user.username))
    i=0
    items = blogPost.objects.filter(username=request.user.username).order_by('-created')
    #items = list(userList.objects.filter(username=request.user))
    users = userList.objects.all().exclude(username__in=items_t)
    del items_t[0]  #first index got filled with null, need to deletes
    context = {'items' : items, 'users' : users, 'following': items_t}
    return render(request, 'blog/manage.html', context)


def view_blog(request, username):
    # Sets up list of just the logged-in user's (request.user's) items
    print(username)
    print(request.user.username)
    items=[]
    if request.user.is_authenticated():
        #items_t = list(followList.objects.filter(username=request.user.username))    #get all for cur user, temporary

        if not followList.objects.filter(username=request.user.username, follows=username):     
            new_item = followList(username=request.user.username, follows=username)    #if no, create
            new_item.save()
            context = sidebar(request)
        else:
            followList.objects.filter(username=request.user.username, follows=username).delete()  # if exists, delete
            context = sidebar(request)
        return render(request, 'blog/index.html', context)


    else:
        items = list(blogPost.objects.filter(username=username).order_by('-created'))
        if not items:
            items=''

        users = userList.objects.all()
        return render(request, 'blog/view_blog.html', {'items' : items, 'users' : users})

@login_required
def add_item(request):
    errors = []

    # Creates a new item if it is present as a parameter in the request
    if not 'item' in request.POST or not request.POST['item']:
       errors.append('You must enter an item to add.')
    else:
        if 'picture' in request.FILES:
            new_item = blogPost(text=request.POST['item'], username=request.user.username, title=request.POST["title"], picture=request.FILES['picture'])
        else:
            new_item = blogPost(text=request.POST['item'], username=request.user.username, title=request.POST["title"])
    new_item.save()

    items = []
    items_t = list(followList.objects.filter(username=request.user.username))
    i=0
    items = blogPost.objects.filter(username=request.user.username).order_by('-created')
    #items = list(userList.objects.filter(username=request.user))
    users = userList.objects.all().exclude(username__in=items_t)
    del items_t[0]  #first index got filled with null, need to deletes
    context = {'items' : items, 'users' : users, 'following': items_t}
    return render(request, 'blog/manage.html', context)

    context = {'items' : items, 'errors' : errors}
    return render(request, 'blog/manage.html', context)

@login_required    
def delete_item(request, item_id):
    errors = []

    # Deletes the item if present in the todo-list database.
    try:
        item_to_delete = blogPost.objects.get(id=item_id)
        item_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The item did not exist.')

    items = []
    items_t = list(followList.objects.filter(username=request.user.username))
    i=0
    items = blogPost.objects.filter(username=request.user.username).order_by('-created')
    #items = list(userList.objects.filter(username=request.user))
    users = userList.objects.all().exclude(username__in=items_t)
    del items_t[0]  #first index got filled with null, need to deletes
    context = {'items' : items, 'users' : users, 'following': items_t, 'errors': errors}
    return render(request, 'blog/manage.html', context)

def register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        return render(request, 'blog/register.html', context)

    errors = []
    context['errors'] = errors

    # Checks the validity of the form data
    if not 'username' in request.POST or not request.POST['username']:
	errors.append('Username is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
	context['username'] = request.POST['username']

    if not 'password1' in request.POST or not request.POST['password1']:
	errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
	errors.append('Confirm password is required.')

    if 'password1' in request.POST and 'password2' in request.POST \
       and request.POST['password1'] and request.POST['password2'] \
       and request.POST['password1'] != request.POST['password2']:
	errors.append('Passwords did not match.')

    if len(User.objects.filter(username = request.POST['username'])) > 0:
	errors.append('Username is already taken.')

    if errors:
        return render(request, 'blog/register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'], \
                                        password=request.POST['password1'], \
                                        email=request.POST['email'])

    new_user.is_active = False	#not able to login until account confirmation
    new_user.first_name = request.POST['fName']
    new_user.last_name = request.POST['lName']
    new_user.save()

     # Send an email with the confirmation link  
    token = default_token_generator.make_token(new_user)
    build_user = Author(user = new_user, token=token)
    build_user.save()
    add_user = userList(username=request.POST['username'])
    add_user.save()
    add_follow = followList(username=request.POST['username'])
    add_follow.save()
    email_subject = 'Your new example.com account confirmation'
    email_body = """
    	Hello %s %s! Thanks for signing up for an account. Before you start using our wonderful services,
    	you first need to activate your account. To do so, please click this link and log in to your new 
    	account: localhost:8000/blog/confirm/%s""" % \
    			(new_user.first_name, new_user.last_name, token)
    send_mail(email_subject,
        email_body,
       'btagani@cmu.edu',
        [new_user.email])
    return render(request, 'blog/needs-confirmation.html', context)


def confirm(request, token):
	#if token does not exist in database, return 404. if it does, grab that object and store into profile
	profile = get_object_or_404(Author, token=token)
	profile.user.is_active=True
	profile.user.save()


	print(profile.user.password)
	print(profile.user.username)

	#new_user = authenticate(username=profile.user.username,password=profile.user.password)
	#login(request, new_user)
	return redirect('/blog/login')


def photo(request, item_id):
    item = get_object_or_404(blogPost, id=item_id)
    if not item.picture:
        raise Http404

    content_type = guess_type(item.picture.name)
    print(content_type)
    return HttpResponse(item.picture.read(), content_type=content_type)