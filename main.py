import uvicorn
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import base64
from checker import *
import json

def print_temp_folder_contents(root_folder):
    if os.path.exists(root_folder):
        print(f"\nFolder structure starting from '{root_folder}':")
        for root, dirs, files in os.walk(root_folder):
            level = root.replace(root_folder, '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}[{os.path.basename(root)}]")
            subindent = ' ' * 4 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")
    else:
        print(f"The folder '{root_folder}' does not exist.")

# Define folder names
folders_to_create = ["temp", "temp_images", "temp_images/Preliminaries/", "temp_images/Chapter 1/", "temp_images/Chapter 2/", "temp_images/Chapter 3/", "temp_images/Chapter 4/", "temp_images/Chapter 5/", "temp_images/Bibliography/"]

def create_folders_print_structure(folders_list):
    for folder_name in folders_list:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"Created folder: {folder_name}")
        else:
            print(f"Folder '{folder_name}' already exists.")

create_folders_print_structure(folders_to_create)

def print_root_dir(root_folder):
    if os.path.exists(root_folder):
        print(f"\nFolder structure starting from '{root_folder}':")
        for root, dirs, files in os.walk(root_folder):
            level = root.replace(root_folder, '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}[{os.path.basename(root)}]")
            subindent = ' ' * 4 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")
    else:
        print(f"The folder '{root_folder}' does not exist.")

root_folder = "temp"
print_root_dir(root_folder)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to UMak CS Thesis Checker API"}

@app.post("/upload")
async def analyze_pdf(pdf_file: UploadFile, selection: str = Form(...), preset: str = Form(...)):
    # Check if a file was uploaded
    if pdf_file is None:
        return {"Error": 'No PDF file is uploaded.'}

    # Check if the file has a PDF file extension
    if not pdf_file.filename.endswith(".pdf"):
        return {"Error": 'The uploaded file is not a PDF.'}

    # Save the uploaded PDF file to a temporary location
    file_path = os.path.join("temp", pdf_file.filename)
    with open(file_path, "wb") as temp_file:
        temp_file.write(pdf_file.file.read())

    pdf_path = f'temp\{pdf_file.filename}'

    # Check and GET DATABASE values 
    decoded_data = json.loads(preset)
        # Extracting values and assigning them to variables
    data = decoded_data[0]  # Assuming there's only one item in the list
    font_family = data['font_family']
    spacings_result = data['spacings']
    margins_json = json.loads(data['margins_json'])
    margins = {
        'margin_top': float(margins_json['margin_top']),
        'margin_left': float(margins_json['margin_left']),
        'margin_right': float(margins_json['margin_right']),
        'margin_bottom': float(margins_json['margin_bottom'])
    }

    font_family = getFontStyle(font_family)

    # Run font detection on the uploaded PDF file to get a list of image paths
    image_paths, errors = analyzePDF(pdf_path, font_family, spacings_result, margins, selection)

    if isinstance(image_paths, str):
        return f"Error: {image_paths}"

    result = cluster_errors(errors)

    image_data_list = []  # list to store base64-encoded image data for each page

    for image_path in image_paths:
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
            image_data_list.append(image_data)

    # Return the image data as JSON response
    return {"image_data_list": image_data_list, "errors" : result}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)