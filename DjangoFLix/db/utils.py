import string
import random
from django.utils.text import slugify


def get_random_string(size=4, chars=string.ascii_lowercase+string.digits):
    return "".join([random.choice(chars) for _ in range(size)])


def get_unique_slug(instance, new_slug=None, size=10):
    title = instance.title
    print(title)
    rand_str = get_random_string(size=size)
    if new_slug is None:
        slug = slugify(title)+rand_str
    else:
        slug = new_slug
    Klass = instance.__class__
    parent = None
    try:
        parent = instance.parent
    except:
        pass
    if parent is not None:
        qs = Klass.objects.filter(parent=parent, slug=slug)
    else:
        qs = Klass.objects.filter(slug=slug)

    if qs.exists():
        new_slug = slugify(title) + rand_str
        return get_unique_slug(instance, new_slug=new_slug)
    return slug
