#-*- coding: utf-8 -*-

from django.template.loader import select_template
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponsePermanentRedirect

from spirit.models.topic import Topic
from spirit.models.category import Category
from spirit.themes import theme_template


def category_detail(request, pk, slug):
    category = Category.objects.get_public_or_404(pk=pk)

    if category.slug != slug:
        return HttpResponsePermanentRedirect(category.get_absolute_url())

    subcategories = Category.objects.for_parent(parent=category)
    topics = Topic.objects.for_category(category=category)\
        .order_by('-is_pinned', '-last_active')\
        .select_related('category')

    base_template = select_template(theme_template(request.user, '_base.html'))
    templates = theme_template(request.user, 'category/category_detail.html')
    return render(request, templates, {'base_template': base_template,
                                       'category': category,
                                       'subcategories': subcategories,
                                       'topics': topics})


class CategoryList(ListView):

    context_object_name = "categories"
    queryset = Category.objects.for_parent()

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        templates = theme_template(context.user, 'category/category_list.html')
        return self.response_class(
            request=self.request,
            template=templates,
            context=context,
            **response_kwargs
        )
