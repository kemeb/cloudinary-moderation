from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO
from cloudinary import CloudinaryImage
import cloudinary
import cloudinary.api
import cloudinary.uploader

load_dotenv()
app = Flask(__name__)
socketio = SocketIO(app)
config=cloudinary.config(secure=True)

# Fetch the images from a specific folder and apply transformation/optimisation
def get_transformed_images():
    all_images = cloudinary.Search().expression('folder:public_gallery').sort_by('public_id', 'desc').max_results(10).execute()
    transformed_images = []
    for item in all_images["resources"]:
        public_id = item['public_id']
        cloudinary_image = CloudinaryImage(public_id)
        image_url = cloudinary_image.build_url(transformation=[
            {'width': 400, 'height': 400, 'crop': 'fill'},
            {'fetch_format': 'auto', 'quality': 'auto'}
        ])
        transformed_images.append(image_url)
    return transformed_images

# Route for homepage to display the images
@app.route('/')
def index():
    transformed_images = get_transformed_images()
    return render_template('index.html', transformed_images=transformed_images)

# Image upload with moderation
@app.route('/upload', methods=['POST'])
def upload():
    files_to_upload = request.files.getlist('file')
    for file_item in files_to_upload:
        if file_item:
            cloudinary.uploader.upload(file_item, 
                                       folder = "public_gallery", 
                                       moderation = "webpurify",
                                       notification_url = 'YOUR_NGROK_URL/status_notification'
                                       )
            
    return redirect(url_for('index'))

# Notify about the moderation status of the image with ngrok
@app.route('/status_notification', methods=['POST'])
def status_notification():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"status": "No data received"}), 400

    # Check for 'moderation' key in data
    if 'moderation' in data:
        status = data['moderation'][0].get('status')
        socketio.emit('moderation', {'status': 'pending'})
    # Check for specific keys in data and 'approved' status
    elif ( data['moderation_status'] == 'approved'):
        socketio.emit('moderation', {'status': 'approved'})
    else:
        socketio.emit('moderation', {'status': 'rejected'})
        return jsonify({"status": "Invalid data structure"}), 400

    return jsonify({"status": "Received"}), 200

# Check for rejected images
@app.route('/rejected_images', methods=['GET', 'POST'])
def rejected_images():
    rejected_images = []
    if request.method == 'POST':
        results = cloudinary.api.resources_by_moderation("webpurify", "rejected")
        for img in results['resources']:
            image_info = img['public_id'].split('/')[-1]
            rejected_images.append(image_info)

    transformed_images = get_transformed_images()
    return render_template('index.html', transformed_images=transformed_images, rejected_images=rejected_images)

               
if __name__ == '__main__':
    app.run(debug=True, port=5001)
    