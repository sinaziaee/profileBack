from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from account.api.serializers import *
from account.models import Account
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['response'] = 'successful'
        token = Token.objects.get(user=account).key
        data['token'] = token
        data['user_id'] = account.user_id
        data['email'] = account.email
        data['first_name'] = account.first_name
        data['last_name'] = account.last_name
        return Response(data=data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def account_properties_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountPropertiesSerializer(account)
        return Response(serializer.data)


@api_view(('GET',))
def all_accounts_view(request):
    all_accounts = Account.objects.all()

    if request.method == 'GET':
        serializer = AccountPropertiesSerializer(all_accounts, many=True)
        return Response(serializer.data)


class TokenObtainView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        print(request.data)
        # user =
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        custom_response = {
            'token': token.key,
            'user_id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }

        return Response(custom_response, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class logoutView(APIView):
    def post(self, request):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response("Successfully logged out!", status=status.HTTP_200_OK)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def update_account_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AccountPropertiesSerializer(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'Updating account has successfully done!'
            return Response(data=data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_user(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return account
