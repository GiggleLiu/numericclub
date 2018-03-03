from being.models import newgroup, getgroup, newuser, getuserbyname, newbeing
from topics.models import Genre, Topic, vote
from talks.models import Talk
from datetime import datetime
import random, traceback

def initialize():
    gdefault = getgroup('default')
    if not gdefault:
        gdefault = newgroup('default')

    # init user
    for i in range(10):
        username = 'test%d'%i
        if not getuserbyname(username):
            user = newuser(username, 'liujinguo', 'cacate0129@gmail.com')
            newbeing(user, truename=username, description="%d"%i, avatar=None)

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
                    add_date=datetime.now(), genre=random.choice(Genre.objects.all()))
            t.save()
        except:
            pass

    for t in Topic.objects.all():
        try:
            for j in range(5):
                kind = random.choice([1, 0, -1])
                vote(topic=t, user=getuserbyname('test%d'%j), kind=kind)
        except Exception:
            print(traceback.format_exc())
