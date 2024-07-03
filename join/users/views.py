from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import View
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from .gmail import send_email
import logging

# Create your views here.

logger = logging.getLogger(__name__)

def homepage(request):
    """ Renders Homepage """
    return render(request, 'users/home.html')

class CustomLoginView(LoginView):
    """ This class-based view extends Django's built-in LoginView to customize the login template. """
    template_name = 'users/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # Browser close
            return redirect(reverse_lazy('users:profile'))
        else:
            logger.error(f"Login failed for user: {email}")
            return render(request, self.template_name, {'error': 'Invalid email or password'})

class CustomPasswordResetForm(PasswordResetForm):
    def save(self, domain_override = None,
             subject_template_name = 'users/reset_subject.txt',
             email_template_name = 'users/reset_email.html',
             use_https = False, token_generator = account_activation_token,
             from_email = None, request = None, html_email_template_name = None,
             extra_email_context = None):
        """
        Generates a one-use only link for resetting password and sends it to the user.
        """
        email = self.cleaned_data["email"]
        UserModel = get_user_model()
        active_users = UserModel._default_manager.filter(email__iexact=email, is_active=True)
        
        for user in active_users:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            subject = render_to_string(subject_template_name, context)
            # Email subject cannot contain newlines
            subject = ''.join(subject.splitlines())
            email_message = render_to_string(email_template_name, context)
            send_email(user.email, subject, email_message)

class CustomPasswordResetView(PasswordResetView):
    """ This class-based view extends Django's built-in PasswordResetView to customize the password reset process. """
    template_name = 'users/reset_password.html'
    email_template_name = 'users/reset_email.html'
    subject_template_name = 'users/reset_subject.txt'
    success_url = reverse_lazy('reset_done')
    form_class = CustomPasswordResetForm

    def form_valid(self, form):
        form.save(
            domain_override = self.request.META['HTTP_HOST'],
            subject_template_name = self.subject_template_name,
            email_template_name = self.email_template_name,
            use_https = self.request.is_secure(),
            token_generator = account_activation_token,
            from_email = None,
            request = self.request
        )
        return super().form_valid(form)

class RegisterView(View):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm

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
            logger.info("User created and verification email sent")
            return redirect('users:login')
        else:
            logger.error("Form is invalid: %s", form.errors)
        return render(request, self.template_name, {'form': form})

    def send_verification_email(self, request, user):
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('users/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = user.email
        try:
            send_email(to_email, mail_subject, message)  # Call your custom send_email function
            logger.info("Verification email sent to %s", to_email)
        except Exception as e:
            logger.error("Error sending email: %s", e)

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='users.backends.EmailBackend')  # Log in the user upon successful activation
        logger.info(f"User {user.username} activated and logged in successfully.")
        return redirect('users:login')
    else:
        logger.error(f"Activation failed for token {token}.")
        return render(request, 'users/activation_invalid.html')

@login_required(login_url='users:login')
def profile(request):
    """ Renders Profile Page. """
    logger.debug(f"User {request.user.username} trying to access profile page")
    return render(request, 'users/profile.html')

class CustomLogoutView(LogoutView):
    """ Custom logout view to redirect to a logout confirmation page. """
    template_name = 'users/logout.html'
    next_page = reverse_lazy('users:logout_success')

def logout_success(request):
    """ Renders a page to confirm successful logout. """
    return render(request, 'users/logout_success.html')
