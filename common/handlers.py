from django.shortcuts import render

from shop.models import BookStock


def conflict(request, target=None, template_name='409.html'):
    if isinstance(target, BookStock):
        template_name = 'shop/book_stock_conflict.html'

    try:
        saved = target.__class__._default_manager.get(pk=target.pk)
    except target.__class__.DoesNotExists:
        saved = None

    context = {
        'target': target,
        'saved': saved,
    }
    return render(request, template_name, context)
