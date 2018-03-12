from django.forms.widgets import Widget
from django.utils.safestring import  mark_safe

class ModelLinkWidget(Widget):
    def __init__(self, obj, attrs=None):
        self.object = obj
        super(ModelLinkWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        if self.object.pk:
            return mark_safe(
                u'<a target="_blank" href="../../../%s/%s/%s/">Edit Component</a>' %\
                      (
                       self.object._meta.app_label,
                       self.object._meta.object_name.lower(),
                       self.object.pk, self.object
                       )
            )
        else:
            return mark_safe(u'')
