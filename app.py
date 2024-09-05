import streamlit as st
from PIL import Image
import io
import requests
import base64

# Function to convert image to base64 and prefix with image type
def image_to_base64(img, img_format):
    buffer = io.BytesIO()
    img.save(buffer, format=img_format)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/{img_format.lower()};base64,{img_base64}"

# Streamlit App
st.title('Prompt to Character Generator')

# Text input for prompt
prompt = st.text_input('Enter a prompt:')

# File uploader for character sheet (required)
uploaded_image = st.file_uploader("Upload Character Sheet", type=["png", "jpg", "jpeg"], label_visibility="visible")

# Add a button to generate the image
if st.button('Generate'):
    if prompt.strip():  # Check if prompt is not empty
        if uploaded_image:
            # Open the uploaded image
            img = Image.open(uploaded_image)
            img_format = uploaded_image.type.split('/')[-1]  # Get the image format

            # Convert uploaded image to base64 with format prefix
            img_base64 = image_to_base64(img, img_format)
            
            # Prepare the API request body
            request_body = {
                "input": {
                    "style": "CCW",
                    "input_image": img_base64,  # Send base64 string with proper format prefix
                    "prompt": prompt
                }
            }
            
            # Define the API endpoint and headers
            api_url = 'https://api.runpod.ai/v2/n69pdfbq22wy82/run'
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
                    # Assuming the API returns a URL to the generated image
                    generated_image_url = result.get('output_image_url')
                    if generated_image_url:
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
            st.error('Please upload a character sheet image. It is required.')
    else:
        st.error('Prompt cannot be empty. Please enter a prompt.')