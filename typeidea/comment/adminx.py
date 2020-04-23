import xadmin
from .models import Comment
from typeidea.base_admin import BaseOwnerAdmin
# Register your models here.


@xadmin.sites.register(Comment)
class CommentAdmin(BaseOwnerAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')
