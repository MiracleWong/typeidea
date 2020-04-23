from datetime import datetime, date
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Tag, Category
from config.models import SideBar
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.db.models import Q, F
from django.core.cache import cache
from comment.forms import CommentForm
from comment.models import Comment


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
                category = Category.objects.get(id=category_id)
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


class CommonViewMiXin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


class PostDetailView(CommonViewMiXin, DetailView):
    queryset = Post.latest_pots()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    # TODO 这里书上为post_id , 出现错误，改为pk 后正常
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'comment_form': CommentForm,
            'comment_list': Comment.get_by_target(self.request.path)
        })
        return context

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False

        uid = self.request.uid

        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)

        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60)  # 1分钟有效

        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24 * 60 * 60)  # 1分钟有效

        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        else:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)


class PostListlView(ListView):
    queryset = Post.latest_pots()
    paginate_by = 1
    context_object_name = 'post_list'  # 如果不设置此项，在模板中需要使用object_list 变量
    template_name = 'blog/list.html'


class IndexView(CommonViewMiXin, ListView):
    queryset = Post.latest_pots()
    paginate_by = 5
    context_object_name = 'post_list'  # 如果不设置此项，在模板中需要使用object_list 变量
    template_name = 'blog/list.html'


class CategoryView(IndexView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """重写queryset，根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Category, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """重写queryset，根据分类过滤"""
        queryset = super.get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super(SearchView, self).get_queryset()
        keyword = self.request.GET.get('keyword')

        if not keyword:
            return queryset

        return queryset.filter(Q(title__icontains=keyword) | Q(title__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super(AuthorView, self).get_queryset()
        author_id = self.kwargs.get('owner_id')

        return queryset.filter(owner_id=author_id)