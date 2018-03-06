import sys
sys.path.insert(0, '.')
from numericclub.utils import get_readme, md2html

def test_getreadme():
    url = 'https://github.com/GiggleLiu/viznet'
    readme = get_readme(url)
    assert(readme)

def test_md2html():
    with open('README.md', 'r') as mdfile:
        lines = mdfile.readlines()
    mdtext = ''.join(lines)
    htmltext = md2html(mdtext)

    with open('README.html', 'w') as htmlfile:
        htmlfile.write(htmltext)

def test_url2html():
    url = 'https://github.com/GiggleLiu/viznet'
    mdtext = get_readme(url)
    htmltext = md2html(mdtext)

    with open('README.html', 'w') as htmlfile:
        htmlfile.write(htmltext)

if __name__ == '__main__':
    test_url2html()
