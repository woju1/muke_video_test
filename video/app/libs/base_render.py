# coding:utf-8

from mako.lookup import TemplateLookup
from django.template import RequestContext
from django.conf import settings
from django.template.context import Context
from django.http import HttpResponse
from django.template import Template


def render_to_response(request, template, data=None):
    context_instance = RequestContext(request)
    path = settings.TEMPLATES[0]['DIRS'][0]

    lookup = TemplateLookup(
        directories=[path],
        output_encoding='utf-8',
        input_encoding='utf-8'
    )
    mako_template = lookup.get_template(template)

    if not data:
        data = {}

    if context_instance:
        context_instance.update(data)
    else:
        context_instance = Context(data)

    result = {}
    for d in context_instance:
        result.update(d)
    result['request'] = request
    result['csrf_token'] = '<input type="hidden" id="django-csrf-token"' \
                           'name="csrfmiddlewaretoken" ' \
                           'value={0}>'.format(request.META['CSRF_COOKIE'])

    # 使用 {% csrf_token %} 标签插入CSRF令牌
    # csrf_token_template = Template('{% csrf_token %}')
    # result['csrf_token'] = csrf_token_template.render(RequestContext(request))
    return HttpResponse(mako_template.render(**result))
