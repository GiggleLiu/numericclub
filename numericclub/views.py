from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
import os

from .utils import md2html, html2headercontent

@cache_page(300)
def help(request, page):
    source_folder, target_folder = 'markdowns', 'templates'
    with open(os.path.join(source_folder, page+'.md'), 'r') as f:
        mdtext = f.read()
    htmltext = md2html(mdtext)
    header, content = html2headercontent(htmltext)
    
    if header is not None and header!='':
        template = 'headercontent.html'
        if page == 'rules':
            template = 'rules_template.html'
        return render(request, template, {'header':header, 'content':content})
    else:
        return render(request, 'error.html', context={'error':'Page not found!'})
