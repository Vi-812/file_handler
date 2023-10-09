from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import File
from .serializers import FileSerializer
from .tasks import process_file
from .forms import FileUploadForm
from django.shortcuts import render, redirect
from django.urls import reverse


def index_view(request):
    answer = request.GET.get('answer')
    context = {
        'answer': answer
    }
    return render(request, 'index.html', context)


def process_file_upload(uploaded_file):
    try:
        file_serializer = FileSerializer(data={'file': uploaded_file})

        if file_serializer.is_valid():
            file_serializer.save()
            file_instance = file_serializer.instance
            process_file.delay(file_instance.id)
            return file_serializer.data
        else:
            error_message = f"Ошибка загрузки файла. Дополнительные данные: {file_serializer.errors}"
            return {'error': error_message}
    except Exception as e:
        return {'error': str(e)}


@api_view(['POST'])
def api_file_upload_view(request):
    if request.method == 'POST':
        uploaded_file = request.data.get('file')
        if not uploaded_file:
            return Response({'error': 'Файл не был передан.'}, status=status.HTTP_400_BAD_REQUEST)

        result_data = process_file_upload(uploaded_file)

        if 'error' in result_data:
            return Response(result_data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(result_data, status=status.HTTP_201_CREATED)


def ui_file_upload_view(request):
    if request.method == 'GET':
        form = FileUploadForm()
        return render(request, 'file_upload.html', {'form': form})
    elif request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            result_data = process_file_upload(uploaded_file)

            if 'error' in result_data:
                redirect_url = f"{reverse('ui-index')}?answer={result_data['error']}"
                return redirect(redirect_url)
            else:
                redirect_url = f"{reverse('ui-index')}?answer={result_data}"
                return redirect(redirect_url)


@api_view(['GET'])
def api_file_list_view(request):
    if request.method == 'GET':
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)


def ui_file_list_view(request):
    if request.method == 'GET':
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return render(request, 'file_list.html', {'files': serializer.data})
