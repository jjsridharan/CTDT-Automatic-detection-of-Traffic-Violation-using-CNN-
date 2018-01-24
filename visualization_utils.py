import collections
import functools
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as Image
import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import six
import tensorflow as tf
from operator import itemgetter
from threading import Thread
from lplate import Main
from Update import update
from helmet_detection import findhelmet
import sys
sys.path.append("..")


_TITLE_LEFT_MARGIN = 10
_TITLE_TOP_MARGIN = 10
STANDARD_COLORS = [
    'AliceBlue', 'Chartreuse', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque',
    'BlanchedAlmond', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
    'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
    'DarkCyan', 'DarkGoldenRod', 'DarkGrey', 'DarkKhaki', 'DarkOrange',
    'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
    'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
    'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
    'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
    'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
    'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
    'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
    'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
    'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
    'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
    'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
    'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
    'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
    'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
    'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
    'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
    'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
    'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
    'WhiteSmoke', 'Yellow', 'YellowGreen'
]
def draw_bounding_box_on_image_array(image,

                                     ymin,

                                     xmin,

                                     ymax,

                                     xmax,display_str_list=(),

                                     color='red',

                                     thickness=4,                                     

                                     use_normalized_coordinates=True):

  """Adds a bounding box to an image (numpy array).



  Args:

    image: a numpy array with shape [height, width, 3].

    ymin: ymin of bounding box in normalized coordinates (same below).

    xmin: xmin of bounding box.

    ymax: ymax of bounding box.

    xmax: xmax of bounding box.

    color: color to draw bounding box. Default is red.

    thickness: line thickness. Default value is 4.

    display_str_list: list of strings to display in box

                      (each to be shown on its own line).

    use_normalized_coordinates: If True (default), treat coordinates

      ymin, xmin, ymax, xmax as relative to the image.  Otherwise treat

      coordinates as absolute.

  """

  image_pil = Image.fromarray(np.uint8(image)).convert('RGB')

  draw_bounding_box_on_image(image_pil, ymin, xmin, ymax, xmax,display_str_list, color,

                             thickness,

                             use_normalized_coordinates)

  np.copyto(image, np.array(image_pil))
  image_pil.save("G:\\person.jpg")



def draw_bounding_box_on_image(image,

                               ymin,

                               xmin,

                               ymax,

                               xmax, display_str_list=(),

                               color='red',

                               thickness=4,

                               use_normalized_coordinates=True):

  """Adds a bounding box to an image.



  Each string in display_str_list is displayed on a separate line above the

  bounding box in black text on a rectangle filled with the input 'color'.

  If the top of the bounding box extends to the edge of the image, the strings

  are displayed below the bounding box.



  Args:

    image: a PIL.Image object.

    ymin: ymin of bounding box.

    xmin: xmin of bounding box.

    ymax: ymax of bounding box.

    xmax: xmax of bounding box.

    color: color to draw bounding box. Default is red.

    thickness: line thickness. Default value is 4.

    display_str_list: list of strings to display in box

                      (each to be shown on its own line).

    use_normalized_coordinates: If True (default), treat coordinates

      ymin, xmin, ymax, xmax as relative to the image.  Otherwise treat

      coordinates as absolute.

  """

  draw = ImageDraw.Draw(image)

  im_width, im_height = image.size

  if use_normalized_coordinates:

    (left, right, top, bottom) = (xmin * im_width, xmax * im_width,

                                  ymin * im_height, ymax * im_height)

  else:

    (left, right, top, bottom) = (xmin, xmax, ymin, ymax)

  draw.line([(left, top), (left, bottom), (right, bottom),

             (right, top), (left, top)], width=thickness, fill=color)

  try:

    font = ImageFont.truetype('arial.ttf', 24)

  except IOError:

    font = ImageFont.load_default()



  # If the total height of the display strings added to the top of the bounding

  # box exceeds the top of the image, stack the strings below the bounding box

  # instead of above.

  display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]

  # Each display_str has a top and bottom margin of 0.05x.

  total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)



  if top > total_display_str_height:

    text_bottom = top

  else:

    text_bottom = bottom + total_display_str_height

  # Reverse list and print from bottom to top.

  for display_str in display_str_list[::-1]:

    text_width, text_height = font.getsize(display_str)

    margin = np.ceil(0.05 * text_height)

    draw.rectangle(

        [(left, text_bottom - text_height - 2 * margin), (left + text_width,

                                                          text_bottom)],

        fill=color)

    draw.text(

        (left + margin, text_bottom - text_height - margin),

        display_str,

        fill='black',

        font=font)

    text_bottom -= text_height - 2 * margin
    
