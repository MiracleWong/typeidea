from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Tag, Category


# Create your views here.

# post_list 的逻辑是：从Model从数据库中批量拿取数据，然后把标题和摘要展示到页面上。
def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None

    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        # 和书上不一致的地方，这里在源代码中没有使用latest_posts
        # post_list = Post.latest_posts(Post)
        post_list = Post.objects.filter(status=Post.STATUS_NORMAL)\
            .select_related('owner', 'category')

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
    }
    # 进行数据回传的时候，要注意context中的内容，不要把后面的加上''，成为'context'
    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id=None):
    try:
        # 通过id获取指定的Post文章
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    return render(request, 'blog/detail.html', context={'post': post})
