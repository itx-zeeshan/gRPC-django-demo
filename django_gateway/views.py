import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../generated')))

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import grpc
import auth_pb2, auth_pb2_grpc, user_pb2, user_pb2_grpc

def get_auth_stub():
    channel = grpc.insecure_channel("localhost:50051")
    return auth_pb2_grpc.AuthServiceStub(channel)

def get_user_stub():
    channel = grpc.insecure_channel("localhost:50052")
    return user_pb2_grpc.UserServiceStub(channel)


class RegisterView(APIView):
    def post(self, request):
        try:
            stub = get_auth_stub()
            res = stub.Register(auth_pb2.RegisterRequest(
                username=request.data["username"],
                password=request.data["password"],
                email=request.data["email"]
            ))
            return Response({
                "success": True,
                "data": {"access_token": res.token},
                "message": res.message
            }, status=status.HTTP_201_CREATED)

        except grpc.RpcError as e:
            return Response({
                "success": False,
                "message": e.details()
            }, status=grpc_to_drf_status(e.code()))
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        try:
            stub = get_auth_stub()
            res = stub.Login(auth_pb2.LoginRequest(
                username=request.data["username"],
                password=request.data["password"]
            ))
            return Response({
                "success": True,
                "data": {"access_token": res.token},
                "message": res.message
            }, status=status.HTTP_200_OK)

        except grpc.RpcError as e:
            return Response({
                "success": False,
                "message": e.details()
            }, status=grpc_to_drf_status(e.code()))
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    def get(self, request):
        try:
            token = request.headers.get("Authorization", "").replace("Bearer ", "")
            if not token:
                return Response({
                    "success": False,
                    "message": "Token not provided"
                }, status=status.HTTP_401_UNAUTHORIZED)

            # auth_stub = get_auth_stub()
            # valid = auth_stub.ValidateToken(auth_pb2.TokenRequest(token=token)).is_valid
            # if not valid:
            #     return Response({
            #         "success": False,
            #         "message": "Invalid token"
            #     }, status=status.HTTP_401_UNAUTHORIZED)

            username = request.GET.get("username")
            if not username:
                return Response({
                    "success": False,
                    "message": "Username is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            user_stub = get_user_stub()
            res = user_stub.GetUser(user_pb2.UserRequest(username=username))

            return Response({
                "success": True,
                "data": {"id": res.id, "username": res.username, "email": res.email},
                "message": "User fetched successfully"
            }, status=status.HTTP_200_OK)

        except grpc.RpcError as e:
            return Response({
                "success": False,
                "message": e.details()
            }, status=grpc_to_drf_status(e.code()))
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        

# Helper function to convert gRPC status codes to DRF status codes
def grpc_to_drf_status(code: grpc.StatusCode):
    return {
        grpc.StatusCode.INVALID_ARGUMENT: status.HTTP_400_BAD_REQUEST,
        grpc.StatusCode.UNAUTHENTICATED: status.HTTP_401_UNAUTHORIZED,
        grpc.StatusCode.PERMISSION_DENIED: status.HTTP_403_FORBIDDEN,
        grpc.StatusCode.NOT_FOUND: status.HTTP_404_NOT_FOUND,
        grpc.StatusCode.ALREADY_EXISTS: status.HTTP_409_CONFLICT,
        grpc.StatusCode.UNAVAILABLE: status.HTTP_503_SERVICE_UNAVAILABLE,
        grpc.StatusCode.INTERNAL: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }.get(code, status.HTTP_400_BAD_REQUEST)
