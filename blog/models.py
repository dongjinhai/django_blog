from django.db import models

# Create your models here.
class Articles(models.Model):
    title = models.CharField('标题',max_length=30)
    date = models.DateTimeField('文章创建日期',auto_now_add=True)
    content = models.TextField('内容')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'articles'

class Users(models.Model):
    name = models.CharField('名字',max_length=15)
    password = models.CharField('密码',max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'

class Comments(models.Model):
    article_id = models.IntegerField('文章的ID')
    user_name = models.CharField('用户名',max_length=15)
    content = models.TextField('内容')
    date = models.DateTimeField('评论创建日期',auto_now_add=True)

    def __str__(self):
        self.user_name

    class Meta:
        db_table = 'comments'

class Message(models.Model):
    content = models.CharField('留言',max_length=20)
    date = models.DateTimeField('日期',auto_now_add=True)

    def __str__(self):
        self.content

    class Meta:
        db_table = 'message'

