from being.models import newuser, getuserbyname
from topics.models import Genre, Topic, newvote
from talks.models import Talk
from datetime import datetime
import random, traceback

def initialize():
    # init user
    admin = 'cacate'
    if not getuserbyname(admin):
        user = newuser(truename=admin, password='liujinguo',
                email='cacate0129@iphy.ac.cn', description="I am the boss!", avatar=None)
        user.is_staff = True
        user.is_superuser = True
        user.save()
    for i in range(10):
        truename = 'test%d'%i
        if not getuserbyname(truename):
            user = newuser(truename=truename, password='liujinguo',
                    email='cacate012%d@gmail.com'%i, description="%d"%i, avatar=None)
            print('create user %s'%truename)

    # init genres
    glist = ['Quantum Computation', 'Machine Learning',
            'Tensor Network', 'Monte Carlo']
    for g in glist:
        try:
            g = Genre(text=g)
            g.save()
            print('create genre %s'%g)
        except Exception:
            pass

    # init topics
    for i in range(10):
        try:
            t = Topic(text='topic%d'%i, ref = None, url='www.baidu.com',
                    add_date=datetime.now(), genre=random.choice(Genre.objects.all()),
                    user=getuserbyname('test%d'%random.randint(0,9)))
            t.save()
            print('create topic %s'%t)
        except:
            pass

    for t in Topic.objects.all():
        try:
            for j in range(5):
                kind = random.choice([1, 0, -1])
                v = newvote(topic=t, user=getuserbyname('test%d'%j), kind=kind)
                print('create vote %s'%v)
        except Exception:
            print(traceback.format_exc())
