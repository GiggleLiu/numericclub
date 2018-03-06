import urllib.request, traceback
import pypandoc
import re, os, glob

from . import settings

def get_readme(url):
    if url[-4:] == '.git':
        url = url[:-4]
    base_url = url.replace('github', 'raw.githubusercontent', 1).strip('/')+'/master/'
    readme_url = base_url +'README.md'
    readme = urllib.request.urlopen(readme_url)
    content =  readme.read().decode(readme.headers.get_content_charset())

    # fix url
    pattern = re.compile(r'\!\[(.*?)\]\(((?!https).*?)\)', re.MULTILINE)
    content_ = re.sub(pattern, r'![\1](%s\2)'%base_url, content)
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
