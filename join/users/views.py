from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth import login

# Create your views here.

User = get_user_model()

def homepage(request):
    """ Renders Homepage """
    return render(request, 'users/home.html')

class CustomLoginView(LoginView):
    """ This class-based view extends Django's built-in LoginView to customize the login template. """
    template_name = 'users/login.html'

class CustomPasswordResetView(PasswordResetView):
    """ This class-based view extends Django's built-in PasswordResetView to customize the password reset process. """
    template_name = 'users/reset_password.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class RegisterView(View):
    template_name = 'users/register.html'
    form_class = UserCreationForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            self.send_verification_email(request, user)
            return redirect('login')
        return render(request, self.template_name, {'form': form})

    def send_verification_email(self, request, user):
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('users/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user),
        })
        to_email = user.email
        send_mail(mail_subject, message, 'yettyagbalu@gmail.com', [to_email])

class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/activation_invalid.html')
