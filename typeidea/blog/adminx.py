# Register your models here.
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
import xadmin
from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import manager, RelatedFieldListFilter
from .models import Post, Tag, Category
from typeidea.base_admin import BaseOwnerAdmin
from .adminforms import PostAdminForm


# 这是一个伪需求：6.2.5 在同一页面编辑关联数据
class PostInLine:
    form_layout = (
        Container(
            Row('title', 'desc')
        )
    )
    extra = 0  # 额外控制多少个
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInLine, ]
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.shot_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(RelatedFieldListFilter):
    """
    自定义过滤器，只展示当前用户的分类
    """

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super(CategoryOwnerFilter, self).__init__(field, request, params, model, model_admin, field_path)
        # 重新获取
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    # list_display 配置列表页面展示哪些字段
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator',
    ]

    # list_display 哪些字段，可以作为链接，点击进入编辑界面
    list_display_links = []

    list_filter = ['category']
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面

    save_on_top = False

    form_layout = (
        Fieldset('基础信息',
                 Row('category', 'title'),
                 'status',
                 'tag',
        ),
        Fieldset('内容信息',
                 'desc',
                 'content',
        )
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}"> 编辑  </a>',
            reverse('xadmin:blog_post_change', args=(obj.id,))
        )
    operator.shot_description = '操作'

    # @property
    # def media(self): # 因为会引起Bootstrap的样式冲突,注释
    #     media = super(PostAdmin, self).media()
    #     media.add_js(['https://cdn.bootcss.com/twitter-bootstrap/4.4.1/js/bootstrap.bundle.js'])
    #     media.add_css({'all': ('https://cdn.bootcss.com/twitter-bootstrap/4.4.1/css/bootstrap.min.css',),})
    #
    #     return media
