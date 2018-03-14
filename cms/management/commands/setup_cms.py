import click
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site

from cms.models import Page
from cms.utils import get_current_site, setup_current_site

class Command(BaseCommand):

    help = 'Sets up the CMS for the user. Run this first before doing any work.'

    def add_arguments(self, parser):
        parser.add_argument('--site_name', action='store', help='Name of your Site (i.e: My Site)')
        parser.add_argument('--domain', action='store', help='Domain of your site (i.e.: example.com)')
        parser.add_argument('--create-sample-data', action='store_true',)

    def handle(self, create_sample_data=None, site_name=None, domain=None, *args, **kwargs):

        # set up the site
        site = get_current_site()
        site_created = False
        if not site:
            site_created = True
            setup_current_site(site_name=site_name, domain=domain)

        # create root element if it doesn't exist
        existing_pages = Page.objects.all()
        if len(existing_pages) == 0:
            self.setup_root_page(site)

        if len(existing_pages) == 1:
            root_page = existing_pages[0]
            if root_page.parent is not None:
                self.setup_root_page(site)
            
        root_page_name = Page.objects.get(parent=None, site=site)
        
        # create sample data
        if create_sample_data:
            
            # prompt user for site names
            click.secho('We will now create additional pages.', fg='green')
            click.secho('Enter "Q" or "q" (without quotes) anytime to quit.', fg='yellow')
            quit_values = ['Q', 'q']
            val = None
            while True:
                page_name = click.prompt('Please enter a new page name: ', type=str)
                if page_name not in quit_values:
                    page = Page.objects.create(name=page_name, parent=root_page_name)
                    click.secho('\t - Successfully created new page: %s' % page_name)
                else:
                    click.secho('Quitting CMS Setup.', fg='yellow')
                    click.secho('You can now start using the CMS!', fg='green')
                    return
        else:
            click.secho('Your CMS is already setup. You can go ahead and starting using it!', fg='green')
        
    def setup_root_page(self, site):
        '''
        Setup the root page element.
        '''
        print(site)
        click.secho('Creating Homepage: ' + site.name)
        root_page_name = '%s Homepage' % site.name
        root = Page.objects.create(name=root_page_name, site=site)
        click.secho('Successfully created Homepage "%s"' % root_page_name, fg='green')
