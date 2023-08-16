import base64
import pyperclip

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_image

# Provide the path to the image you want to encode
image_path = "images/Input/obama.jpg"
encoded_image = encode_image(image_path)

# Copy the encoded image to the clipboard
pyperclip.copy(encoded_image)

print("Encoded image copied to clipboard.")
