from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import ArticleColumn, ArticlePost, ArticleTag
from .forms import ArticleColumnForm, ArticlePostForm, ArticleTagForm

import json


@login_required(login_url='/account/login')
@csrf_exempt
def article_column(request):
    if request.method == 'GET':
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request, "article/column/article_column.html", {"columns": columns,
                                                                      'column_form': column_form})

    if request.method == 'POST':
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id,
                                               column=column_name)
        if columns:
            # Duplicate Entry, refuse create
            return HttpResponse("2")
        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse("1")


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST['column_name']
    column_id = request.POST['column_id']
    try:
        result = ArticleColumn.objects.get(id=column_id)
        result.column = column_name
        result.save()
        return HttpResponse("1")
    except:
        return HttpResponse('0')


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article_column(request):
    column_id = request.POST['column_id']
    try:
        result = ArticleColumn.objects.get(id=column_id)
        result.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                tags = request.POST['tags']
                if tags:
                    for _tag in json.loads(tags):
                        _tag = request.user.tag.get(tag=_tag)
                        new_article.article_tag.add(_tag)
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        article_tags = request.user.tag.all()
        return render(request, "article/column/article_post.html", {"article_post_form": article_post_form,
                                                                    "article_columns": article_columns,
                                                                    "article_tags": article_tags})


@login_required(login_url='/account/login/')
def article_list(request):
    articles = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(articles, 4)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles_list = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles_list = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles_list = current_page.object_list
    return render(request, "article/column/article_list.html", {"articles": articles_list,
                                                                'page': current_page})


@login_required(login_url='/account/login/')
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    article_tags = request.user.tag.all()
    return render(request, "article/column/article_detail.html", {"article": article,
                                                                  "article_tags": article_tags})


@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def del_article(request):
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='/account/login/')
@csrf_exempt
def edit_article(request, article_id):
    if request.method == 'GET':
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=article_id)
        this_article_form = ArticlePostForm(initial={"title": article.title})
        this_article_column = article.column
        article_tags = request.user.tag.all()

        return render(request, "article/column/edit_article.html",
                      {"article": article, "article_columns": article_columns,
                       "this_article_column": this_article_column,
                       "this_article_form": this_article_form,
                       "article_tags": article_tags})
    else:
        re_article = ArticlePost.objects.get(id=article_id)
        try:
            re_article.column = request.user.article_column.get(id=request.POST['column_id'])
            re_article.title = request.POST['title']
            re_article.body = request.POST['body']
            tags = request.POST['tags']
            if tags:
                for _tag in json.loads(tags):
                    _tag = request.user.tag.get(tag=_tag)
                    re_article.article_tag.add(_tag)
            re_article.save()
            return HttpResponse("1")
        except:
            return HttpResponse("2")


@login_required(login_url='/account/login')
@csrf_exempt
def article_tag(request):
    if request.method == 'GET':
        tags = ArticleTag.objects.filter(author=request.user)
        tag_form = ArticleTagForm()
        return render(request, "article/tag/tag_list.html", {"article_tags": tags, "article_tag_form": tag_form})

    if request.method == 'POST':
        tag_form = ArticleTagForm(data=request.POST)
        if tag_form.is_valid():
            try:
                new_tag = tag_form.save(commit=False)
                new_tag.author = request.user
                new_tag.save()
                return HttpResponse("1")
            except:
                return HttpResponse("Failed to save data.")
        else:
            return HttpResponse("Invalid Form")


@login_required(login_url='/account/login')
@csrf_exempt
def del_article_tag(request):
    tag_id = request.POST['tag_id']
    try:
        tag = ArticleTag.objects.get(id=tag_id)
        tag.delete()
        return HttpResponse("1")
    except:
        pass
    return HttpResponse("2")
