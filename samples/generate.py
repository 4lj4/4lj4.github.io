import os
import markdown2

def convert_markdown_to_html(md_file_path):
    if not md_file_path.endswith(".md"):
        raise ValueError("Input file must have a .md extension")
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()
    html_content = markdown2.markdown(
        md_content,
        extras=[
            'fenced-code-blocks',  # Improved handling of code blocks
            'code-friendly',       # Additional code formatting improvements
            'tables',              # Table support
            'smarty-pants',        # Smart typography, e.g., "quotes"
            'footnotes',           # Footnotes support
            'cuddled-lists',       # Improved list formatting
            'toc',                 # Table of Contents
            'task_list',           # Task list items
        ]
    )
    output_html_path = os.path.splitext(md_file_path)[0] + ".html"
    with open(output_html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

def parse_info_file(info_file):
    info_dict = {}
    with open(info_file, 'r') as f:
        for line in f:
            key, value = line.strip().split(':', 1)
            info_dict[key.strip()] = value.strip()
    return info_dict

def generate_html(sample_path, info_file, zip_file, analysis_guide):
    sample_info = parse_info_file(info_file)

    # Generate HTML for each sample
    html_content = f"""
    <div>
        <h2>{os.path.basename(sample_path)}</h2>
        <p><strong>Author:</strong> {sample_info.get('Author', 'N/A')}</p>
        <p><strong>Date:</strong> {sample_info.get('Date', 'N/A')}</p>
        <p><strong>Notes:</strong> {sample_info.get('Notes', 'N/A')}</p>
        <p><strong>C2 Status:</strong> {sample_info.get('C2 Status', 'N/A')}</p>
        <p><strong>SHA256:</strong> {sample_info.get('SHA256', 'N/A')}</p>
        <a href="{zip_file}" download>Download Sample (Encrypted zip, pass:infected)</a>
        <a href="{analysis_guide}" download>View analysis guide</a>
    </div>
    """

    return html_content

def generate_index_html():
    files_directory = "sample-files"
    output_html = "index.html"

    with open(output_html, 'w') as index_file:
        # Write the entire HTML structure
        index_file.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LJ4's samples</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            margin: 20px;
        }

        h1 {
            color: #333;
        }

        div {
            background-color: #fff;
            border: 1px solid #ddd;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }

        a {
            display: inline-block;
            padding: 10px;
            margin-top: 10px;
            background-color: #4285f4;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
        }

        a:hover {
            background-color: #3367d6;
        }
    </style>
</head>
<body>
    <h1>Malicious software samples found in the wild</h1>
    <h2>DO NOT DOWNLOAD IF YOU DO NOT KNOW EXACTLY WHAT YOURE DOING</h2>
    """)

        # Iterate through each sample in the "files" folder
        for sample_folder in os.listdir(files_directory):
            sample_path = os.path.join(files_directory, sample_folder)
            info_file = os.path.join(sample_path, "info.txt")
            zip_file = os.path.join(sample_path, f"{sample_folder}.zip")
            analysis_guide = os.path.join(sample_path, "analysis.html")
            convert_markdown_to_html(os.path.join(sample_path, "analysis.md"))

            if os.path.isdir(sample_path) and os.path.exists(info_file) and os.path.exists(zip_file):
                # Append HTML content for each sample
                index_file.write(generate_html(sample_path, info_file, zip_file, analysis_guide))

        # Write the closing part of the HTML
        index_file.write("</body></html>")

def main():
    generate_index_html()

if __name__ == "__main__":
    main()