def isintersecting(box1, box2,im_height,im_width,lparam,tparam):
  ymin1, xmin1, ymax1, xmax1 = box1
  ymin2, xmin2, ymax2, xmax2 = box2
  (left1, right1, top1, bottom1) = (xmin1 * im_width, xmax1 * im_width,ymin1 * im_height, ymax1 * im_height)
  print(left1,right1,top1,bottom1)
  left1=left1-lparam
  top1=top1-tparam
  (left2, right2, top2, bottom2) = (xmin2 * im_width, xmax2 * im_width,ymin2 * im_height, ymax2 * im_height)
  print(left1,right1,top1,bottom1)
  print(left2,right2,top2,bottom2)
  if left2 >=left1 and left2<=right1 and left2>=top1 and left2<=bottom1 :
    return True
  if right2 >=left1 and right2<=right1 and right2>=top1 and right2<=bottom1 :
    return True
  return False
def visualize_boxes_and_labels_on_image_array(image,
                                              boxes,
                                              classes,
                                              scores,
                                              category_index,
                                              instance_masks=None,
                                              keypoints=None,
                                              use_normalized_coordinates=False,
                                              max_boxes_to_draw=20,
                                              min_score_thresh=.7,
                                              agnostic_mode=False,
                                              line_thickness=4):
  box_to_display_str_map = collections.defaultdict(list)
  box_to_color_map = collections.defaultdict(str)
  box_to_instance_masks_map = {}
  class_list = []
  box_to_keypoints_map = collections.defaultdict(list)
  for j in range(20) :
    if scores[j] < min_score_thresh :
      break
    else :
      if classes[j] in category_index.keys() :
        class_list.append([category_index[classes[j]]['name'],j])
  image_pil = Image.fromarray(np.uint8(image)).convert('RGB')
  im_width, im_height = image_pil.size
  lplate="notfound"
  for i in range(j):
    if scores[i] > min_score_thresh:
      if not agnostic_mode:
        if classes[i] in category_index.keys():
          class_name = category_index[classes[i]]['name']
          if 'motorcycle' in class_name :
            print(boxes[i].tolist())
            personcount=0
            for item in class_list :
              if 'person' in item[0] :
                find_intersect = isintersecting(tuple(boxes[i].tolist()),tuple(boxes[item[1]].tolist()),im_height,im_width,50,30)
                print("person\n\n")
                ymin, xmin, ymax, xmax = tuple(boxes[item[1]].tolist())
                draw_bounding_box_on_image_array(image,ymin,xmin,ymax,xmax,['Person'])                                    
                if find_intersect is True:
                 personcount+=1
                 flag=True
                 image_pil.save("G:\\1.jpg")
                 classes_list,boxess=findhelmet("G:\\1.jpg")
                 for items in classes_list :
                   if 'helmet' in items[0] :
                     find_intersect = isintersecting(tuple(boxes[item[1]].tolist()),tuple(boxess[items[1]].tolist()),im_height,im_width,0,30)
                     if find_intersect is True :
                       flag=False
                 if flag is True :
                   if "notfound" in lplate :
                     #boxofvehicle=(ymin1, xmin1, ymax1, xmax1)
                     #image_pil = image_pil.crop(boxofvehicle)
                     #image_pil.save("G:\\1.jpg")
                     lplate=Main.main("G:\\1.jpg")
                     if ((lplate is None) or (len(lplate)==0))==False :
                       lplate,cor=lplate
                       lplate=lplate.strChars
                       update(lplate)
                   else :
                     update(lplate)
                   ymin, xmin, ymax, xmax = tuple(boxes[i].tolist())
                   draw_bounding_box_on_image_array(image,ymin,xmin,ymax,xmax,['motorcycle'])
            if personcount >= 3 :
              print("Number of persons greater than 3 in motorcycle")
              if "notfound" in lplate :
                lplate=Main.main("G:\\1.jpg")
                lplate,cor=lplate
                lplate=lplate.strChars
                update(lplate)
              else :
                update(lplate)
              
