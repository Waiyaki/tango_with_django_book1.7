from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login, logout
# from django.http import HttpResponseRedirect

from .models import Category, Page
from .forms import CategoryForm, PageForm

# from .forms import UserForm, UserProfileForm


def index(request):

    category_list = Category.objects.order_by("-likes")[:5]
    page_list = Page.objects.order_by('-views')[:5]
    page_list = [page for page in page_list if page.views != 0]
    context_dict = {'categories': category_list,
                    'pages': page_list
                    }

    visits = request.session.get('visits')
    if not visits:
        # 'visits' cookie doesn't exist, so set visits to 1
        visits = 1

    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:

        # cast the last visit time to a Python date/time object
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        # If it has been more than 1 day since the last visit...
        if(datetime.now() - last_visit_time).seconds > 5:
            visits = visits + 1

            # flag that the last visit time needs to be updated
            reset_last_visit_time = True
    else:
        # 'last_visit' cookie doesn't exist, flag that it should be set
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    context_dict['visits'] = visits
    response = render(request, 'rango/index.html', context_dict)

    # return the response back to the user
    return response


def about(request):
    visits = request.session.get('visits')
    if not visits:
        visits = 1
        request.session['visits'] = visits
    context_dict = {'visits': visits}
    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        context_dict['category_name_slug'] = category_name_slug

        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages

        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        # the request was not a post, show the form
        form = CategoryForm()

    # render the form with errors if any
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()

                # Update this to redirect() some time
                return category(request, category_name_slug)
        else:
            print(form.errors)
    else:
        form = PageForm()  # was not a post, so display the form

    context_dict = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)


"""
def register(request):
    # Was the registration successful? Initially False
    registered = False

    # If a POST, process the form
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # Validity checks...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the users form data to the database
            # Returns a user object
            user = user_form.save()

            # Hash and set the password
            user.set_password(user.password)
            user.save()

            # Sort out the UserProfileForm
            profile = profile_form.save(commit=False)

            # Make the link between a profile and its owner
            profile.user = user

            # If the user provided a profile picture, get it
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now save the UserProfile
            profile.save()

            # Registration successful.
            registered = True

        # Invalid form.
        # Print problems to the terminal, and show them to the user as well
        else:
            print(user_form.errors, profile_form.errors)

    # Not a http POST, so render the registration form
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context
    return render(request,
                  'rango/register.html',
                  {'user_form': user_form, 'profile_form': profile_form,
                   'registered': registered}
                  )


def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details
            print("Invalid login details: {} {}".format(username, password))
            return HttpResponse("Invalid login details.")
    else:
        # Not a http post, display the login form.
        return render(request, 'rango/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')
"""


@login_required
def restricted(request):
    return HttpResponse("Since you are logged in, you can see this.")
