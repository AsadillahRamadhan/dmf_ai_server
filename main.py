import grpc
from concurrent import futures
import proto.ai_service_pb2 as ai_service_pb2
import proto.ai_service_pb2_grpc as ai_service_pb2_grpc
from process.analyze import process
import os
from dotenv import load_dotenv

load_dotenv()

class AIService(ai_service_pb2_grpc.AIServiceServicer):
    def AnalyzeData(self, request, context):
        data = process(request)
        return ai_service_pb2.DataResponse(
            rotation_rpm=1600,
            magnet_strength=0.8,
            magnet_active=True
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ai_service_pb2_grpc.add_AIServiceServicer_to_server(AIService(), server)
    server.add_insecure_port(f'[::]:{os.getenv('SERVER_PORT')}')
    server.start()
    print(f'Server Started at Port {os.getenv('SERVER_PORT')}')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()