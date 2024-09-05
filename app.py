import streamlit as st
import requests

# Streamlit App
st.title('Prompt to Character Generator')

# Text input for prompt
prompt = st.text_input('Enter a prompt:')

# Text input for image URL (instead of file uploader)
image_url = st.text_input('Enter the Image URL:')

# Add a button to generate the image
if st.button('Generate'):
    if prompt.strip():  # Check if prompt is not empty
        if image_url.strip():  # Check if the image URL is not empty
            # Prepare the API request body
            request_body = {
                "input": {
                    "style": "CCW",
                    "input_image": image_url,  # Use the image URL instead of base64 string
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
                    
                    # Display the API result (json output)
                    st.subheader("API Response Details:")
                    # st.json(result)  # Show the entire JSON response
                    
                    # Extract the image URL from the "output" array
                    generated_image_url = result.get('output')[0]  # First image URL in the output array
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
            st.error('Please enter a valid image URL.')
    else:
        st.error('Prompt cannot be empty. Please enter a prompt.')