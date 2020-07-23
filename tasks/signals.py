from django.db.models.signals import m2m_changed, post_save, pre_save, post_delete
from django.dispatch import receiver
from tasks.models import TodoItem, Category, PriorityCounter
from collections import Counter

from utils.counters import count_categories, count_priorities


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_added(sender, instance, action, model, **kwargs):
    if action != "post_add":
        return

    for cat in instance.category.all():
        slug = cat.slug

        new_count = 0
        for task in TodoItem.objects.all():
            new_count += task.category.filter(slug=slug).count()

        Category.objects.filter(slug=slug).update(todos_count=new_count)


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_removed(sender, instance, action, model, **kwargs):
    if action != "post_remove":
        return
    count_categories()


@receiver(post_save, sender=TodoItem)
def task_priority_changed(sender, instance, **kwargs):
    priority_counter, _ = PriorityCounter.objects.get_or_create(priority=instance.priority)
    count_priorities()


@receiver(post_delete, sender=TodoItem)
def task_deleted(sender, instance, **kwargs):
    count_categories()
    count_priorities()
