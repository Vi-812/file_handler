from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import File
from .serializers import FileSerializer
from .tasks import process_file


@api_view(['POST'])
def file_upload_view(request):
    if request.method == 'POST':
        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            file_instance = file_serializer.instance
            process_file.delay(file_instance.id)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def file_list_view(request):
    if request.method == 'GET':
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)
