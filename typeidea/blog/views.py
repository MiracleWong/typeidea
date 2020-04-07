from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Tag, Category
from config.models import SideBar


# Create your views here.

# post_list 的逻辑是：从Model从数据库中批量拿取数据，然后把标题和摘要展示到页面上。
def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None

    if tag_id:
        # try……except：如果查询到不存在的对象，需要捕获并处理异常，避免当数据不存在时出现错误
        try:
            # tag 和 post 是多对多的关系，需要先获取tag对象，接着通过对象来获取对应的文章列表
            tag = Tag.objects.get(id=tag_id)
        except tag.DoesNotExist:
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
    else:
        # 逻辑如下：先取出状态正常的所有的Post的集合，在从其中过滤出指定id的Post。
        # 而不是先过滤出指定id的Post，再看文章状态是否正常。
        post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
        if category_id:
            try:
                category = Category.objects.get(id = category_id)
            except Category.DoesNotExist:
                category = None
            else:
                post_list = post_list.filter(category_id=category_id)

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    # 进行数据回传的时候，要注意context中的内容，不要把后面的加上''，成为'post_list'
    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id=None):
    try:
        # 通过id获取指定的Post文章
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None

    context = {
        'post': post,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)
