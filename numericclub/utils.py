import urllib.request, traceback
import pypandoc
from django.core.cache import cache
import re, os, glob

from . import settings

def get_readme(url):
    if url[-4:] == '.git':
        url = url[:-4]
    base_url = url.replace('github', 'raw.githubusercontent', 1).strip('/')+'/master/'
    readme_url = base_url +'README.md'
    readme = urllib.request.urlopen(readme_url)
    content =  readme.read().decode(readme.headers.get_content_charset())

    # fix image url
    pattern = re.compile(r'\!\[(.*?)\]\(/?((?!http).*?)\)', re.MULTILINE)
    content_ = re.sub(pattern, r'![\1](%s\2)'%base_url, content)
    # fix link url
    base_url_link = os.path.join(url, 'blob/master/')
    pattern = re.compile(r'([^!])\[(.*?)\]\(/?((?!http).*?)\)', re.MULTILINE)
    content_ = re.sub(pattern, r'\1[\2](%s\3)'%base_url_link, content_)
    return content_

def md2html(text):
    return pypandoc.convert_text(text, to='html5', format='md',
            extra_args=['--mathjax', '--standalone', '--toc',
                '--template=templates/markdown_template.html', '--css=static/css/template.css',
                ])

def html2headercontent(htmltext):
    header = re.search(r'<header>([\s\S]*)</header>', htmltext).group(1)
    content = re.search(r'<content>([\s\S]*)</content>', htmltext).group(1)
    return header, content

def get_readme_html(url):
    if url is not None and url!='':
        try:
            #if settings.DEBUG:
            #    with open('README.html', 'r') as f:
            #        htmltext = f.read()
            #        return html2headercontent(htmltext)
            #else:
            mdtext = get_readme(url)
            htmltext = md2html(mdtext)
            return html2headercontent(htmltext)
        except Exception:
            print(traceback.format_exc())
            return '',''
    else:
        return '',''

def headercontent4page(page):
    cache_id = 'headercontent-help-%s'%page
    res = cache.get(cache_id)
    if res is None:
        source_folder, target_folder = 'markdowns', 'templates'
        with open(os.path.join(source_folder, page+'.md'), 'r') as f:
            mdtext = f.read()
        htmltext = md2html(mdtext)
        res = html2headercontent(htmltext)
        cache.set(cache_id, res, 600)
    return res
