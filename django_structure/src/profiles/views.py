from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator

from profiles.models import Profile

# Create your views here.
# Подключение функций для работы страниц: home, about, userProfile:
def home(request):
    context = {}
    template = 'home.html'
    return render(request, template, context)

def about(request):
    context = {}
    template = 'about.html'
    return render(request, template, context)

# Декоратор, требующий обязательного входа в профиль:
@login_required
def userProfile(request):
    user = request.user
    context = {'user': user}
    template = 'profile.html'
    return render(request, template, context)

    class ProfileObjectMixin(SingleObjectMixin):
        """
        Provides views with the current user's profile.
        """
        model = Profile

        def get_object(self):
            """Return's the current users profile."""
            try:
                return self.request.user.get_profile()
            except Profile.DoesNotExist:
                raise NotImplemented(
                    "What if the user doesn't have an associated profile?")

        @method_decorator(login_required)
        def dispatch(self, request, *args, **kwargs):
            """Ensures that only authenticated users can access the view."""
            klass = ProfileObjectMixin
            return super(klass, self).dispatch(request, *args, **kwargs)


    class ProfileUpdateView(ProfileObjectMixin, UpdateView):
        """
        A view that displays a form for editing a user's profile.

        Uses a form dynamically created for the `Profile` model and
        the default model's update template.
        """
        pass  # That's All Folks!
