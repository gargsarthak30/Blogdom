from django.shortcuts import render, HttpResponseRedirect, render_to_response
from django.core.context_processors import csrf
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.views.generic import *
from .forms import PasswordResetRequestForm, SetPasswordForm, RegistrationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models.query_utils import Q
from . import welcomeMail


def user_signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            subject = welcomeMail.subject
            message = welcomeMail.message
            from_email = welcomeMail.from_email
            to_list = [request.POST.get('email')]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            return HttpResponseRedirect(reverse('login'))
    else:
        form = RegistrationForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('signup.html', args)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('user_profile_edit'))
        else:
            c = {}
            c.update(csrf(request))
            c['errors'] = 'Wrong Credentials'
            return render_to_response('login.html', c)
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c)


# For Password Reset

class ResetPasswordRequestView(FormView):
    template_name = "test_template.html"
    success_url = 'user_account/login'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email_or_username"]

<<<<<<< HEAD
            if self.validate_email_address(data) is True:
                associated_users = User.objects.filter(Q(email=data)|Q(username=data))
                if associated_users.exists():
                    for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'Blogdom',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                        subject_template_name='password_reset_subject.txt'
                        email_template_name = 'password_reset_email.html'
                        subject = loader.render_to_string(subject_template_name, c)
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

                    result = self.form_valid(form)
                    messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
                    return result
                result = self.form_invalid(form)
                messages.error(request, 'No user is associated with this email address')
                return result

            else:
                associated_users = User.objects.filter(username=data)
                if associated_users.exists():
                    for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'Blogdom',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                        subject_template_name='password_reset_subject.txt'
                        email_template_name = 'password_reset_email.html'
                        subject = loader.render_to_string(subject_template_name, c)
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, 'garg_sarthak@yahoo.com', [user.email], fail_silently=False)

                    result = self.form_valid(form)
                    messages.success(request, 'Email has been sent to ' + data +"'s email address. Please check its inbox to continue reseting password.")
                    return result

                result = self.form_invalid(form)
                messages.error(request, 'This username does not exist in the system.')
                return result

=======
        if self.validate_email_address(data) is True:
            associated_users = User.objects.filter(Q(email=data)|Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': 'Blogdom',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                    subject_template_name='password_reset_subject.txt'
                    email_template_name = 'password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

                result = self.form_valid(form)
                messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'No user is associated with this email address')
            return result

        else:
            associated_users = User.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': 'Blogdom',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                    subject_template_name='password_reset_subject.txt'
                    email_template_name = 'password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, 'garg_sarthak@yahoo.com', [user.email], fail_silently=False)

                result = self.form_valid(form)
                messages.success(request, 'Email has been sent to ' + data +"'s email address. Please check its inbox to continue reseting password.")
                return result

            result = self.form_invalid(form)
            messages.error(request, 'This username does not exist in the system.')
            return result

>>>>>>> 6cd1878fc6176a9923f87f47e1f2b62c1f61f210
        messages.error(request, 'Invalid Input')
        return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
    template_name = 'test_template.html'
<<<<<<< HEAD
    success_url = 'user_account/login/'
=======
    success_url = '/login/'
>>>>>>> 6cd1878fc6176a9923f87f47e1f2b62c1f61f210
    form_class = SetPasswordForm

    def post(self, request, token=None, uidb64=None, *args, **kwargs):
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user=None
        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password has been reset.")
                return self.form_valid(form)
            else:
                messages.error(request, "Password reset has been unsuccessful.")

        else:
             messages.error(request, 'The reset password link is no longer valid.')
             return self.form_invalid(form)

