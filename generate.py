# Python script to convert JSON to HTML
import os
import json
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

def resize_and_convert_images(original_dir, target_dir):
    # remove existing target directory, recursively removing files and dirs
    if os.path.exists(target_dir):
        import shutil
        shutil.rmtree(target_dir)


    for subdir, _, files in os.walk(original_dir):
        relative_path = os.path.relpath(subdir, original_dir)
        target_subdir = os.path.join(target_dir, relative_path)
        os.makedirs(target_subdir, exist_ok=True)

        for i, file in enumerate(files):
            if file.lower().endswith(('.heic', '.jpg', '.jpeg', '.png', '.gif')):
                source_path = os.path.join(subdir, file)
                # target_file_name = os.path.splitext(file)[0] + '.jpg'
                target_file_name = subdir.split('/')[-1] + '_' + str(i) + '.jpg'
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
        .project img {
            width: 24%;
            margin: 1%;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .project-description {
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class=\"container\">
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
            <div>
        """
        # Add images
        for image in project_images:
            image_path = f"images/{project['shortname']}/{image}"
            html += f'<img src=\"{image_path}\" alt=\"{project["title"]} image\">'

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
