import json
import jsonschema
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Create your models here.
class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True


class ComponentType(BaseModel):


    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        help_text='The name of the component')

    slug = models.CharField(
        max_length=255,
        null=False,
        blank=True,
        db_index=True,
        help_text='The Slug Value is auto-generated from the component type\'s name.')

    is_static = models.BooleanField(default=True)

    schema = models.TextField(
        null=False,
        default=False,
        help_text='Valid JSON Schema to validate the datatype'
    )

    class Meta:

        verbose_name = 'Component Type'

    def __str__(self):

        return '%s - (%s)' % (self.name, 'static' if self.is_static else 'dynamic')

    def clean_fields(self, exclude=None):

        super(ComponentType, self).clean_fields(exclude=exclude)
        try:
            json.loads(self.schema)
        except json.JSONDecodeError as e:
            raise ValidationError({
                'schema': _('Schema is not a valid JSON. %s' % str(e))
            })

    def save(self, *args, **kwargs):

        json.loads(self.schema)
        return super(ComponentType, self).save(*args, **kwargs)


from mptt.models import MPTTModel, TreeForeignKey

from cms.fields import JSONTextField
from cms.utils import get_current_site_id


class Resource(BaseModel, MPTTModel):

    name = models.CharField(
        max_length=255,
        null=False,
        blank=False)

    description = models.CharField(
        max_length=500,
        null=True,
        blank=True)

    slug = models.CharField(
        max_length=255,
        null=False,
        blank=True)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)

    path = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        db_index=True)

    def save(self, *args, **kwargs):

        self.slug = slugify(self.name)
        self.path = self.determine_path()
        return super(Resource, self).save(*args, **kwargs)

    def determine_path(self):

        resource = self
        resources = []
        while resource.parent:
            resources.append(resource)
            resource = resource.parent

        if resources:
            resources.reverse()
        return '/' + '/'.join([r.slug for r in resources])

    def get_absolute_url(self):

        url = reverse('page-detail', args=[self.path.strip('/')])
        return '/%s' % url.strip('/')

    def __str__(self):

        return "%s" % (self.name)

    class Meta:

        abstract = True


class Page(Resource):
    '''
    Inheriting from a Resource, the page is an abstraction that represents a
    typical HTML page, that has a name, description and a unique slug.
    '''
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='(Optional) The page title is optional. If it is empty, the Page Name will be used.')

    site = models.ForeignKey('sites.Site', default=get_current_site_id, on_delete=models.CASCADE)

    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if not self.title:
            self.title = self.name

        return super(Page, self).save(*args, **kwargs)

    class Meta:

        verbose_name = 'CMS Page'

class Section(BaseModel):

    page = models.ForeignKey(
        'cms.Page',
        on_delete=models.CASCADE,
        help_text="Select the page that this section belongs to.",
        related_name='sections'
    )

    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        help_text='Give a name for the section')

    slug = models.CharField(
        max_length=255,
        null=False,
        blank=True,
        help_text='The Slug value is auto-generated from your section\'s name.')

    position = models.IntegerField(default=0, null=False)

    def __str__(self):

        return '%s :: %s' % (self.page.name, self.name)

    def save(self, *args, **kwargs):

        self.slug = slugify(self.name)
        return super(Section, self).save(*args, **kwargs)

    class Meta:

        verbose_name = 'Page Section'

class Component(BaseModel):

    section = models.ForeignKey(
        'cms.Section',
        on_delete=models.CASCADE,
        help_text='The section this component belongs to.',
        related_name='components'
    )

    component_type = models.ForeignKey(
        'cms.ComponentType',
        on_delete=models.CASCADE,
        default=''
    )

    name = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    slug = models.CharField(
        max_length=255,
        null=False,
        blank=True,
        help_text='The Slug Value is auto-generated from your component\'s name.'
    )

    content = JSONTextField(null=False, blank=True, default="{}")

    position = models.IntegerField(default=0, null=False)

    def get_admin_edit_link(self):

        if self.id:
            url = reverse('admin:cms_component_change', args=(self.id,))
            return '<a class="btn btn-success" style="color:#fff;" href="#" onclick="window.open(\'%s?_popup=1\', \'Edit Component\', \'left=20,top=20,width=1024,height=512,toolbar=0,resizable=0\');">Click Here to Edit Component</a>' % url
        else:
            return 'Component not created yet. Please Save this component first before trying to edit it.'

    def __str__(self):

        return self.name

    def save(self, *args, **kwargs):

        self.validate_component()
        self.slug = slugify(self.name)
        return super(Component, self).save(*args, **kwargs)


    def validate_component(self):

        pass

