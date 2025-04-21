import streamlit as st
import os
from PIL import Image
import io
import matplotlib.pyplot as plt

# Title of the web app
st.title("🖼️ Image Upload, Process & Generate Code")

# Description for the app
st.markdown("""
### 🚀 Welcome to the Image Uploader + Analyzer App!
- Upload your image to view format, size, resolution and try simple image processing tools.
- You can even download the processed image.
""")

# Directory where uploaded images will be saved
upload_directory = 'uploaded_files'

# Create directory if it doesn't exist
if not os.path.exists(upload_directory):
    os.makedirs(upload_directory)

# File uploader
uploaded_file = st.file_uploader("📁 Choose an image", type=["jpg", "jpeg", "png", "gif"])

if uploaded_file is not None:
    # Save the uploaded image
    file_path = os.path.join(upload_directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load image using PIL
    image = Image.open(uploaded_file)

    # Display original image
    st.subheader("🖼️ Uploaded Image Preview")
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Image Metadata
    st.markdown("### 📊 Image Info")
    st.write(f"**Filename:** `{uploaded_file.name}`")
    st.write(f"**Format:** `{image.format}`")
    st.write(f"**Mode:** `{image.mode}`")
    st.write(f"**Resolution:** {image.size[0]}x{image.size[1]}")
    image_size = os.path.getsize(file_path) / 1024
    st.write(f"**Size:** {image_size:.2f} KB")

    # Optional: Convert to Grayscale
    if st.checkbox("Convert to Grayscale"):
        gray_img = image.convert("L")
        st.image(gray_img, caption="🖤 Grayscale Image", use_column_width=True)

        # Download grayscale image
        buf = io.BytesIO()
        gray_img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button(
            label="📥 Download Grayscale Image",
            data=byte_im,
            file_name="grayscale_image.png",
            mime="image/png"
        )

    # Optional: Show histogram
    if st.checkbox("📈 Show Image Histogram"):
        st.write("🔍 Histogram (color distribution)")
        plt.figure(figsize=(8, 4))
        plt.title("Histogram")
        if image.mode != "L":
            for i, color in enumerate(["red", "green", "blue"]):
                plt.hist(image.getdata(band=i), bins=256, color=color, alpha=0.5, label=color)
        else:
            plt.hist(image.getdata(), bins=256, color="gray")
        plt.legend()
        st.pyplot(plt)

    # Show generated code
    st.subheader("🧾 Generated Python Code:")
    generated_code = f"""
from PIL import Image

# Load the image
image = Image.open("{uploaded_file.name}")

# Get size
width, height = image.size
print(f"Resolution: {{width}}x{{height}}")

# Image format and mode
print(f"Format: {{image.format}}")
print(f"Mode: {{image.mode}}")

# Optional grayscale conversion
gray = image.convert("L")
gray.save("grayscale_image.png")
"""
    st.code(generated_code, language='python')
else:
    st.info("Upload an image to get started.")
