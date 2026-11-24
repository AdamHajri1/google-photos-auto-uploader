\# Google Photos Auto Uploader



A Python-based Windows application that automatically uploads photos from a local folder to Google Photos.



\## Features



\- Automatically detects new photos in a selected folder.

\- Uploads photos to Google Photos using the Google Photos API.

\- Detects duplicate files using SHA-256 hashing.

\- Runs automatically when Windows starts using Task Scheduler.

\- Keeps original photos on the computer.

\- Remembers successfully uploaded photos.



\## Technologies Used



\- Python

\- Google Photos API

\- OAuth 2.0

\- Google Authentication

\- Requests

\- Windows Task Scheduler



\## Project Structure



```text

cloud-storage/

├── auto\_uploader.py

├── test\_login.py

├── test\_upload.py

├── requirements.txt

├── README.md

└── .gitignore

```



\## Requirements



\- Windows 10 or Windows 11

\- Python 3

\- Git

\- A Google account

\- Google Cloud project with the Google Photos API configured



\## Installation



1\. Clone this repository:



```bash

git clone YOUR\_REPOSITORY\_URL

```



2\. Open the project folder:



```bash

cd YOUR\_REPOSITORY\_NAME

```



3\. Install the dependencies:



```bash

pip install -r requirements.txt

```



4\. Configure Google OAuth credentials and place your `client\_secret.json` in the project folder.



5\. Run the login script:



```bash

python test\_login.py

```



6\. Start the automatic uploader:



```bash

python auto\_uploader.py

```



\## Usage



Place your photos inside the `AutoUpload` folder.



The application checks the folder periodically and uploads new photos to Google Photos.



Successfully uploaded files are recorded to prevent duplicate uploads.



\## Privacy and Security



\- Original photos are never deleted automatically.

\- Google credentials and authentication tokens must remain private.

\- Personal photos and upload history are excluded from Git.



\## Important



This project is designed for personal photo backup. Google Photos API access and storage quotas apply.



\## Author



Developed as a personal Python automation project.

