from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from .forms import  UploadFileForm,RegisterForm
from botocore.exceptions import NoCredentialsError

from django.views.decorators.http import require_POST
from django.contrib.auth import login

import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv


# Load the environment variables from .env file
load_dotenv('myproject/aws_secrets.env')
bucket_name = settings.AWS_STORAGE_BUCKET_NAME

# Create an S3 client using credentials from settings.py
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)





@login_required
def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home page or your chosen URL after logout

@login_required
def document_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_name = default_storage.save(file.name, file)

            # Directly use the file URL or handle file content
            file_url = default_storage.url(file_name)

            # Upload to S3 using the file's content
            # Assuming `upload_to_s3` can be modified to take file content or a file-like object
            if upload_to_s3(default_storage.open(file_name, 'rb'), bucket_name, file_name):
                full_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
                messages.success(request, f'Success! Your file is saved at {full_url}')
            else:
                messages.error(request, 'Failed to upload to S3')
                return HttpResponse("Failed to upload to S3", status=500)
        else:
            messages.error(request, 'Form is not valid')
            return HttpResponse("Form is not valid", status=400)
        return redirect('home')
    else:
        form = UploadFileForm()  # An unbound form

    return render(request, 'documents/upload_form.html', {'form': form})




@login_required
def document_view(request):
    # Get list of objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    objects = response.get('Contents', [])

    # Create a list that will store each object's data, including a public URL
    documents = []
    for obj in objects:
        document = {
            'name': obj['Key'],
            'url': f"https://{bucket_name}.s3.amazonaws.com/{obj['Key']}",
            'last_modified': obj['LastModified'],
            'size': obj['Size']
        }
        documents.append(document)

    return render(request, 'documents/document_list.html', {'documents': documents})


@login_required
@require_POST  # Ensure this view can only be called with a POST request for security
def document_delete(request, key):
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=key)
    except Exception as e:
        # Log the error or handle it appropriately
        print(e)

    return redirect('document_view')


def serve_document(request, filename):
    # Initialize the S3 client
    s3_client = boto3.client('s3')

    # The path where the file will be saved temporarily (in memory)
    from io import BytesIO
    stream = BytesIO()
    try:
        # Download the file from S3 to a stream
        s3_client.download_fileobj(
            Bucket=bucket_name,
            Key=filename,
            Fileobj=stream
        )
        # Set the stream position to the beginning
        stream.seek(0)

        # Create a response object and send the file directly to the user
        response = HttpResponse(stream.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    except s3_client.exceptions.NoSuchKey:
        # If the file doesn't exist in S3, raise a 404 error
        raise Http404("Document does not exist")

    except Exception as e:
        # Handle other possible exceptions (like permission issues, etc.)
        raise Http404(f"An error occurred accessing the document: {str(e)}")

    finally:
        # Close the stream
        stream.close()


def upload_to_s3(file_obj, bucket_name, file_name):

    try:
        # Upload the file to S3
        s3_client.upload_fileobj(
            file_obj,  # File object opened in binary-read mode
            bucket_name,
            file_name,
        )
        return True
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Credentials error: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False




def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately after registration
            return redirect('home')  # Redirect to a home page or other appropriate page
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
