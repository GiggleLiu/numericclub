from django.shortcuts import render
from django.http import HttpResponse

from .utils import headercontent4page

def help(request, page):
    header, content = headercontent4page(page)
    if header is not None and header!='':
        template = 'headercontent.html'
        if page == 'rules':
            template = 'rules_template.html'
        return render(request, template, {'header':header, 'content':content})
    else:
        return render(request, 'error.html', context={'error':'Page not found!'})
