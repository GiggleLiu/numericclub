from being.models import newuser, getuserbyname
from topics.models import Genre, Topic, newvote
from talks.models import Talk
from django.contrib.auth.models import Group
from datetime import datetime
import random, traceback

def initialize():
    gdefault = Group.objects.get('default')
    if not gdefault:
        gdefault = Group('default')
        gdefault.save()

    # init user
    for i in range(10):
        username = 'test%d'%i
        if not getuserbyname(username):
            user = newuser(username=username, password='liujinguo',
                    email='cacate0129@gmail.com', description="%d"%i, avatar=None)

    # init genres
    glist = ['Quantum Computation', 'Machine Learning',
            'Tensor Network', 'Monte Carlo']
    for g in glist:
        try:
            gl = Genre(text=g)
            g.save()
            gl.append(g)
        except:
            pass

    # init topics
    for i in range(10):
        try:
            t = Topic(text='topic%d'%i, ref = None, url='www.baidu.com',
                    add_date=datetime.now(), genre=random.choice(Genre.objects.all()),
                    user=getuserbyname('test%d'%random.randint(0,9)))
            t.save()
        except:
            pass

    for t in Topic.objects.all():
        try:
            for j in range(5):
                kind = random.choice([1, 0, -1])
                newvote(topic=t, user=getuserbyname('test%d'%j), kind=kind)
        except Exception:
            print(traceback.format_exc())
