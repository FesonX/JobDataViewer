# coding=utf-8
from django import template
from django.db.models import Count
from article.models import ArticlePost

register = template.Library()


@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()


@register.simple_tag
def author_total_articles(user):
    return user.article.count()


@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n=5):
    articles = ArticlePost.objects.order_by("-created")[:n]
    return {"latest_articles": articles}


@register.simple_tag
def most_commented_articles(n=3):
    # get total comments in each article and set as its annotate
    return ArticlePost.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:n]
