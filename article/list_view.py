from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .models import ArticlePost
from .forms import CommentForm
from django.conf import settings
from django.db.models import Count
import markdown
import redis


r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


@csrf_exempt
@require_POST
@login_required(login_url='/account/login/')
def like_article(request):
    article_id = request.POST.get('id')
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == "wow":
                article.wow.add(request.user)
                return HttpResponse("1")
            else:
                return HttpResponse("2")
        except:
            return HttpResponse("no")


def article_titles(request, username=None):
    if username:
        user = User.objects.get(username=username)
        articles_title = ArticlePost.objects.filter(author=user)
        try:
            user_info = user.userinfo
        except:
            user_info = None
    else:
        articles_title = ArticlePost.objects.all()

    paginator = Paginator(articles_title, 4)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list

    for article in articles:
        article.body = markdown.markdown(article.body)

    if username:
        return render(request, "article/list/author_articles.html", {"articles": articles,
                                                                    "page": current_page,
                                                                    "user_info": user_info,
                                                                    "user": user})
    return render(request, "article/list/article_titles.html", {"articles": articles,
                                                                "page": current_page})


def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    # plus one view and return total views
    total_views = r.incr("article:{}:views".format(article.id))
    # name, mount, value
    r.zincrby('article_ranking', 1, article.id)

    # get sorted set article_ranking's top10
    article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed_articles = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed_articles.sort(key=lambda x: article_ranking_ids.index(x.id))

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
    else:
        comment_form = CommentForm()

    article_tags = request.user.tag.all()
    article_tags_ids = article.article_tag.values_list("id", flat=True)
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count("article_tag")).\
        order_by('-same_tags', '-created')[:4]

    return render(request, "article/list/article_detail.html", {'article': article,
                                                                'total_views': total_views,
                                                                'most_viewed': most_viewed_articles,
                                                                'comment_form': comment_form,
                                                                "article_tags": article_tags,
                                                                "similar_articles": similar_articles})
