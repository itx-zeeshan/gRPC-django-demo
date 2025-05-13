import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../generated')))

import grpc
from concurrent import futures
import user_pb2, user_pb2_grpc
from models import SessionLocal, User

class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        db = SessionLocal()
        user = db.query(User).filter_by(username=request.username).first()

        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

        return user_pb2.UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email or ""
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    print("User gRPC Service running on port 50052")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
