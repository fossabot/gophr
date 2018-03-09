import click
from django.conf import settings
from django.contrib.sites.models import Site


def setup_current_site():
    '''
    Sets up the user with the current site.
    '''
    site_id = settings.SITE_ID
    click.secho('\nA site has not been configured for this CMS. Please answer the questions below.', fg='yellow')
    domain = click.prompt('Please enter the domain you are registering the site for: (i.e.: mysite.com): ', type=str, default='mysite.com')
    site_name = click.prompt('What is the name of your site? (i.e.: MySite DEV): ', type=str, default='MySite DEV')
    site = Site.objects.create(id=site_id, domain=domain, name=site_name)
    return site

def get_current_site():
    '''
    Gets the current site information.
    '''
    if not hasattr(settings, 'SITE_ID'):
        msg = '\nYou need to define SITE_ID in your settings. More information: https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-SITE_ID'
        click.secho(msg, fg='red')
        raise ValueError(msg)
    
    try:
        site_id = settings.SITE_ID
        site = Site.objects.get(id=site_id)
        return site
    except Site.DoesNotExist:
        click.secho("Please setup your site by calling 'python manage.py setup_cms' before continuing.", fg='red')
    return None

def get_current_site_id():
    '''
    Gets the current site id.
    '''
    site = get_current_site()
    return site.id