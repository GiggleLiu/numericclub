from django.shortcuts import render
from django.http import HttpResponse
import os

from .utils import md2html, html2headercontent

def rules(request):
    return render(request, 'rules.html', context={})

def help(request, page):
    source_folder, target_folder = 'markdowns', 'templates'
    with open(os.path.join(source_folder, page+'.md'), 'r') as f:
        mdtext = f.read()
    htmltext = md2html(mdtext)
    header, content = html2headercontent(htmltext)
    
    if header is not None and header!='':
        return render(request, 'headercontent.html', {'header':header, 'content':content})
    else:
        return render(request, 'error.html', context={'error':'Page not found!'})
