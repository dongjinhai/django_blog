from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from .models import Users,Articles,Comments,Message
from django.views.generic.list import ListView
import markdown2
from pagedown.widgets import AdminPagedownWidget
from django.contrib.auth.signals import user_logged_in, user_logged_out
# 登录
from django.contrib.auth import login,logout,authenticate
# Create your views here.
# 创建表单
class UserForm(forms.Form):
    username = forms.CharField(label='用户',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput)

# 登录
def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #与数据库比较
            user = Users.objects.filter(name = username,password = password)
            if user:
                #跳转到首页
                response = HttpResponseRedirect('/index')
                #将username写如到request
                request.session['user'] = username
                return response
            else:
                return render_to_response('error.html',{'message':'用户和密码不对！'},context_instance=RequestContext(request))
    else:
        uf = UserForm()

    return HttpResponseRedirect('/index')
#注册
def regist(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 判断是否有效
            user = Users.objects.filter(name = username)
            if user:
                return render_to_response('error.html',{'message':username+':已存在!'},context_instance=RequestContext(request))
            else:
                #添加到数据库
                Users.objects.create(name = username,password = password)
                return HttpResponseRedirect('/index')
                # return HttpResponse('注册成功！')
        else:
            return render_to_response('error.html',{'message':'表单无效，请重新注册！'})
    else:
        uf = UserForm()

    return render_to_response('detail.html',{'uf':uf},context_instance=RequestContext(request))
#登出
def logout(request):
    response = HttpResponse('已经登出！')
    #清除session里的用户
    request.session['user'] =None
    # request.session['user'] = 'Anonymous users'
    return response

# 首页通用视图
class IndexView(ListView):
    template_name = 'index.html'
    # 指定要使用的上下文变量，可以在页面中使用
    context_object_name = 'article_list'

    def get_queryset(self):
        # 截取最新发布的5篇文章
        article_list = Articles.objects.all().order_by('-date')[0:5]
        for article in article_list:
            # fenced-code-blocks代码高亮
            article.content = markdown2.markdown(article.content,extras=['fenced-code-blocks'])
        return article_list

    def get_context_data(self,**kwargs):
        uf = UserForm()
        kwargs['uf'] = uf
        # 最新的12条留言
        messages = Message.objects.all().order_by('-date')[0:12]
        kwargs['messages'] = messages
        return super(IndexView,self).get_context_data(**kwargs)

class Detail(ListView):
    template_name = 'detail.html'
    context_object_name = 'comment_list'

    def get_queryset(self):
        # 倒序获得评论,使用data,‘—’使其倒叙
        comment_list = Comments.objects.filter(article_id = self.kwargs['article_id']).order_by('-date')
        return comment_list

    def get_context_data(self, **kwargs):
        article = Articles.objects.filter(id = self.kwargs['article_id'])
        # fenced-code-blocks代码高亮,使用markdown语法
        for article in article:
            # fenced-code-blocks代码高亮
            article.content = markdown2.markdown(article.content,extras=['fenced-code-blocks'])
        kwargs['article'] = article
        article_list = Articles.objects.all()
        kwargs['article_list'] = article_list
        return super(Detail, self).get_context_data(**kwargs)

def comment(request):
    if request.method=='POST':
        # 如果不存在content返回空，避免报错
        content = request.POST.get('content','')
        article_id = request.POST.get('article_id','')
        user_name = request.POST.get('user_name','')
        Comments.objects.create(content=content,article_id=article_id,user_name=user_name)
    return HttpResponseRedirect('/detail/'+article_id)
# 留言
def message(request):
    if request.method=='GET':
        content = request.GET.get('content','')
        Message.objects.create(content=content)
    return HttpResponseRedirect('/index')

def test(request):
    return render_to_response('test.html',{},context_instance=RequestContext(request))

