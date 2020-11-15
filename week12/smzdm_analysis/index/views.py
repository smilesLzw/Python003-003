from django.shortcuts import render

from .models import Comment

# Create your views here.
def index(request):
    conditions = {}

    # 所有采集到的数据
    comments = Comment.objects.all()

    # 正向评论数据
    positive_comment = Comment.objects.filter(sentiment__gte=0.5)
    # 负向评论数据
    negative_comment = Comment.objects.filter(sentiment__lt=0.5)

    # 获取搜索关键字
    search = request.POST.get('search', '')

    # 如果有搜索关键字，则增加筛选条件
    if search:
        conditions['comment__contains'] = search
        comments = Comment.objects.filter(**conditions)
        return render(request, 'index.html', context={'comments': comments})
    else:
        return render(request, 'index.html', context={'comments': comments})