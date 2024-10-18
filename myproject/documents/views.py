from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.conf import settings
import os

def home(request):
    return render(request, 'home.html')

@login_required
def document_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            return redirect('document_view')
    else:
        form = DocumentForm()
    return render(request, 'documents/upload.html', {'form': form})

@login_required
def document_view(request):
    documents = Document.objects.filter(user=request.user)
    return render(request, 'documents/document_list.html', {'documents': documents})

def document_delete(request, pk):
    Document.objects.get(id=pk).delete()
    return redirect('document_view')



def serve_document(request, filename):
    # Define the path to your documents
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    
    # Check if file exists
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404("Document does not exist")
