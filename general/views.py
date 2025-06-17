from django.shortcuts import render, get_object_or_404
from .models import Blog  # or whatever your blog model is named

from django.shortcuts import render

def blog_list(request):
    return render(request, 'blog_list.html') 

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog_detail.html', {'blog': blog})
