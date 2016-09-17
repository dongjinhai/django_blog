from django.contrib import admin
from .models import Articles,Users,Comments,Message
from django import forms
from pagedown.widgets import AdminPagedownWidget
# Register your models here.

# 后台文章的输入使用pagedown编辑器，支持markdown
# 定义自己的form
class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=AdminPagedownWidget())
    class Meta:
        model =Articles
        fields = '__all__'

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm

admin.site.register(Articles,ArticleAdmin)
admin.site.register(Users)
admin.site.register(Comments)
admin.site.register(Message)
