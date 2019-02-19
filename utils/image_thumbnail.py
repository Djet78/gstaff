from PIL import Image


def thumbnail(img_path, max_height, max_width):
    """ Cuts image if it's bigger than 'max_height' or 'max_width' """
    im = Image.open(img_path)
    if im.height > max_height or im.width > max_width:
        im.thumbnail((max_height, max_width))
        im.save(img_path)
