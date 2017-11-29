from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post



"""
https://mozillazg.github.io/2013/01/django-pagination-by-use-paginator.html
"""
def post_list(request, category=None):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts})


"""
    return render(request, 'blog/post/list.html', context={'posts': queryset})
     ** ListView (带分页)
"""
class PostListView(ListView):       # Django的Class Basic View -- ListView：显示对象列表
    queryset = Post.published.all()
    context_object_name = 'posts'       #（'posts' = queryset） 指定获取的模型列表数据保存的变量名。这个变量会被传递给模板
    paginate_by = 5             #  指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    template_name = 'blog/post/list.html'       # 指定这个视图渲染的模板


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})