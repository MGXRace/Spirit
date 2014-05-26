#-*- coding: utf-8 -*-
try:
    import pkg_resources
except ImportError:
    pkg_resources = None

__all__ = ['theme_template', 'THEME_CHOICES', 'THEME_DICT']


# Load theme classes automatically on module import
THEME_ENTRY_POINT = 'spirit.themes'
THEME_CHOICES = []
THEME_DICT = {}

if pkg_resources is not None:
    for ep in pkg_resources.iter_entry_points(THEME_ENTRY_POINT):
        THEME_CHOICES.append((ep.name, ep.name))
        THEME_DICT[ep.name] = ep.load()

def theme_template(user, template_name):
    if not user.is_authenticated():
        return ['spirit/{}'.format(template_name)]

    return [
        'spirit/themes/{}/{}'.format(user.theme, template_name),
        'spirit/{}'.format(template_name)
    ]