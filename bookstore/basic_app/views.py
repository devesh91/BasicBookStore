from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm,BookCatalogueForm,BookCatalogue
from basic_app.models import BookCatalogue
from django.http import HttpResponse



# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'basic_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'basic_app/login.html', {})

@login_required()
def bookcatalogue(request):
    book_list = BookCatalogue.objects.all()
    book_dict = {"book_records": book_list}
    return render(request, 'basic_app/bookcatalogue.html', context=book_dict)


def view_bookcatalogue(request):
    form = BookCatalogueForm()
    if request.method == 'POST':
        form = BookCatalogueForm(request.POST)

        if request.POST.getlist('book[]', True):
            Blist = request.POST.getlist('book[]')
            Qlist = request.POST.getlist('quantity[]')
            Price = request.POST.getlist('price[]')
            Qlist = list(map(int, Qlist))
            Price = list(map(int, Price))
            books = list(map(str, BookCatalogue.objects.all()))
            bookstring = ""
            Bill = 0

            counter=0
            for flag in Blist:
                for ind in range(len(books)):
                    if flag == books[ind]:
                        Bill = Qlist[counter]*Price[ind]+Bill
                        counter=counter + 1


            for i in Blist:
                bookstring=  i + "," + bookstring

            my_dict = {'booklist': bookstring,'totalbill':Bill}

            return render(request,'basic_app/bookcatalogue.html',context=my_dict)
    return render(request,'basic_app/bookcatalogue.html',{'form':form})






