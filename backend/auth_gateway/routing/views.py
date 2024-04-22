import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

session = requests.Session()
session.keep_alive = True

USER_URL = 'http://localhost:8001/api'
ACCOUNT_URL = 'http://localhost:8002/api'
TRANSACTION_URL = 'http://localhost:8003/api'

# helper function that makes post requests to a specified service
def post_request(url, endpoint, data):
    try:
        response = session.post(f'{url}/{endpoint}/', data=data)
        response.raise_for_status()
        
        # Add logging to inspect response content
        print("Response content:", response.content)
        return Response(response.json(), status=response.status_code)
    except requests.HTTPError as e:
        return Response({'error': f'{e}'}, status=e.response.status_code)
    except requests.RequestException as e:
        return Response({'error': f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# helper function that makes get requests to a specified service    
def get_request(url, endpoint, user_id):
    try:
        response = session.get(f'{url}/{endpoint}/', params={'user_id': user_id})
        response.raise_for_status()
        return Response(response.json(), status=response.status_code)
    except requests.HTTPError as e:
        return Response({'error': f'{e}'}, status=e.response.status_code)
    except requests.RequestException as e:
        return Response({'error': f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# USER SERVICE
# register
@api_view(['POST'])
def register(request):
    data = request.data
    return post_request(USER_URL, 'register', data)


# ACCOUNT SERVICE
# account create
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_account(request):
    data = request.data
    data['user'] = request.user.id
    return post_request(ACCOUNT_URL, 'create_account', data)


# account status
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def account_status(request):
    data = request.data
    return post_request(ACCOUNT_URL, 'account_status', data)


# get all accounts
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_accounts_by_user(request):
    try:
        # Forward the request to the 'get_accounts' endpoint
        response = session.get(f'{ACCOUNT_URL}/get_accounts_by_user/{request.user.id}')
        
        return Response(response.json(), status=response.status_code)
    except requests.RequestException as e:
        # Handle any errors that occurred during the request
        return Response({'error': f'Error fetching bank accounts: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# get all accounts via specified id
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_accounts_by_username(request, username):
    try:
        # Forward the request to the 'get_accounts' endpoint
        response = session.get(f'{ACCOUNT_URL}/get_accounts_by_username/{username}')
        
        return Response(response.json(), status=response.status_code)
    except requests.RequestException as e:
        # Handle any errors that occurred during the request
        return Response({'error': f'Error fetching bank accounts: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    

# TRANSACTION SERVICE
# Deposit
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def deposit(request):
    data = request.data
    return post_request(TRANSACTION_URL, 'deposit', data)

# External Payment
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def external_payment(request):
    data = request.data
    return post_request(TRANSACTION_URL, 'external_payment', data)

# Transfer money internally
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def transfer(request):
    data = request.data
    return post_request(TRANSACTION_URL, 'transfer', data)

# Get all accounts by account id
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def account_transactions(request, account_id):
    try:
        # Forward the request to the 'get_accounts' endpoint
        response = session.get(f'{TRANSACTION_URL}/account_transactions/{account_id}')
        
        return Response(response.json(), status=response.status_code)
    except requests.RequestException as e:
        # Handle any errors that occurred during the request
        return Response({'error': f'Error fetching bank accounts: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# Get all recurring payments by account
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def account_recurrings(request, account_id):
    try:
        # Forward the request to the 'get_accounts' endpoint
        response = session.get(f'{TRANSACTION_URL}/account_recurrings/{account_id}')
        
        return Response(response.json(), status=response.status_code)
    except requests.RequestException as e:
        # Handle any errors that occurred during the request
        return Response({'error': f'Error fetching bank accounts: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# Create recurring payment
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def recurring_payment(request):
    data = request.data
    return post_request(TRANSACTION_URL, 'recurring_payment', data)

    