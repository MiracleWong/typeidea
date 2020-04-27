"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

import xadmin
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.sitemaps import views as sitemap_views
from blog.views import (
    PostDetailView, TagView, CategoryView,
    IndexView, SearchView, AuthorView
)
from comment.views import CommentView
from config.views import LinkListView
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from .autocomplete import CategoryAutoComplete, TagAutoComplete


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    # pk的意思是Primary Key，指的是id，但是 detail view 要求，必须使用的是pk
    url(r'^post/(?P<pk>\d+).html$', PostDetailView.as_view(), name='post-detail'),
    # 搜索页面
    url(r'^search/$', SearchView.as_view(), name='search'),
    # 作者页面
    url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name="author"),
    url(r'^links/$', LinkListView.as_view(), name='links'),
    url(r'^comment/$', CommentView.as_view(), name='comment'),
    url(r'^admin/', xadmin.site.urls, name='xadmin'),
    # RSS
    url(r'^rss|feed/', LatestPostFeed(), name='rss'),
    # Sitemap
    url(r'^sitemap\.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap }}),
    # 配置
    url(r'^category-autocomplete/$', CategoryAutoComplete.as_view(), name='category-autocomplete'),
    url(r'^tag-autocomplete/$', TagAutoComplete.as_view(), name='tag-autocomplete'),

    # 上传的图片
    url(r'^ckeditor/', include('ckeditor_uploader.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

