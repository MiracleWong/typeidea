from django.contrib import admin

# Register your models here.


from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .adminforms import PostAdminForm
from .models import Post, Tag, Category
from typeidea.custom_admin import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry


# 这是一个伪需求：6.2.5 在同一页面编辑关联数据
class PostInLine(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInLine, ]
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.shot_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """
    自定义过滤器，只展示当前用户的分类
    """

    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    # form = PostAdminForm
    # list_display 配置列表页面展示哪些字段
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator',
    ]

    # list_display 哪些字段，可以作为链接，点击进入编辑界面
    list_display_links = []

    list_filter = [CategoryOwnerFilter, ]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面

    save_on_top = False

    """
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )    
    """

    fieldsets = (
        ('基础配置', {
            # 'description': '基础配置描述',
            'fields': (
                ('category', 'title'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('wide',),
            'fields': ('tag',)
        }),
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}"> 编辑  </a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.shot_description = '操作'

    class Media:
        css = {
            'all': ('https://cdn.bootcss.com/twitter-bootstrap/4.4.1/css/bootstrap.min.css',),
        }
        js = ('https://cdn.bootcss.com/twitter-bootstrap/4.4.1/js/bootstrap.bundle.js',)


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = [
        'object_repr', 'object_id', 'action_flag',
        'user', 'change_message',
    ]