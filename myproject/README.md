The Cloud Drive application is a Django-based project designed for document management, utilizing AWS S3 for cloud storage. The application supports user registration, login, document upload, viewing, and deletion.
## Table of Contents
- [Functions Provided](#Functions-Provided)
- [Implementation of Functions](#Implementation-of-Functions)
- [Component Design](#Component-Design)
- [Deployment Design](#Deployment-Design)
- [Setup and Configuration](#Setup-and-Configuration)
- [Installation Instructions](#Installation-Instructions)
- [Running the Application](#Running-the-Application)
----

## URL Endpoints

| Endpoint               | Functionality                          |
|------------------------|----------------------------------------|
| `/register/`           | User registration page                 |
| `/upload/`             | Document upload form                   |
| `/view/`               | View list of uploaded documents        |
| `/logout/`             | Logout the current user                |
| `/delete/<str:key>/`   | Delete a specific document             |
| `/serve/<str:filename>/` | Download a specific document         |


## Functions Provided
1. User Registration and Authentication

    * Allows new users to create accounts.
    * Enables existing users to log in and manage their sessions.
    * Provides logout functionality for session management.

2. Document Upload

    * Supports file uploads, allowing users to store documents (e.g., PDF, JPG, TXT) in the cloud.
    * Utilizes AWS S3 to store files securely.

3. Document Management

    * Lists uploaded documents, displaying metadata such as name, size, and last modified date.
    * Allows users to delete documents from AWS S3.
    * Provides a download function, allowing users to retrieve files from S3 directly.

4. Secure File Access

    * Ensures that only authenticated users can upload, view, or delete files.
    * Uses Django’s built-in authentication system to manage user sessions.

## Implementation of Functions
1. User Registration (RegisterForm)

    * Form: Extends Django’s UserCreationForm with an additional email field.
    * Validation: Ensures that users provide valid email addresses and that passwords meet specified security requirements.
    * View Logic: The register view processes form data, creates a new user, and logs them in upon successful registration.
    * Database Interaction: Uses Django’s ORM to save user details in the SQLite3 database.

2. File Upload (UploadFileForm)

    * orm: A simple form with a FileField to handle file uploads.
    * View Logic: The document_upload view validates the form, saves the file using Django's default storage backend, and uploads it to AWS S3.
    * File Handling: Uses the Boto3 library to handle file uploads to S3.
    * Feedback: Uses Django’s messaging framework to notify users of successful or failed uploads.

3. Viewing Files (document_view)

    * View Logic: Fetches a list of files from AWS S3 using list_objects_v2.
    * Presentation: Passes the list of files to the template to render them on the user’s view page.
    * Metadata Display: Includes information such as file name, URL, size, and last modified date.

4. Deleting Files (document_delete)

    * View Logic: Accepts a POST request containing the S3 key of the file to be deleted.
    * AWS Interaction: Uses the Boto3 client’s delete_object method to remove the specified file from the S3 bucket.
    * Security: Ensures that only authenticated users can perform deletion actions.

5. Downloading Files (serve_document)

    * View Logic: Retrieves the file from AWS S3 using download_fileobj and streams it back to the user.
    * HTTP Response: Constructs a response object with the file content and sets the appropriate headers for downloading.


## Component Design

The Cloud Drive application is structured into several components:
1. Web Tier

    * Front-End: HTML templates using Django’s templating engine to render pages.
    * Pages: Includes registration, login, file upload form, list of uploaded files, and download pages.
    * User Interface: Uses Bootstrap for responsive design and styling.

2. Application Tier

    * Django Views: Handles HTTP requests and manages business logic.
    * Forms: Manages user inputs and validation for registration and file uploads.
    * Error Handling: Uses Django’s messaging framework to provide feedback to users for various operations.

3. Database Tier

    * Database: SQLite3 for user information storage.
    * User Data: Stores user credentials such as username, email, and hashed password.

4. Storage Tier

    * AWS S3: Stores user-uploaded files, ensuring high availability and scalability.
    * Boto3: Python SDK used for interacting with S3 for upload, download, and delete operations.

## Deployment Design
1. AWS EC2 Deployment

    * The application is hosted on an EC2 instance, providing a public IP address for external access.
    * Django runs on the EC2 instance using gunicorn or uWSGI as the application server.

2. Static and Media Files

    * Static Files: Managed using django-storages with S3 as the backend, ensuring that CSS, JavaScript, and other static files are served efficiently.
    * Media Files: User-uploaded files are stored in the AWS S3 bucket.

3. Security Measures

    * Environment variables managed securely using python-dotenv for AWS credentials.
    * Implements Django’s built-in CSRF protection for form submissions.


## Setup and Configuration

### Prerequisites
- Python 3.8 or later
- AWS Account and S3 Bucket
- Boto3 and Django Storages Library


List of Python packages required for the project as specified in the `requirements.txt`:

- asgiref==3.8.1
- boto3==1.35.43
- botocore==1.35.43
- Django==5.1.2
- django-storages==1.14.4
- jmespath==1.0.1
- python-dateutil==2.9.0.post0
- python-dotenv==1.0.1
- s3transfer==0.10.3
- six==1.16.0
- sqlparse==0.5.1
- urllib3==2.2.3

## Installation Instructions

1. Clone the repository 
    ```bash
    https://github.com/Tony363/5517.git
    cd myproject
    ```
2. To install these dependencies, navigate to the project directory in your terminal and run the following command:

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

    This command will automatically install all the packages listed in the `requirements.txt` file along with their dependencies.

3. **Configure AWS Credentials**:
   Store your AWS credentials in an environment file `.env` located at `5517/myproject/myproject/aws_secrets.env`. This should contain:
   ```
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   ```

4. **Update `settings.py`**:
   Ensure the settings for AWS S3 in `settings.py` match your AWS configuration, especially `AWS_STORAGE_BUCKET_NAME` and `AWS_S3_REGION_NAME`.

## Running the Application

1. **Set Up the Database**:
   Run migrations to set up your database schema:
   ```bash
   python manage.py migrate
   ```

2. **Create Superuser**:
   Create an administrative user to access the Django admin:
   ```bash
   python manage.py createsuperuser
   ```

3. **Run the Server**:
   Start the development server on your local machine:
   ```bash
   python manage.py runserver
   ```
   This will start the server on `http://127.0.0.1:8000/` by default.






