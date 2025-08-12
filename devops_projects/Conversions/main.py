import zipfile
import os

folder_to_zip = r"C:\Users\alkam\Desktop\PythonFile\Console-Project"
zip_file_name = r"C:\Users\alkam\Desktop\project_archive.zip"

with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as myzip:
    for foldername, subfolders, filenames in os.walk(folder_to_zip):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            arcname = os.path.relpath(filepath, folder_to_zip)  # keep folder structure
            myzip.write(filepath, arcname)

print(f"✅ Folder '{folder_to_zip}' has been zipped into '{zip_file_name}'")
