from PIL import Image
from django.core.files.base import ContentFile

import base64, secrets, io

from django.db.models import Q
from product.models import ProductAttributes, ProductImage\
                            , CategoryProduct, Category, Product

def save_attribute(attributes, product):

    for attr in attributes:
        is_main = str(attr['is_main']).capitalize()
        key = attr['key']
        label = attr['label']
        value = attr['value']
        ProductAttributes.objects.create(is_main=is_main, key=key, label=label, value=value, product_id=product.id)


def get_image_from_data_url( data_url, resize=True, base_width=600 ):

    # getting the file format and the necessary dataURl for the file
    _format, _dataurl       = data_url.split(';base64,')
    # file name and extension
    _filename, _extension   = secrets.token_hex(20), _format.split('/')[-1]

    # generating the contents of the file
    file = ContentFile( base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")

    # resizing the image, reducing quality and size
    if resize:

        # opening the file with the pillow
        image = Image.open(file)
        # using BytesIO to rewrite the new content without using the filesystem
        image_io = io.BytesIO()

        # resize
        w_percent = (base_width/float(image.size[0]))
        h_size = int((float(image.size[1])*float(w_percent)))
        image = image.resize((base_width,h_size), Image.ANTIALIAS)

        # save resized image
        image.save(image_io, format=_extension)

        # generating the content of the new image
        file = ContentFile( image_io.getvalue(), name=f"{_filename}.{_extension}" )

    # file and filename
    return file, (_filename, _extension)


def save_image(images, product):

    for image in images:
        ProductImage.objects.create(images=get_image_from_data_url(image)[0], product_id=product.id)


def save_category(categories, product):

    for category in categories:
        CategoryProduct.objects.create(category_id=category, product_id=product.id)


def get_attributes(id):
    attributes = []
    for attribut in ProductAttributes.objects.filter(product=id):
        attributes.append(
            {
                "id": attribut.id,
                "is_main": attribut.is_main,
                "key": attribut.key,
                "label": attribut.label,
                "value": attribut.value,
                "created_at": attribut.created_at,
            }
        )
    return attributes


def get_images(product):
    images = []
    for image in ProductImage.objects.filter(product_id=product.id):
        images.append("http://127.0.0.1:8000" + image.images.url)

    return images


def get_categories(product):
    categories = []
    for category in CategoryProduct.objects.filter(product_id=product.id):
        category = Category.objects.get(id=category.category_id)
        categories.append({
            "id": category.id,
            "name": category.name,
        })

    return categories


def get_available_colors_and_sizes(id):
    available_colors = []
    available_sizes = []
    for product in Product.objects.filter(Q(parent_id=id) | Q(id=id)):
        for attribute in ProductAttributes.objects.filter(product=product):
            if attribute.key == 'size':
                available_sizes.append({
                    "product_id": product.id,
                    "size": attribute.value
                })
            elif attribute.key == 'color':
                available_colors.append({
                    "product_id": product.id,
                    "color": attribute.value,
                    "image": "http://127.0.0.1:8000" + product.image.url,
                })
    return available_colors, available_sizes
