# Cloudinary Image Moderation with Status Notifications

This repository contains a Flask web application that use Cloudinary with WebPurify add-on, to perform image moderation upon image uploading, and get live status notifications about the moderation of an image.

## Purpose

The application serves as a demostration of how to:
- Upload images to Cloudinary
- Moderation images with WebPurify
- Get status notifications using Ngrok, SocketIO and Bootstrap

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Cloudinary Python SDK
- Ngrok

### Installation

1. Clone this repository
2. Install dependencies using `pip install -r requirements.txt`
3. Set up your Cloudinary account and get API credentials, [Cloudinary Integration Documentation](https://cloudinary.com/documentation/how_to_integrate_cloudinary#landingpage)
4. Create a `.env` file and add your Cloudinary credentials:
```
CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>
```
5. Subscribe to the [WebPurify add-on](https://cloudinary.com/addons#webpurify)
6. Create a webhook URL using Ngrok and add it to `app.py` to the `notification_url` in the `upload` function

### Running the Application

1. Run the Flask app: `python app.py`
2. Access the application via your web browser at [http://loclahost:5001](http://localhost:5001)

## Functionality

- Navigate to the homepage and select an image file to upload
- The uploaded image undergoes the WebPurify moderation
- As soon as the upload happened, a toast notification will appear that shows, that the image is waiting for moderation
- When the moderation status of the image changes, the notification will change to either approved or to rejected status
- Upon successful approved moderation, after a refresh, the image will appear on the site
- In case the iamge has been rejected, you can see the list of rejected image IDs by clicking the 'Check Rejected Images'
