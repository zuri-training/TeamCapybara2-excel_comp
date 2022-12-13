from django.shortcuts import redirect,get_object_or_404
from django.core.exceptions import ImproperlyConfigured

from authentication.models import Profile

class NotVerifiedMixin:
    """
    A mixin to redirect non verified users to a custom page 
    requesting them to verify their accounts before gaining 
    access to the full functionalities of the web app.
    Redirect user to redirect_url if test_func() returns False
    """

    redirect_url = None

    def get_redirect_url(self):
        redirect_url = self.redirect_url
        if not redirect_url:
            raise ImproperlyConfigured(
                '{0} is missing redirect_url attribute. Define {0}.redirect_url to overide get_redirect_url() method'.format(self.__class__.__name__)
            )
        return str(redirect_url)

    def test_func(self):
        raise NotImplementedError(
            '{0} method test_func() failed to be implemented'.format(self.__class__.__name__)
        )
    
    def get_test_func(self):
        return self.test_func()

    def dispatch(self,request,*args,**kwargs):
        test_result = self.get_test_func()
        if not test_result:
            return redirect(self.get_redirect_url())
        return super().dispatch(request,*args,**kwargs)

class CheckVerificationMixin(NotVerifiedMixin):
    def test_func(self):
        user = self.request.user 
        user_profile = get_object_or_404(Profile,user=user)
        return user_profile.is_verified