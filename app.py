from flask import Flask, render_template, request, send_file
import os
from PIL import Image
import io
import matplotlib.pyplot as plt

app = Flask(__name__)

# Directory where uploaded images will be saved
upload_directory = 'uploaded_files'

# Create directory if it doesn't exist
if not os.path.exists(upload_directory):
    os.makedirs(upload_directory)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['image']

    if uploaded_file:
        # Save the uploaded image
        file_path = os.path.join(upload_directory, uploaded_file.filename)
        uploaded_file.save(file_path)

        # Load image using PIL
        image = Image.open(file_path)

        # Image Metadata
        image_info = {
            "filename": uploaded_file.filename,
            "format": image.format,
            "mode": image.mode,
            "resolution": f"{image.size[0]}x{image.size[1]}",
            "size": os.path.getsize(file_path) / 1024  # in KB
        }

        # Convert to Grayscale if checked
        gray_img = None
        if request.form.get("grayscale"):
            gray_img = image.convert("L")
            # Save grayscale image
            gray_img_path = os.path.join(upload_directory, 'grayscale_' + uploaded_file.filename)
            gray_img.save(gray_img_path)

        # Histogram
        histogram = None
        if request.form.get("histogram"):
            histogram = plot_histogram(image)

        # Generate Python Code
        generated_code = generate_python_code(uploaded_file.filename)

        return render_template("result.html", image=image, image_info=image_info, grayscale_img=gray_img,
                               histogram=histogram, generated_code=generated_code)

    return "No file uploaded", 400


def plot_histogram(image):
    # Create histogram
    plt.figure(figsize=(8, 4))
    plt.title("Histogram")
    if image.mode != "L":
        for i, color in enumerate(["red", "green", "blue"]):
            plt.hist(image.getdata(band=i), bins=256, color=color, alpha=0.5, label=color)
    else:
        plt.hist(image.getdata(), bins=256, color="gray")
    plt.legend()

    # Save the plot to a BytesIO object to send with response
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf


def generate_python_code(image_filename):
    code = f"""
from PIL import Image

# Load the image
image = Image.open("{image_filename}")

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
    return code


if __name__ == '__main__':
    app.run(debug=True)
