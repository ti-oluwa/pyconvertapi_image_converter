import os
import concurrent.futures
import convertapi
import time
from typing import Any


to_formats = ['jpg', 'png', 'svg', 'webp', 'tiff']
from_formats = ['jpg', 'png', 'svg', 'jpeg', 'webp', 'tiff', 'jpeg', 'heic', 'ico', 'gif']

class ConvertAPIImageConverter:
    """
    Converts supported image type(s) to specified supported format.

    :param api_secret: convertapi secret key
    :param save_to: path to save converted images to.

    :attribute image_quality: image quality. Defaults to 90
    :attribute image_dpi: image resolution. Defaults to 326
    :attribute api_secret: convertapi secret key
    :attribute _store_files: whether to store converted files on convertapi servers. Defaults to True
    """
    image_quality: int = 90
    image_dpi: int = 326
    _store_files: bool = True
    api_secret: str = None
    save_to: str = None

    def __init__(self, api_secret: str, save_to: str) -> None:
        self.api_secret = api_secret
        self.save_to = os.path.abspath(save_to)

    
    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        self._validate_cls_attrs()


    @classmethod
    def _validate_cls_attrs(cls):
        if cls.api_secret and not isinstance(cls.api_secret, str):
            raise TypeError('Invalid type for api_secret. Should be a string')
        if not isinstance(cls.image_quality, int):
            raise TypeError('Invalid type for image_quality. Should be an integer')
        if not isinstance(cls.image_dpi, int):
            raise TypeError('Invalid type for image_dpi. Should be an integer')
        if not 10 <= cls.image_quality <= 100:
            raise ValueError(f'Invalid value for image_quality. Should be between 10 and 100')
        if not 10 <= cls.image_dpi <= 800:
            raise ValueError(f'Invalid value for image_dpi. Should be between 10 and 800')
        if not isinstance(cls._store_files, bool):
            raise TypeError('Invalid type for _store_files. Should be a boolean')
        if cls.save_to and not isinstance(cls.save_to, str):
            raise TypeError('Invalid type for save_to. Should be a string')

    @property
    def settings(self):
        """
        Image conversion settings.
        """
        settings = {
            "image_resolution_dpi": self.image_dpi,
            "image_quality": self.image_quality,
            "api_secret": self.api_secret,
            "store_files": self._store_files,
            "save_to": self.save_to,
        }
        return settings


    def convert(self, path: str, to_format: str):
        """
        Converts supported image type to specified format.

        :param path: path to the image or directory containing image files
        :param to_format: the format to convert to. Valid values are: 'jpg', 'png', 'svg', 'webp', 'tiff'
        :return: None
        :raises ValueError: if `path` does not point to a file or directory
        """
        path = os.path.abspath(path)
        self.save_to = self.save_to if self.save_to else os.path.dirname(path)
        to_format = to_format.removeprefix('.')

        if os.path.isfile(path):
            return self.convert_image_to(path, to_format)
        if os.path.isdir(path):
            return self.convert_images_to(path, to_format)
        raise ValueError('`path` does not point to a file or directory')


    def convert_image_to(self, path: str, to_fmt: str):
        """
        Convert an image to specified format.

        :param path: path to the image file
        :param to_fmt: the format to convert to. Valid values are: 'jpg', 'png', 'svg', 'webp', 'tiff'
        :return: None
        """
        name, from_fmt = self.get_file_attr(path)
        if not self.validate_formats(to_fmt, from_fmt):
            raise Exception("Unsupported conversion format detected for file: %s" % name)

        if not to_fmt == from_fmt:
            convertapi.api_secret = self.api_secret
            params = {
                'ImageResolution': self.image_dpi,
                'File': path,
                'ImageQuality': self.image_quality,
                'StoreFile': self._store_files
            }
            save_to = os.path.join(self.save_to, name.replace(from_fmt, to_fmt))
            os.makedirs(os.path.dirname(save_to), exist_ok=True)
            f = open(save_to, "w")
            f.close()
            convertapi.convert(to_format=to_fmt, params=params, from_format=from_fmt).save_files(save_to)
        return None

    
    def convert_images_to(self, path: str, to_fmt: str):
        """
        Convert images in a directory to specified format.

        :param path: path to the directory containing the image files
        :param to_fmt: the format to convert to. Valid values are: 'jpg', 'png', 'svg', 'webp', 'tiff'
        :return: None
        """
        image_files = self.get_supported_images_in_dir(path)
        # slice image_files into parts of 10
        image_files_slice = [ image_files[i:i + 10] for i in range(0, len(image_files), 10) ]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for img_files in image_files_slice:
                executor.map(lambda args: self.convert_image_to(*args), [ (path, to_fmt) for path in img_files ])
                time.sleep(3)
        return None


    @staticmethod
    def get_file_attr(file_path: str):
        """
        Get file name and format from file path.

        :param file_path: path to the file
        :return: tuple of file name and format
        """
        filename = os.path.basename(file_path)
        file_format = os.path.splitext(file_path)[1].removeprefix('.')
        return filename, file_format


    @staticmethod
    def validate_formats(to_fmt:str, from_fmt: str):
        """
        Validate conversion formats.

        :param to_fmt: format to convert to
        :param from_fmt: format to convert from
        :return: True if formats are valid, False otherwise
        """
        if to_fmt in to_formats and from_fmt in from_formats:
            return True
        return False


    def get_supported_images_in_dir(self, dir_path: str):
        """
        Returns a list of supported images in a directory.

        :param dir_path: path to the directory
        :return: list of supported images in the directory
        """
        dir_contents = os.listdir(dir_path)
        dir_files = filter(lambda content: os.path.isfile(f"{dir_path}/{content}"), dir_contents)
        dir_images = []
        for file in dir_files:
            file_path = os.path.join(dir_path, file)
            _, fmt = self.get_file_attr(file_path)
            if fmt in from_formats:
                dir_images.append(file_path)
        return dir_images

