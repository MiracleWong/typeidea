
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    """

    django 要求模型必须继承 models.Model 类。
    当然自己也可以写一个继承自 models.Model 的基类
    Category 需要分类名 name、状态 status 、是否为导航 is_nav、作者（拥有者） owner
    Category类，还有一个列 id，虽然没有显示定义，但 django 会为我们自动创建，这是一个自增类型。
    django 内置的全部类型可查看文档：
    https://docs.djangoproject.com/zh-hans/3.0/ref/models/fields/#field-types
    PS：因为Model内部的字段几乎没有修改，所以虽然我们用的django 是1.11.29版本，上面链接给的是3.0 的文档，也是Ok的。
    https://blog.csdn.net/weixin_30402085/article/details/99607736
    """

    """
    django 内置的全部参数可查看：
    https://docs.djangoproject.com/zh-hans/3.0/ref/models/fields/#field-options
    1、null：如果是True，Django会在数据库中将此字段的值置为NULL，默认值是False
    2、blank：针对业务层面：如果为True时，django的 Admin 中添加数据时可允许空值，可以不填。如果为False则必须填。默认是False。NULL纯粹是与数据库有关系的。而blank是与页面必填项验证有关的
    3、primary_key = False：主键，对AutoField设置主键后，就会代替原来的自增 id 列
    4、auto_now：自动创建---无论添加或修改，都是当前操作的时间
    5、auto_now_add：自动创建---永远是创建时的时间
    5、choices： 一个二维的元组被用作choices，如果这样定义，Django会select box代替普通的文本框，并且限定choices的值是元组中的值
    6、max_length：字段长度
    7、default：默认值
    8、verbose_name：Admin中字段的显示名称，如果不设置该参数时，则与属性名。
    9、db_column：数据库中的字段名称
    10、unique：唯一约束，需要配置时，设置为unique=True，设置后，不需要再设置db_index
    11、db_index：数据库索引
    12、editable： 在Admin里是否可编辑。默认为True。不需要可配置为false
    13、error_messages=None：错误提示
    14、auto_created=False：自动创建
    15、help_text：在Admin中提示帮助信息
    16、validators：自定义校验逻辑
    17、upload-to：文件上传时的保存上传文件的目录
    18、unique_for_date：针对date的联合约束
    19、unique_for_month：针对月份的联合约束
    20、unique_for_year：针对年份的联合约束
    21、error_message: 用来自定义字段值校验失败时的异常提示。字典格式
    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    # CharField：字符型，max_length 参数指定其最大长度(必须设置)，超过这个长度的分类名就不能被存入数据库。该Category类中的name最大长度为 50
    name = models.CharField(max_length=50, verbose_name='名称')
    # PositiveIntegerField：正整数类型，范围：(0, 2147483647)
    # 一个二维的元组被用作choices，如果这样定义，Django会选择框select box代替普通的文本框（Text），填写该字段field
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name="状态")
    # BooleanField：允许为空的布尔类型，一般用于记录状态标记
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(User, verbose_name='作者')
    # DateTimeField：日期时间类型
    # DateTimeField.auto_now：保存时自动设置该字段为现在日期，最后修改日期
    # DateTimeField.auto_now_add：当该对象第一次被创建是自动设置该字段为现在日期，创建日期。
    # 参数同日期类型 DateField 一致
    created_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='创建时间')

    # 通过一个内嵌类 "class Meta" 给你的 model 定义元数据
    # Model 元数据就是 "不是一个字段的任何数据"
    # 参考地址：https://www.cnblogs.com/sui776265233/p/10670757.html
    class Meta:
        # verbose_name：给模型类起一个更可读的名字：
        # verbose_name_plural：指定模型的复数形式是什么，若是没有提供，
        verbose_name = verbose_name_plural = '分类'

    """
    __str__():方法是当print 输出实例对象或str() 实例对象时，调用这个方法
    TODO 可以测试__str__()和__unicode__()的区别
    """

    def __str__(self):
        return self.name


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name='名称')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    #
    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    # TextField 来存储大量文本内容，对应于MySQL中的logtext
    content = models.TextField(verbose_name='正文', help_text='正文必须为Markdown格式')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name='作者')
    category = models.ForeignKey(Category, verbose_name='分类')
    tag = models.ForeignKey(Tag, verbose_name='标签')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return '<Post>: {}>'.format(self.title)

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']  # 根据id进行降序排列 TODO: 哪里来的id