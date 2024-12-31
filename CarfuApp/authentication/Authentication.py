from rest_framework.authentication import TokenAuthentication


class UserTokenAuthentication(TokenAuthentication):

    def authenticate(self, request):
        from CarfuApp.models import AuthUserToken
        from rest_framework.exceptions import AuthenticationFailed
        header_token = request.META.get('HTTP_AUTHORIZATION')
        if not header_token:
            return None
        try:
            token = header_token.split(' ')[1]
            verified_token = AuthUserToken.objects.get(key=token)
            user = verified_token.user
        except (AuthUserToken.DoesNotExist, IndexError, ValueError) as e:
            raise AuthenticationFailed('Invalid token provided')
        return user, None

    def authenticate_header(self, request):
        return self.authenticate(request)
