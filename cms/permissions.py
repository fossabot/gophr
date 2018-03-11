from rest_framework.permissions import BasePermission, SAFE_METHODS

class PagePermission(BasePermission):
    '''
    PagePermission
    --------------
    The default permission used by Gophr's Page Views. A user who is 
    authenticated is allowed to pass on, but a user who is not authenticated
    (basically an Anonymous user) can only access content that is Published.
    '''

    def has_object_permission(self, request, view, page):

        if request.user.is_authenticated:

            '''
            The user is authenticated, and so we will allow them to access the 
            page. If they can access it, we return True and let the next 
            Permission class in the chain of permissions we check to determine
            if the user can access the page.
            '''
            return True

        else:
            '''
            This user is not authenticated, and so we need to check if the page
            has been published or not. If it is not published, they don't have 
            permission at all, but if it is published, they can access it.
            '''
            return True if page.is_published else False