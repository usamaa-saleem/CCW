import streamlit as st
import requests
import firebase_admin
from firebase_admin import credentials, storage
import tempfile
import os

# Initialize Firebase Admin SDK
def initialize_firebase():
    cred = credentials.Certificate('ccw-production-3c9b8-firebase-adminsdk-gxree-299a765cca.json')  # Path to your Firebase service account key
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'ccw-production-3c9b8.appspot.com'  # Replace with your Firebase Storage bucket name
    })

# Upload image to Firebase Storage and get the URL
def upload_to_firebase(file):
    bucket = storage.bucket()
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file.read())
        temp_file.flush()
        temp_file.seek(0)
        blob = bucket.blob(f'uploaded-images/{os.path.basename(temp_file.name)}')
        blob.upload_from_filename(temp_file.name)
        blob.make_public()  # Make the file publicly accessible
        public_url = blob.public_url
        
    # Clean up temporary file
    os.remove(temp_file.name)
    
    return public_url

# Initialize Firebase (only once)
if not firebase_admin._apps:
    initialize_firebase()

# Streamlit App
st.title('Prompt to Character Generator')

# Text input for prompt
prompt = st.text_input('Enter a prompt:')

# File uploader for image upload
uploaded_image = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])

# Add a button to generate the image
if st.button('Generate'):
    if prompt.strip():  # Check if prompt is not empty
        if uploaded_image is not None:  # Check if an image has been uploaded
            # Upload the image to Firebase Storage and get the URL
            image_url = upload_to_firebase(uploaded_image)
            
            # Prepare the API request body
            request_body = {
                "input": {
                    "style": "CCW",
                    "input_image": image_url,  # Use the cloud storage URL
                    "prompt": prompt
                }
            }
            
            # Define the API endpoint and headers
            api_url = 'https://api.runpod.ai/v2/n69pdfbq22wy82/runsync'
            headers = {
                'Authorization': 'Bearer XZSJTQHX9WARNU6ZTIOF42VEZWI76RI9DE0RE3EC',
                'Content-Type': 'application/json'
            }
            
            # Send the request to the API
            try:
                response = requests.post(api_url, json=request_body, headers=headers)
                
                # Check if the response is successful
                if response.status_code == 200:
                    result = response.json()
                    
                    # Extract the image URL from the "output" array
                    generated_image_url = result.get('output')[0]  # First image URL in the output array
                    if generated_image_url:
                        # Display the generated image
                        st.image(generated_image_url, caption=f"Generated for: {prompt}")
                    else:
                        st.error('Failed to get the image URL from the response.')
                else:
                    # Handle error response
                    error_info = response.json()
                    st.error(f"Error {response.status_code}: {error_info.get('message', 'An unexpected error occurred.')}")
            
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {str(e)}")
        else:
            st.error('Please upload an image.')
    else:
        st.error('Prompt cannot be empty. Please enter a prompt.')