from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm, RegistrationForm, UserProfileForm, UserForm, UserInfoForm
from .models import UserProfile


def user_login(request):
    # If POST Validate data, if GET, send a login page
    if request.method == 'POST':
        # Get POST data from frontend
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # cleaned_data will return valid data as a dict, ignore invalid property
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user:
                login(request, user)
                return HttpResponse("Hello! Login Successfully!")
            else:
                return HttpResponse("Sorry, username or password is wrong")
        else:
            return HttpResponse("Invalid login")

    if request.method == 'GET':
        # Create a empty login form
        login_form = LoginForm()
        return render(request, "account/login.html", {"form": login_form})


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)

        if user_form.is_valid()*userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            # Save user_id in table account_userinfo
            UserInfo.objects.create(user=new_user)

            return HttpResponseRedirect('/account/login')
        else:
            return HttpResponse("Sorry, failed to register")
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, 'account/register.html', {"form": user_form,
                                                         'profile': userprofile_form})


@login_required(login_url='/account/login/')
def myself(request):

    userprofile = UserProfile.objects.get(user=request.user) if hasattr(request.user, 'userprofile') \
        else UserProfile.objects.create(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user)if hasattr(request.user, 'userinfo') \
        else UserInfo.objects.create(user=request.user)

    return render(request, 'account/myself.html', {"user": request.user,
                                                   "userinfo": userinfo, "userprofile": userprofile})


@login_required(login_url='/account/login/')
def myself_edit(request):
    userprofile = UserProfile.objects.get(user=request.user) if hasattr(request.user, 'userprofile') \
        else UserProfile.objects.create(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) if hasattr(request.user, 'userinfo') \
        else UserInfo.objects.create(user=request.user)

    if request.method == 'POST':
        print('Coming')
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        print(userprofile_form)
        print(userprofile_form.is_valid())
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            print('coming')
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            request.user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            print(userprofile_cd['phone'])
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.about = userinfo_cd['about']
            request.user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth": userprofile.birth,
                                                    "phone": userprofile.phone})
        userinfo_form = UserInfoForm(initial={"school": userinfo.school,
                                              "company": userinfo.company,
                                              "profession": userinfo.profession,
                                              "about": userinfo.about,
                                              "address": userinfo.address})

        return render(request, "account/myself_edit.html", {"user_form": user_form,
                                                            "userprofile_form": userprofile_form,
                                                            "userinfo_form": userinfo_form})


from .models import UserInfo


@login_required(login_url='/account/login/')
def my_image(request):
    if request.method == 'POST':
        img = request.POST['img']
        userinfo = UserInfo.objects.get(user=request.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request, 'account/image_crop.html',)
