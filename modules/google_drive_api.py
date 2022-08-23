from apiclient import errors, http
from apiclient.discovery import build


def printChildren(parent):
    param = {
        "q": "'"
        + parent
        + "' in parents and mimeType != 'application/vnd.google-apps.folder'"
    }
    result = service.files().list(**param).execute()
    print(type(result))
    print(result)
    files = result.get("files")

    for afile in files:
        print("File {}".format(afile.get("name")))


def print_file_metadata(service, file_id):
    """Print a file's metadata.

    Args:
      service: Drive API service instance.
      file_id: ID of the file to print metadata for.
    """
    try:
        file = service.files().get(fileId=file_id).execute()
        print(file["name"])
        print(file["mimeType"])

    except errors.HttpError as error:
        print(f"An error occurred: {error}")


def print_file_content(service, file_id):
    """Print a file's content.

    Args:
      service: Drive API service instance.
      file_id: ID of the file.

    Returns:
      File's content if successful, None otherwise.
    """
    try:
        print(service.files().get_media(fileId=file_id).execute())
    except errors.HttpError as error:
        print(f"An error occurred: {error}")


def download_file(service, file_id, local_fd):
    """Download a Drive file's content to the local filesystem.

    Args:
      service: Drive API Service instance.
      file_id: ID of the Drive file that will downloaded.
      local_fd: io.Base or file object, the stream that the Drive file's
          contents will be written to.
    """
    request = service.files().get_media(fileId=file_id)
    media_request = http.MediaIoBaseDownload(local_fd, request)

    while True:
        try:
            download_progress, done = media_request.next_chunk()
        except errors.HttpError as error:
            print("An error occurred: %s" % error)
            return
        if download_progress:
            print("Download Progress: %d%%" % int(download_progress.progress() * 100))
        if done:
            print("Download Complete")
            return


API_KEY = ""
FOLDER_ID = ""  # NOTE: folder must be publicly visible when using an API key.
service = build("drive", "v3", developerKey=API_KEY)
metadata = print_file_content(service, "1dYfAlz3wDrwLD6TQOIFkehWe91kpYOQO")
