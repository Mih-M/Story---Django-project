import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify

from story_app.forms import StoryForm, CommentForm
from story_app.models import Story
from story_auth.models import Writer
from story_common.decorators import group_required


def home(request):
    latest_stories = Story.objects.filter(published=True).order_by('-date')[:3]
    context = {
        'latest_stories': latest_stories,
    }
    return render(request, 'index.html', context)


def all_stories(request):
    stories = Story.objects.filter(published=True).order_by('-date')
    categories = [' '.join(cat[1].split('-')).capitalize() for cat in Story.CATEGORY_CHOICES]
    writers = Writer.objects.filter(approved=True).order_by('user_profile__user__first_name')

    context = {
        'stories': stories,
        'categories': categories,
        'writers': writers,
    }
    return render(request, 'all_stories.html', context)


@login_required()
def custom_stories(request, username, request_stories):
    user = request.user
    user_profile = user.userprofile
    is_writer = user.groups.filter(name='Writer').exists()

    if is_writer:
        if request_stories == 'my-stories':
            stories = user_profile.writer.story_set.filter(published=True).order_by('-date')
            header = 'My stories'
        elif request_stories == 'unpublished-stories':
            stories = user_profile.writer.story_set.filter(published=False).order_by('-date')
            header = 'My stories - unpublished'
    if request_stories == 'favorite-stories':
        stories = ''
        header = 'Favorite stories'

    categories = [' '.join(cat.split('-')).capitalize() for cat in [s.get_category_display() for s in stories]]
    writers = set(s.writer for s in stories)

    context = {
        'stories': stories,
        'header': header,
        'categories': categories,
        'writers': writers,
    }
    return render(request, 'custom_stories.html', context)


def story_details(request, pk, story_title):
    story = Story.objects.get(pk=pk)
    is_published = story.published
    is_owner = story.writer.user_profile == request.user.userprofile if request.user.is_authenticated else False

    if not is_published and not (is_owner or request.user.is_superuser):
        return redirect('home')

    paragraphs = story.content.split('\n')

    context = {
        'story': story,
        'paragraphs': paragraphs,
        'is_published': is_published,
        'is_owner': is_owner,
        'comment_form': CommentForm(),
        'comments': story.comment_set.all(),
    }
    return render(request, 'story_details.html', context)


def writers_profile(request, pk, writers_name):
    writer = Writer.objects.get(pk=pk)
    stories = writer.story_set.all()

    context = {
        'writer': writer,
        'stories': stories,
    }

    return render(request, 'writers_profile.html', context)


@group_required(['Writer'])
def add_story(request):
    if request.method == 'GET':
        context = {
            'story_form': StoryForm(),
        }

        return render(request, 'add_story.html', context)
    else:
        story_form = StoryForm(request.POST, request.FILES)

        if story_form.is_valid():
            story = story_form.save(commit=False)
            story.writer = request.user.userprofile.writer
            story.save()

            return redirect('profile', request.user.username)

        context = {
            'story_form': story_form,
        }

        return render(request, 'add_story.html', context)


@group_required(['Writer'])
def edit_story(request, story_pk, story_title):
    story = Story.objects.get(pk=story_pk)

    if request.user.userprofile != story.writer.user_profile and not request.user.is_superuser:
        redirect('home')

    if request.method == 'GET':
        context = {
            'story_form': StoryForm(instance=story),
            'story': story,
        }

        return render(request, 'edit_story.html', context)
    else:
        old_photo = story.image
        story_form = StoryForm(request.POST, request.FILES, instance=story)

        if story_form.is_valid():
            if story_form.cleaned_data['image'] != old_photo:
                os.remove(old_photo.path)
            story_form.save()
            story.published = False
            story.save()

            return redirect('story_details', story.id, slugify(story.title))

        context = {
            'story_form': story_form,
            'story': story,
        }

        return render(request, 'edit_story.html', context)


@group_required(['Writer'])
def delete_story(request, story_pk, story_title):
    story = Story.objects.get(pk=story_pk)

    if request.user.userprofile != story.writer.user_profile and not request.user.is_superuser:
        redirect('home')

    if request.method == 'GET':
        context = {
            'story': story,
        }

        return render(request, 'delete_story.html', context)
    else:
        story.delete()

        return redirect('profile', request.user.username)


@group_required()
def approve_story(request, story_pk):
    if request.method == 'POST':
        story = Story.objects.get(pk=story_pk)
        story.published = True
        story.save()

        return redirect('su_profile')


@login_required()
def add_comment(request, story_pk):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        story = Story.objects.get(pk=story_pk)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.story = story
            comment.author = request.user.userprofile
            comment.save()

            return redirect('story_details', story_pk, slugify(story.title))

        context = {
            'comment_form': comment_form,
        }
        return render(request, 'story_details.html', context)
