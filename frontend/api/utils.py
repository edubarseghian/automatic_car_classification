import hashlib
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


def allowed_file(filename):
    """
    Checks if the format for the file received is acceptable. For this
    particular case, we must accept only image files. This is, files with
    extension ".png", ".jpg", ".jpeg" or ".gif".

    Parameters
    ----------
    filename : str
        Filename from werkzeug.datastructures.FileStorage file.

    Returns
    -------
    bool
        True if the file is an image, False otherwise.
    """
    # Current implementation will allow any kind of file.
    # TODO
    # return '.' in filename and \
    #filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    imgExtensions = ['.png', '.jpg', '.jpeg', '.gif']

    #filename = secure_filename(file.filename)
    if filename != '':
        file_ext = str.lower(os.path.splitext(filename)[1])
        if file_ext not in imgExtensions:
            return False
        else:
            return True
    # split_name = filename.split('.')
    # print(str(split_name[1]))
    # if split_name[1] == 'png' or split_name[1] == 'jpg' or split_name[1] == 'jpeg' or split_name[1] == 'gif':
    #     return True
    # else:
    #     return False


def get_file_hash(file):
    """
    Returns a new filename based on the file content using MD5 hashing.
    It uses hashlib.md5() function from Python standard library to get
    the hash.

    Parameters
    ----------
    file : werkzeug.datastructures.FileStorage
        File sent by user.

    Returns
    -------
    str
        New filename based in md5 file hash.
    """
    # Current implementation will return the original file name.
    # TODO

    split_name = file.filename
    split_name = split_name.split('.')
    filemd5 = hashlib.md5()
    filemd5.update(file.read())
    filemd5name = filemd5.hexdigest()
    #filename = secure_filename(file.filename)
    file.seek(0)
    file.filename = secure_filename(filemd5name + '.' + split_name[1])
    return file.filename


#a = allowed_file('/usr/src/dog./')
