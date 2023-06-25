from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from custom_auth.models import MainUser
from custom_auth.serializers import UserSerializer, EmailVerificationSerializer

# Create your views here.

class RegistrationView(generics.CreateAPIView):
    queryset = MainUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        current_site = get_current_site(request)
        verification_url = f"{current_site}/api/email-verify/{uid}/{token}"

        mail_subject = 'Подтвердите свой аккаунт'
        message = render_to_string('email_verification.html', {
            'user': user,
            'verification_url': verification_url
        })
        to_email = request.data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        user = serializer.save()
        return Response({'message': 'User created successfully. \
                         Please check your email to verify your account.'})

class EmailVerificationView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        try:
            uid = force_text(urlsafe_base64_decode(self.kwargs['uid']))
            user = MainUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, MainUser.DoesNotExist):
            return Response({'message': 'Invalid verification link'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Account verified successfully. You can now login.'})
        
        return Response({'message': 'Invalid verification link'}, 
                        status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    queryset = MainUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)

        user = MainUser.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            return Response({'message': 'Invalid credentials'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({'message': 'Account is not verified. \
                             Please check your email for verification instructions.'},
                            status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(response_data)