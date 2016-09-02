from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView

from .forms import LoginForm, JoinForm
from .models import User

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.cleaned_data['user'])
            if request.POST.get('next'):
                return redirect(request.POST['next'])
            else:
                return redirect('/')  # TODO: reverse url
        else:
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('accounts:login'))


class JoinView(CreateView):
    form_class = JoinForm
    template_name = 'accounts/join.html'

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, 'alert.html', {'message': 'Join Successful',
                                                   'url': '/'})


def user_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'accounts/user_view.html', {'user': user})