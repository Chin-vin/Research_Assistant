import os


UPLOAD_DIR = "uploaded_pdfs"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


def save_uploaded_file(uploaded_file):

    file_path = os.path.join(
        UPLOAD_DIR,
        uploaded_file.name
    )

    with open(file_path, "wb") as f:

        f.write(uploaded_file.read())

    return file_path