try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
# Include the above line, if you don't have tesseract executable in your PATH
# Example tesseract_cmd: 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

img = Image.open('kenteken.png')
print(img.getpixel((230,150)))

width, height = img.size

for x in  range(width):
    for y in range(height):
        print('x: {}, y: {}'.format(x, y))


# print(pytesseract.image_to_string(Image.open('screenshot_1.png')))
