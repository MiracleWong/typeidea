from io import BytesIO
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image, ImageDraw, ImageFont


class WatermarkStorage(FileSystemStorage):
    def save(self, name, content, max_length=None):
        # 处理逻辑
        if 'image' in content.content_type:
            # 加水印
            image = self.watermark_with_text(content, "miraclewong", 'red')
            content = self.convert_image_to_file(image, name)
        return super().save(name, content, max_length)

    def convert_image_to_file(self, image, name):
        temp = BytesIO()
        image.save(temp, format='PNG')
        file_size = image.tell()
        return InMemoryUploadedFile(temp, None, name, 'image/png', file_size, None)

    def watermark_with_text(self, file_obj, text, color, fontfamliy=None):
        image = Image.open(file_obj).convert('RGBA')
        draw = ImageDraw.Draw(image)
        width, height = image.size
        margin = 10
        if fontfamliy:
            font = ImageFont.truetype(fontfamliy, int(height/20))
        else:
            font = None
        text_width, text_heigth = draw.textsize(text, font)
        x = (width - text_width - margin)
        y = (height - text_heigth - margin)

        draw.text((x, y), text, color, font)
        return image
