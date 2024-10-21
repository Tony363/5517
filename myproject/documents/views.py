from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from .forms import DocumentForm, UploadFileForm
from .models import Document
from botocore.exceptions import NoCredentialsError
import os
import boto3
from django.views.decorators.http import require_POST
from django.contrib.auth import login
from .forms import RegisterForm
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
            print("WTF",file_name)
            local_file_path = default_storage.path(file_name)

            # Upload to S3
            if upload_to_s3(local_file_path, bucket_name, file_name):
                file_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
                messages.success(request, f'Success! Your file is saved at {file_url}')
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
    # document = get_object_or_404(Document, upload__name=key)
    # Attempt to delete the file from S3
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=key)
    except Exception as e:
        # Log the error or handle it appropriately
        print(e)

    # Delete the document record from the database
    # document.delete()
    return redirect('document_view')

# def serve_document(request, filename):
#     # Ensure the filename exists in S3 and then redirect to its URL
#     try:
#         # Check if the file exists by trying to get its metadata
#         response = s3_client.head_object(Bucket=settings.AWS_S3_BUCKET_NAME, Key=filename)
#         file_url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{filename}"
#         return redirect(file_url)
#     except s3_client.exceptions.ClientError as e:
#         # If a client error is thrown, then the file doesn't exist
#         raise Http404("Document does not exist")
    

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



def upload_to_s3(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket using settings from Django settings.py

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified, file_name is used
    :return: True if file was uploaded, else False
    """

    try:
        # Upload the file
        s3_client.upload_file(file_name, bucket, object_name)
        return True
    except NoCredentialsError:
        print("Credentials not available")
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
