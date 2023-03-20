# PyConvertAPI Image Converter
![GitHub MIT License](https://img.shields.io/github/license/ti-oluwa/pyconvertapi_image_converter?color=%23E1e5&style=plastic)
![Languages used](https://img.shields.io/github/languages/top/ti-oluwa/pyconvertapi_image_converter)
![Code size](https://img.shields.io/github/languages/code-size/ti-oluwa/pyconvertapi_image_converter)
![Utilities](https://img.shields.io/badge/Utilities-1-blue?style=for-the-badge)

PyConvertAPI Image Converter is a Python library for converting images to different formats using [ConvertAPI](https://www.convertapi.com/). ConvertAPI is a cloud based file conversion API. It allows you to convert files from one format to another. It supports over 200 different file formats and conversion types. ConvertAPI is a paid service. You can sign up for a free account and get 100 free conversions per month. You can also get a paid account with more conversions per month. You can find more information about ConvertAPI at [https://www.convertapi.com/](convertapi.com).

## Installation
* Ensure you have python3 and pip installed on your system.
* You can the install PyConvertAPI Image Converter using pip:

```bash
pip install pyconvertapi-image-converter
```

## Usage

### Importing the library
To use the library, you need to import it into your project. You can import the library using the following code:

```python
import pyconvertapi_image_converter
```


### Creating a ConvertAPIImageConverter object
To create a ConvertAPIImageConverter object as well to as convert an image, you need to provide your ConvertAPI secret. You can get your ConvertAPI secret from your ConvertAPI account. You can create a ConvertAPIImageConverter object using the following code:

```python
from pyconvertapi_image_converter import ConvertAPIImageConverter

# Create a ConvertAPIImageConverter object
converter = ConvertAPIImageConverter('your_secret')

# Convert an image to PNG format
converter.convert(path='path/to/image.jpg', to_format='png')

# Convert an image to SVG format
converter.convert(path='path/to/image.jpeg', to_format='svg')
```


### Converting all images in a directory
To convert all images in a directory, you can use the following code:

```python
from pyconvertapi_image_converter import ConvertAPIImageConverter

converter = ConvertAPIImageConverter('your_secret')

# Convert all images in a directory to PNG format
converter.convert('path/to/directory', to_format='png')
```


### Supported formats
To get a list of supported formats, you can use the following code:
```python
from pyconvertapi_image_converter import to_formats, from_formats

# Get a list of supported formats for input files
print(from_formats)

# Get a list of supported formats for output files
print(to_formats)
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Contributing
Pull requests and feedbacks are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors and acknowledgment

* [**ti-oluwa**](https://github.com/ti-oluwa) ![Twitter Follow](https://img.shields.io/twitter/follow/ti_oluwa_?style=social)
* [**ConvertAPI**](https://www.convertapi.com/)
* [**ConvertAPI Python Client**](https://github.com/ConvertAPI/convertapi-python)
