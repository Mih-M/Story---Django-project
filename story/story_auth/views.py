import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db import transaction
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify

from story_app.models import Story
from story_auth.forms import SignUpForm, SignInForm, BecomeAWriterForm, EditProfileWriterForm, EditProfileUserForm
from story_auth.models import UserProfile, Writer
from story_core.decorators import group_required


@transaction.atomic()
def sign_up(request):
    if request.method == 'GET':
        context = {
            'sign_up_form': SignUpForm()
        }

        return render(request, 'sign_up.html', context)
    else:
        sign_up_form = SignUpForm(request.POST)

        if sign_up_form.is_valid():
            user = sign_up_form.save()
            user_profile = UserProfile(user=user)
            user_profile.save()

            return render(request, 'welcome_to_story.html')

        context = {
            'sign_up_form': sign_up_form,
        }

        return render(request, 'sign_up.html', context)


def sign_in(request):
    if request.method == 'GET':
        context = {
            'sign_in_form': SignInForm(),
        }

        return render(request, 'sign_in.html', context)
    else:
        sign_in_form = SignInForm(request.POST)

        if sign_in_form.is_valid():
            username = sign_in_form.cleaned_data['username']
            password = sign_in_form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('home')

            context = {
                'sign_in_form': sign_in_form,
                'error_message': 'Username or password is incorrect',
            }

            return render(request, 'sign_in.html', context)


def sign_out(request):
    logout(request)
    return redirect('home')


@login_required()
def profile(request, username):
    user = request.user
    user_profile = user.userprofile
    is_writer = user.groups.filter(name='Writer').exists()

    my_stories = user_profile.writer.story_set.filter(published=True).order_by('-date', '-id')[:3] if is_writer else ''
    unpublished_stories = user_profile.writer.story_set.filter(published=False).order_by('-date', '-id')[:3] \
        if is_writer else ''
    favorite_stories = user_profile.favorites.filter(published=True).order_by('-date', '-id')[:3]

    context = {
        'user_profile': user_profile,
        'is_writer': is_writer,
        'my_stories': my_stories,
        'unpublished_stories': unpublished_stories,
        'favorite_stories': favorite_stories,
    }

    return render(request, 'profile.html', context)


@transaction.atomic()
@login_required()
def edit_profile(request, username):
    is_writer = request.user.groups.filter(name='Writer').exists()

    if request.method == 'GET':
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

        if is_writer:
            initial['description'] = request.user.userprofile.writer.description
            form = EditProfileWriterForm(initial=initial)
        else:
            form = EditProfileUserForm(initial=initial)

        context = {
            'form': form,
            'is_writer': is_writer,
        }

        return render(request, 'edit_profile.html', context)
    else:
        old_picture = request.user.userprofile.profile_picture

        if is_writer:
            form = EditProfileWriterForm(request.POST, request.FILES)
        else:
            form = EditProfileUserForm(request.POST, request.FILES)

        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()

            if is_writer:
                request.user.userprofile.writer.description = form.cleaned_data['description']
                request.user.userprofile.writer.save()

            if form.cleaned_data['picture']:
                request.user.userprofile.profile_picture = form.cleaned_data['picture']
                request.user.userprofile.save()
                if old_picture:
                    os.remove(old_picture.path)

            return redirect('profile', slugify(request.user.username))

        context = {
            'form': form,
        }

        return render(request, 'edit_profile.html', context)


@login_required()
def delete_profile(request, username):
    if request.method == 'GET':
        return render(request, 'delete_profile.html')
    else:
        profile_picture = request.user.userprofile.profile_picture

        if profile_picture:
            os.remove(profile_picture.path)

        request.user.delete()
        return redirect('home')


@group_required()
def su_profile(request):
    new_stories = Story.objects.filter(published=False).order_by('-date', '-id')
    new_writers = Writer.objects.filter(approved=False)

    context = {
        'new_stories': new_stories,
        'new_writers': new_writers,
    }

    return render(request, 'su_profile.html', context)


@transaction.atomic()
@login_required
def become_a_writer(request):
    if request.method == 'GET':
        if hasattr(request.user.userprofile, 'writer'):
            return render(request, 'application_submitted.html')
        else:
            application_form = BecomeAWriterForm(initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            })

            context = {
                'application_form': application_form,
            }

            return render(request, 'become_a_writer.html', context)
    else:
        user = request.user
        user_profile = user.userprofile
        application_form = BecomeAWriterForm(request.POST, request.FILES)

        if application_form.is_valid():
            writer = Writer(user_profile=user_profile)
            writer.save()
            user.first_name = application_form.cleaned_data['first_name']
            user.last_name = application_form.cleaned_data['last_name']
            user.save()
            if application_form.cleaned_data['picture']:
                user_profile.profile_picture = application_form.cleaned_data['picture']
                user_profile.save()

            return render(request, 'application_submitted.html')

        context = {
            'application_form': application_form,
        }

        return render(request, 'become_a_writer.html', context)


@group_required()
def approve_writer(request, writer_pk):
    if request.method == 'POST':
        writer = Writer.objects.get(pk=writer_pk)
        writer.approved = True
        writer.save()

        group = Group.objects.get(name='Writer')

        user = writer.user_profile.user
        user.groups.add(group)
        user.save()

        return redirect('su_profile')
