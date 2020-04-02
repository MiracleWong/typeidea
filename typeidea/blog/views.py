from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Tag, Category


# Create your views here.


# def post_list(request, category_id=None, tag_id=None):
#     if tag_id:
#         print("tag_id:"+tag_id)
#         try:
#             tag = Tag.objects.get(id=tag_id)
#             # print("tag:"+tag)
#         except tag.DoesNotExist:
#             post_list = []
#         else:
#             post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
#     else:
#         post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
#         if category_id:
#             post_list = post_list.filter(category_id=category_id)
#
#     return render(request, 'blog/list.html', context={'post_list': 'post_list'})
#
#
# def post_detail(request, post_id=None):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#     return render(request, 'blog/detail.html', context={'post': 'post'})
def post_list(request, category_id=None, tag_id=None):
    queryset = Post.objects.all()
    if category_id:
        # 分类页面
        queryset = queryset.filter(category_id=category_id)
    elif tag_id:
        # 标签页面
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            queryset = []
        else:
            queryset = tag.posts.all()

    context = {
        'posts': queryset,
    }
    return render(request, 'blog/list.html', context=context)


def post_detail(request, pk=None):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        post = None

    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context=context)