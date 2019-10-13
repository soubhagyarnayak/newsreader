import os

from PIL import Image

class ImageUtility:
    
    def trim(self,src_image,convert_to_black_white):
        """
        Trims an image i.e. removes similar pixels from all sides.
        If convert_to_black_white is specified, then the image is first processed to have better result
        """
        (bitmaps,X,Y) = self.load_bitmap(src_image, convert_to_black_white)
        (x_left,y_top,x_right,y_bottom) = (0,0,X,Y)

        all_white = True
        while True:
            for y in range(y_top+1,y_bottom):
                if bitmaps[x_left,y] != bitmaps[x_left,y_top]:
                    all_white = False
                    break
            if all_white:
                x_left += 1
            else:
                break
        all_white = True

        while True:
            for y in range(y_top+1,y_bottom):
                if bitmaps[x_right-1,y] != bitmaps[x_right-1,y_top]:
                    all_white = False
                    break
            if all_white:
                x_right -= 1
            else:
                break
        all_white = True

        while True:
            for x in range(x_left+1, x_right):
                if bitmaps[x,y_top] != bitmaps[x_left,y_top]:
                    all_white = False
                    break
            if all_white:
                y_top += 1
            else:
                break
        all_white = True

        while True:
            for x in range(x_left+1, x_right):
                if bitmaps[x,y_bottom-1] != bitmaps[x_left,y_bottom-1]:
                    all_white = False
                    break
            if all_white:
                y_bottom -= 1
            else:
                break
        box = (x_left, y_top, x_right, y_bottom)

        trimmed_image = src_image.crop(box)
        return trimmed_image

    def split_x(self, src_image, convert_to_black_white=False):
        """
        Splits an image vertically if all pixels in a column are same
        If convert_to_black_white is specified, then the image is first processed to have better result
        """
        (bitmaps,X,Y) = self.load_bitmap(src_image, convert_to_black_white)
        (x_left,y_top,x_right,y_bottom) = (0,0,X,Y)
        regions = [(x_left,x_right)]
        for x in range(x_left,x_right-1):
            all_equal = True
            for y in range(y_top+1,y_bottom):
                if bitmaps[x,y] != bitmaps[x,y_top]:
                    all_equal = False
                    break
            if all_equal:
                last_region = regions[-1]
                regions[-1] = (last_region[0],x-1)
                regions.append((x+1,last_region[1]))
        boxes = [(region[0],y_top,region[1],y_bottom) for region in regions if (region[1]-region[0])>1]
        return [src_image.crop(box) for box in boxes]

    def split_y(self, src_image, convert_to_black_white=False):
        """
        Splits an image horizontally if all pixels in a row are same
        If convert_to_black_white is specified, then the image is first processed to have better result
        """
        (bitmaps,X,Y) = self.load_bitmap(src_image, convert_to_black_white)
        (x_left,y_top,x_right,y_bottom) = (0,0,X,Y)
        regions = [(y_top, y_bottom)]
        for y in range(y_top,y_bottom-1):
            all_equal = True
            for x in range(x_left+1,x_right):
                if bitmaps[x,y] != bitmaps[x_left,y]:
                    all_equal = False
                    break
            if all_equal:
                last_region = regions[-1]
                regions[-1] = (last_region[0],y-1)
                regions.append((y+1,last_region[1]))
        boxes = [(x_left,region[0],x_right,region[1]) for region in regions if (region[1]-region[0])>1]
        return [src_image.crop(box) for box in boxes]

    def load_bitmap(self, src_image, convert_to_black_white):
        cannonical_image = src_image
        if convert_to_black_white:
            cannonical_image = self.convert_to_black_white(src_image)
        return (cannonical_image.load(),cannonical_image.size[0],cannonical_image.size[1])

    def convert_to_black_white(self,src_image):
        gray_image = src_image.convert('L')
        return gray_image.point(lambda x: 0 if x<128 else 255, '1')

    def process(self, image_src_path, image_dest_dir_path,convert_to_black_white):
        image = Image.open(image_src_path)
        extension = os.path.splitext(os.path.split(image_src_path)[-1])[1]
        image = self.trim(image,convert_to_black_white)
        images = self.split_x(image, True)
        final_images = []
        for image in images:
            final_images.extend(self.split_y(image, True))
        for i in range(len(final_images)):
            path = os.path.join(image_dest_dir_path,'trimmed_{}{}'.format(i,extension))
            final_images[i].save(path)