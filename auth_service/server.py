import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../generated')))

import grpc
from concurrent import futures
import auth_pb2, auth_pb2_grpc
import jwt, datetime
from models import User, SessionLocal

SECRET_KEY = 'django-insecure-fo-c5@6w(ifllsb&ym0i#h+fz(lv40lomxt*)v0ulx!--=)sl&'

import grpc

class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def Register(self, request, context):
        db = SessionLocal()
        if db.query(User).filter_by(username=request.username).first():
            context.abort(grpc.StatusCode.ALREADY_EXISTS, "User already exists")

        try:
            new_user = User(username=request.username, password=request.password, email=request.email)
            db.add(new_user)
            db.commit()

            token = jwt.encode({
                "username": request.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, SECRET_KEY, algorithm="HS256")

            return auth_pb2.AuthResponse(token=token, message="Registered successfully")
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Server error: {str(e)}")

    def Login(self, request, context):
        db = SessionLocal()
        user = db.query(User).filter_by(username=request.username, password=request.password).first()
        if not user:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid credentials")

        token = jwt.encode({
            "username": request.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")

        return auth_pb2.AuthResponse(token=token, message="Login successful")

    def ValidateToken(self, request, context):
        try:
            jwt.decode(request.token, SECRET_KEY, algorithms=["HS256"])
            return auth_pb2.ValidateResponse(is_valid=True)
        except jwt.ExpiredSignatureError:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token has expired")
        except jwt.InvalidTokenError:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Auth gRPC Service running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()