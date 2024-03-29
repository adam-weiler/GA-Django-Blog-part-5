from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from blog.models import Article, Topic, Comment
from blog.forms import ArticleForm, CommentForm


def root(request): # Redirects to http://localhost:8000/articles
    return redirect(reverse("show_all"))


def show_all(request):  # Renders a list of all articles.
    context = { 'blog_articles': Article.objects.all().order_by('-published_date'), 'blog_topics': Topic.objects.all() } #The - in published_date means order from newest to oldest.
    return render(request, "articles.html", context)


def show_article(request, article_id):  # Renders a single article.
    article = Article.objects.get(pk=article_id)
    form = CommentForm()

    return render(request, 'article.html', {
        'article': article, 
        'form': form
    })


def new_article(request):  # Renders a form to create a new article.
    form = ArticleForm()

    return render(request, 'article_form.html', {
        'form': form
    })


def create_article(request):  # User creating a new article.
    form = ArticleForm(request.POST)

    if form.is_valid():
        form.save()
        return redirect(reverse('show_all'))
    else:  # Else sends user back to article_form page.
        return render(request, 'article_form.html', {
            'form': form
        })
        # return redirect(reverse('new_article')) #How do you reverse and attach a form..?


def create_comment(request, article_id):  # Renders a form to create a new comment.
    article = Article.objects.get(pk=article_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.article = article
        new_comment.save()
        return redirect(reverse('show_article', args=[article_id]))
    else:  # Else sends user back to article page.
        return render(request, 'article.html', {
            'article': article, 
            'form': form
        })

    