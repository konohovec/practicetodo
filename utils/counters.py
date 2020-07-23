from tasks.models import PriorityCounter, TodoItem, Category
from collections import Counter


def count_categories():
    cat_counter = Counter()
    for cat in Category.objects.all():
        cat_counter[cat.slug] += cat.todoitem_set.all().count()

    for slug, new_count in cat_counter.items():
        Category.objects.filter(slug=slug).update(todos_count=new_count)


def count_priorities():
    for prc in PriorityCounter.objects.all():
        prc.todos_ammount = TodoItem.objects.filter(priority=prc.priority).count()
        prc.save()
