# Python script to convert JSON to HTML
import os
import json
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()


def resize_and_convert_images(original_dir, target_dir):
    # Clear the target directory
    if os.path.exists(target_dir):
        for root, dirs, files in os.walk(target_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
    os.makedirs(target_dir, exist_ok=True)

    for subdir, _, files in os.walk(original_dir):
        relative_path = os.path.relpath(subdir, original_dir)
        target_subdir = os.path.join(target_dir, relative_path)
        os.makedirs(target_subdir, exist_ok=True)

        for i, file in enumerate(files):
            if file.lower().endswith(('.heic', '.jpg', '.jpeg', '.png', '.gif')):
                source_path = os.path.join(subdir, file)
                target_file_name = f"{os.path.basename(relative_path)}_{i + 1}.jpg"
                target_path = os.path.join(target_subdir, target_file_name)

                try:
                    with Image.open(source_path) as img:
                        img = img.convert('RGB')  # Ensure compatibility
                        img.thumbnail((1000, 1000))  # Resize to 1000px on the longest edge
                        img.save(target_path, 'JPEG', quality=85)
                except Exception as e:
                    print(f"Failed to process {source_path}: {e}")


def generate_html(json_file, output_file):
    # Load JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # HTML Template
    html = """<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Portfolio</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            color: #333;
            margin: 0;
            padding: 0;
        }
        .container {
            width: 90%;
            margin: 20px auto;
        }
        .header {
            text-align: left;
            margin-bottom: 40px;
        }
        .header a {
            text-decoration: none;
            color: #2d6a4f;
            font-size: 2em;
            font-weight: bold;
        }
        .project {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            margin-bottom: 20px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            position: relative;
        }
        .project h2 {
            color: #2d6a4f;
            margin: 0;
        }
        .project-category {
            font-size: 0.8em;
            color: #6c757d;
            position: absolute;
            top: 20px;
            right: 20px;
        }
        .project-images {
            display: flex;
            overflow-x: auto;
            gap: 10px;
        }
        .project-images img {
            height: 150px;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            cursor: pointer;
            transition: transform 0.3s;
        }
        .project-images img:hover {
            transform: scale(1.1);
        }
        .project-description {
            margin-top: 10px;
        }
        #image-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        #image-modal img {
            max-width: 90%;
            max-height: 90%;
        }
    </style>
    <script>
        function openImage(src) {
            const modal = document.getElementById('image-modal');
            const modalImg = modal.querySelector('img');
            modalImg.src = src;
            modal.style.display = 'flex';
        }
        function closeImage() {
            const modal = document.getElementById('image-modal');
            modal.style.display = 'none';
        }
    </script>
</head>
<body>
    <div id=\"image-modal\" onclick=\"closeImage()\">
        <img src=\"\" alt=\"\">
    </div>
    <div class=\"container\">
        <div class=\"header\">
            <a href=\"http://samcooler.com\">Sam Cooler</a>
        </div>
"""

    # Add projects to HTML
    for project in data['projects']:
        # Scan images directory
        images_dir = os.path.join('images', project['shortname'])
        project_images = []
        if os.path.exists(images_dir):
            project_images = [img for img in os.listdir(images_dir) if img.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

        html += f"""
        <div class=\"project\">
            <h2>{project['title']}</h2>
            <div class=\"project-category\">{project['category']}</div>
            <p><strong>{project['short_description']}</strong></p>
            <p class=\"project-description\">{project['long_description']}</p>
            <div class=\"project-images\">
        """
        # Add images
        for image in project_images:
            image_path = f"images/{project['shortname']}/{image}"
            html += f'<img src=\"{image_path}\" alt=\"{project["title"]} image\" onclick=\"openImage(\'{image_path}\')\">'

        html += "</div></div>"

    # Close HTML
    html += """
    </div>
</body>
</html>
"""

    # Write to output file
    with open(output_file, 'w') as f:
        f.write(html)


# Resize and convert images
resize_and_convert_images('images_original', 'images')

# Generate HTML
generate_html('projects.json', 'portfolio.html')
