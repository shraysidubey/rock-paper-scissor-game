import random
from django.http import HttpResponse
from rps.forms import UserForm, UserProfileForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rps.models import UserProfile

def index(request):

    context_dict = {}
    try:
        if request.user.is_authenticated():
            user_profile = UserProfile.objects.get(user=request.user.id)
            context_dict['user'] = request.user
            context_dict['user_profile'] = user_profile


    except UserProfile.DoesNotExist:
        print("UserNot found")
        pass
    return render(request, 'rps/index.html', context_dict)


def register(request):
    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            print "succesfully saved the profile"

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'rps/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        #print "username", username
        password = request.POST.get('password')
        #print "password", password

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:

                login(request, user)
                return HttpResponseRedirect('/rps/')
            else:
                return HttpResponse("Your RPS GAME account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:

        return render(request, 'rps/login.html', {})

def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are logged in.")
    else:
        return HttpResponse("You are not logged in.")


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    return HttpResponseRedirect('/rps/')

def play_game(request, user_choice):
    cont_dict = {}
    user_choice = int(user_choice)
    comp_choice = random.randint(0,2)

    output_of_match = compare_choices(user_choice, comp_choice)
    print "output of match", output_of_match

    user_profile = UserProfile.objects.get(user=request.user.id)
    list_of_username = UserProfile.objects.all().order_by('-wins')[:10]
    cont_dict['list_of_username'] = list_of_username

    message = "you chose: " + options(user_choice) + ", Computer chose: " + options(comp_choice)
    if output_of_match == 1:
        message += " ,Woaahh you won!!"
    else:
        message += " ,Ooppss you lost!!"

    cont_dict['message'] = message

    cont_dict['user_profile'] = user_profile.user
    user_profile.matches = user_profile.matches + 1

    if output_of_match == 1:
        user_profile = UserProfile.objects.get(user=request.user.id)
        user_profile.wins = user_profile.wins + 1
        print "wins", user_profile.wins

    user_profile.save()
    cont_dict['user_profile'] = user_profile

    return render(request, 'rps/index.html', cont_dict)

'''
 0 - stone
 1 - paper
 2 - scissor    (0,1)(0,2)(1,0)(1,2)(2,0)(2,1)()()()
 return 1(user_win)
'''

def compare_choices(user_choice, comp_choice):
    if user_choice == 0 and comp_choice == 1:
        return 0
    elif user_choice == 0 and comp_choice == 2:
        return 1
    elif user_choice == 1 and comp_choice == 0:
        return 0
    elif user_choice == 1 and comp_choice == 2:
        return 1
    elif user_choice == 2 and comp_choice == 0:
        return 0
    elif user_choice == 2 and comp_choice == 1:
        return 1
    else:
        return 0

def options(user_choice):
    if user_choice == 0:
        return "stone"
    elif user_choice == 1:
        return "paper"
    elif user_choice == 2:
        return "scissor"