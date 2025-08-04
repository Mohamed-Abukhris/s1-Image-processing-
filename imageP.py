import os , sys

from PIL import Image

source_photos = 'photos'
destination_photos = 'Jpg_to_Png_Converter'

for filename in os.listdir(source_photos):
    if filename.lower().endswith(('.jpg' ,'.jpeg' )):
        image_path = os.path.join(source_photos, filename)

        image = Image.open(image_path)
        basename = os.path.splitext(filename)[0]
        print(basename)
        new_filename = basename +'.png'

        new_path = os.path.join(destination_photos, new_filename)

        image.save(new_path,"PNG")
        print('converted and moved:{filename}')

print('done')


