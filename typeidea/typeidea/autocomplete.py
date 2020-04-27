from dal import autocomplete
from blog.models import Category, Tag


class CategoryAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Category.objects.none()

        qs = Category.objects.filter(owner=self.request.user)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class TagAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # 首先判断用户是否登录，如果未登录直接返回空的queryset
        # 因为该值后面还会被其他的模块处理，所以不能返回None
        if not self.request.user.is_authenticated():
            return Tag.objects.none()

        # 获取该用户创建的所有标签
        qs = Tag.objects.filter(owner=self.request.user)

        # q是url传上来的值
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
