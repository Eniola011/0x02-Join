from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import View
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
# from .decorators import user_authenticated
from .forms import CustomUserCreationForm
# from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth import login
import logging
from .gmail import send_email  # Import your custom send_email function

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

class CustomPasswordResetView(PasswordResetView):
    """ This class-based view extends Django's built-in PasswordResetView to customize the password reset process. """
    template_name = 'users/reset_password.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

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
        login(request, user)  # Log in the user upon successful activation
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
