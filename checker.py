import os
import re

# text detection
# import pytesseract

# image generation
import fitz
import numpy as np
import cv2
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt

def getFontStyle(font_family):
    if font_family == 'Times New Roman':
        acceptable_fonts = {
            'Times New Roman',
            'Times New Roman,Bold',
            'Times New Roman,Italic',
            'TimesNewRoman',
            'TimesNewRoman,Italic',
            'TimesNewRoman,Bold',
            'TimesNewRoman,BoldItalic',
            'TimesNewRomanPS-BoldMT',
            'TimesNewRomanPS-BoldItalicMT',
            'TimesNewRomanPS-ItalicMT',
            'TimesNewRomanPSMT',
            'TimesNewRomanPSMT-Bold',
            'Times-Bold',
            'Times-Roman',
            'Times-Italic'
        }

        return acceptable_fonts
        
    elif font_family == 'Arial':
        arial = 'add here'

    elif font_family == 'Calibri':
        calibri = 'add calibri'

# CALCULATE MARGINS AND SPACINGS
# def calculate(img, boxes):
#     # Load the image from the provided path

#     height, width = img.shape[:2]

#     if not boxes:  # Check if boxes list is empty
#         # Set default values for margins
#         top_margin = 0
#         bottom_margin = 0
#         left_margin = 0
#         right_margin = 0
#         min_x = 0
#         max_x = 0
#         min_y = 0
#         max_y = 0
#         spacings = []
#         spacing_idx = []
#     else:
#         min_x = min(box[0] for box in boxes)
#         max_x = max(box[0] + box[2] for box in boxes)
#         min_y = min(box[1] for box in boxes)
#         max_y = max(box[1] + box[3] for box in boxes)

#         top_margin = min_y / height
#         bottom_margin = (height - max_y) / height
#         left_margin = min_x / width
#         right_margin = (width - max_x) / width
#         spacing_idx = []
#         spacings = []
#         sorted_boxes = sorted(boxes, key=lambda box: box[1])
#         for i in range(len(sorted_boxes) - 1):
#             y_bottom = sorted_boxes[i][1] + sorted_boxes[i][3]
#             y_top = sorted_boxes[i+1][1]
#             spacing = ((y_top - y_bottom) / height) * 100
#             # if spacing >= 2 and spacing <= 2.85:  # modify this if necessary
#             #     spacing = 2
#             # if spacing >= 0.3 and spacing <= 1.45:
#             #     spacing = 1
#             if spacing > 0:
#                 spacings.append(spacing)
#                 spacing_idx.append(i)

#     return top_margin, bottom_margin, left_margin, right_margin, min_x, max_x, spacings, spacing_idx # min_y, max_y, height, width : removed

# def margin(img, top_margin, bottom_margin, left_margin, right_margin, margins): 
#     margin_ret = []

#     # OPENCV LINE EXTRACTION
#     # margin_height_top = int(top_margin * img.shape[0])
#     margin_height_bottom = int((1 - bottom_margin) * img.shape[0])
#     # margin_width_left = int(left_margin * img.shape[1]) 
#     # margin_width_right = int((1 - right_margin) * img.shape[1])

#     # decode json_margins paramter from the DATABASE
#     top = float(margins['margin_top'])
#     bottom = float(margins['margin_bottom'])
#     left = float(margins['margin_left'])
#     right = float(margins['margin_right'])

#     margin_color = (255, 0, 0)  # RGB
#     margin_thickness = 2

#     # UPDATE AND ADD IF STATEMENTS HERE, MUTATE VALUES
#     top_round = round(top_margin, 2)
#     bottom_round = round(bottom_margin, 2)
#     left_round = round(left_margin, 2)
#     right_round = round(right_margin, 2)

#     # TOP
#     if top == 1:
#         correct_top = 300
#         margin_top = [
#             0.05, # remove if there's no number in top
#             0.09,
#             0.1
#         ]
    
#     # LEFT
#     if left == 1:
#         correct_left = 284
#         margin_left = [
#             0.12,
#             1.0
#         ]

#     if left == 1.5:
#         correct_left = 432
#         margin_left = [
#             0.16,
#             0.17,
#             0.18,
#             0.19 
#         ]

#     # RIGHT
#     if right == 1:
#         margin_right = 2152
#         right_margin_one = [
#             0.12,
#             0.13
#         ]

#     # BOTTOM
#     if bottom == 1:
#         correct_bottom = 2701
#         margin_bottom = [
#             0.8,
#             0.09,
#             0.1,
#             0.11,
#             0.12,
#             0.13,
#             0.14,
#             0.15,
#             0.16
#         ]

#     # Top margin
#     if top_round not in margin_top:
#         cv2.line(img, (0, correct_top), (img.shape[1], correct_top), (62,199,214), margin_thickness)
#         margin_ret.append({'top_margin': top_round})
#     else:
#         margin_ret.append({'top_margin': 'N/A'})

#     # Bottom margin
#     if bottom_round not in margin_bottom:
#         cv2.line(img, (0, correct_bottom), (img.shape[1], correct_bottom), (241,75,38), margin_thickness)
#         margin_ret.append({'bottom_margin': bottom_round})
#     else:
#         margin_ret.append({'bottom_margin': 'N/A'})

#     # Left margin
#     if left_round not in margin_left:
#         cv2.line(img, (correct_left, 0), (correct_left, img.shape[0]), (0, 0, 0), margin_thickness)
#         margin_ret.append({'left_margin': left_round})
#     else:
#         margin_ret.append({'left_margin': 'N/A'})

#     # Right margin
#     if right_round not in right_margin_one:
#         cv2.line(img, (margin_right, 0), (margin_right, img.shape[0]), (0,126,167), margin_thickness)
#         margin_ret.append({'right_margin': right_round})
#     else:
#         margin_ret.append({'right_margin': 'N/A'})

#     return margin_ret

# def spacing(img, spacings, spacing_indices, text_boxes, min_x, max_x, accepted_spacings):
#     import math
#     spacing_color = (55, 183, 9) 
#     spacing_thickness = 2
#     spacings_ret = []

#     sorted_boxes = sorted(text_boxes, key=lambda box: box[1])
#     for i, index in enumerate(spacing_indices):
#         if index < len(sorted_boxes) - 1:
#             y_bottom = sorted_boxes[index][1] + sorted_boxes[index][3]
#             y_top = sorted_boxes[index+1][1]
#             spacing_height = int((y_bottom + y_top) / 2)

#             # CONVERT TO STRING to accept the condition from accepted_spacings
#             spaces = "{:.1f}".format(spacings[i])
#             spaces_formatted = str(math.floor(float(spaces)))

#             if spaces <= '1':
#                 cv2.line(img, (min_x, y_top), (max_x, y_top), spacing_color, spacing_thickness)
#                 cv2.line(img, (min_x, y_bottom), (max_x, y_bottom), spacing_color, spacing_thickness)
#                 cv2.putText(img, '1', (int((min_x + max_x) / 2), spacing_height + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
#                 spacings_ret.append('1')

#             if spaces_formatted != accepted_spacings and spaces_formatted > '1':
#                 cv2.line(img, (min_x, y_top), (max_x, y_top), spacing_color, spacing_thickness)
#                 # cv2.line(img, (min_x, spacing_height), (max_x, spacing_height), spacing_color, spacing_thickness) # middle
#                 cv2.line(img, (min_x, y_bottom), (max_x, y_bottom), spacing_color, spacing_thickness)
#                 cv2.putText(img, spaces, (int((min_x + max_x) / 2), spacing_height + 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
#                 spacings_ret.append(spaces)
                
#     return spacings_ret

def remove_rn(data):
    # regular expression pattern to match both uppercase and lowercase Roman numerals
    roman_numeral_pattern = r'\b[MmDdCcLlXxVvIi]+\b'

    # remove Roman numerals
    for i in range(len(data['text'])):
        data['text'][i] = re.sub(roman_numeral_pattern, '', data['text'][i]).strip()

    return data

def getSpecificPage(pdf_path, selection):
    pdf_document = fitz.open(pdf_path)

    n_pages = pdf_document.page_count

    section_headings = {
    'Preliminaries': [
        'ABSTRACT',
        'ACKNOWLEDGEMENTS',
        'TABLE OF CONTENTS',
        'LIST OF FIGURES',
        'LIST OF TABLES',
        'LIST OF ABBREVIATIONS'
    ],
    'Chapter 1': ['CHAPTER I'],
    'Chapter 2': ['CHAPTER II'],
    'Chapter 3': ['CHAPTER III'],
    'Chapter 4': ['CHAPTER IV'],
    'Chapter 5': ['CHAPTER V'],
    'Bibliography' : ['BIBLIOGRAPHY']
}

    sections = {}

    if selection not in section_headings:
        return '' # selection not recognized

    headings = section_headings[selection]
    n_pages = len(pdf_document)
    found_heading = None
    next_heading = None

    for page_num in range(n_pages):
        page = pdf_document[page_num]
        page_text = page.get_text()

        for heading in headings:
            pattern = rf'(?i)\b{heading}\b'
            match = re.search(pattern, page_text)
            if match:
                found_heading = heading
                sections[heading] = {
                    'starting_page': page_num + 1,
                }
            # else:
            #     return ''
                         
        if selection != 'Preliminaries':
            if found_heading:
                # if a heading has been found, check for the next heading
                next_headings = section_headings.get(f'Chapter {int(selection.split(" ")[-1]) + 1}', [])
                if next_headings:
                    for next_heading in next_headings:
                        next_pattern = rf'(?i)\b{next_heading}\b'
                        next_match = re.search(next_pattern, page_text)
                        if next_match:
                            sections[found_heading]['ending_page'] = page_num
                            return sections
                else:
                # if there is no next chapter, check for the 'Bibliography' section
                    bibliography_headings = section_headings.get('Bibliography', [])
                    for bibliography_heading in bibliography_headings:
                        bibliography_pattern = rf'(?i)\b{bibliography_heading}\b'
                        bibliography_match = re.search(bibliography_pattern, page_text)
                        if bibliography_match:
                            sections[found_heading]['ending_page'] = page_num
                            return sections

def analyzePDF(pdf_path, acceptable_fonts, accepted_spacings, margins_json, selection):
    pdf_document = fitz.open(pdf_path)

    from datetime import datetime
    datetime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    directory = f'{os.getcwd()}\\temp_images\\{selection}\\{datetime}'
    os.makedirs(directory)

    sections_page = getSpecificPage(pdf_document, selection)

    # GAWIN KO MAMAYA!!
    # if isinstance(sections_page, str):
    #     return f'{selection} not recognized. Please upload a full document paper.', ''

    extracted_pages = list(sections_page.values())[0]

    # assign starting and ending page
    starting_page = extracted_pages['starting_page']
    ending_page = extracted_pages['ending_page']
    
    px = 4

    image_paths = []
    image_with_rect = None

    paper_error = []
    font_style_error = []
    font_size_error  = []
    font_color_error = []
    margin_error     = []
    spacing_error    = []

    errors = {
        'paper_size' : paper_error,
        'font_family' : font_style_error,
        'font_size' : font_size_error,
        'font_color' : font_color_error,
        'margins' : margin_error,
        'spacings' : spacing_error
    }

    increment_page = 0

    if starting_page == 0:
            # add more functions to this
            paper_error.append('No pages detected.')

    for page_num in range(starting_page - 1, ending_page):
        page = pdf_document[page_num]
        pix = page.get_pixmap(matrix=fitz.Matrix(px, px))
        image_np = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
        image_with_rect = image_np.copy()

        # Get BBox from image to text and GET text
        # tesseract_data = pytesseract.image_to_data(image_np, output_type=pytesseract.Output.DICT)
        # new_data = remove_rn(tesseract_data)
        # n_boxes = len(new_data['text'])
        
        # Font Analysis
        blocks = page.get_text("dict")['blocks']
        width = page.get_text("dict")['width']
        height = page.get_text("dict")['height']

        # Check paper size
        # A Letter Size = 612 × 792
        height = height / 72
        width = width / 72

        # Paper Sizes List
        Letter = width == 8.5 and height == 11
        # Legal = width == 8.5 and height == 14
        # Tabloid = width == 11 and height == 17
        # A4 = width == float("%2.f" % 2.91) and height == float("%2.f" % 4.12)

        if not Letter: # EDIT MAMAHYA
            paper_error.append(page)

        # === Font ===
        for block in blocks:    
            if 'image' not in block: # analyze texts only
                lines = block['lines']
                for line in lines:
                    spans = line['spans']
                    for span in spans:
                        if span['text'] != ' ': # dont include empty chars
                            size = span['size']
                            color = span['color']
                            fonts = span['font']
                            overlay = image_with_rect.copy()

                            # This part will cluster the data and append the errors
                            if fonts not in acceptable_fonts:
                                cv2.rectangle(overlay, (int(span['bbox'][0]) * px, int(span['bbox'][1]) * px),
                                            (int(span['bbox'][2]) * px, int(span['bbox'][3]) * px), (62,199,214), -1)
                                cv2.addWeighted(overlay, 0.3, image_with_rect, 1 - 0.3, 0, image_with_rect)
                                # append to list
                                font_style_error.append({"page": increment_page, "fonts": fonts})

                            if size not in {12.0}: # size 12
                                cv2.rectangle(overlay, (int(span['bbox'][0]) * px, int(span['bbox'][1]) * px),
                                            (int(span['bbox'][2]) * px, int(span['bbox'][3]) * px), (241,232,38), -1)
                                cv2.addWeighted(overlay, 0.3, image_with_rect, 1 - 0.3, 0, image_with_rect)
                                # append to list
                                font_size_error.append({"page": increment_page, "size": size})

                            if color not in {0}: # not black
                                cv2.rectangle(overlay, (int(span['bbox'][0]) * px, int(span['bbox'][1]) * px),
                                                (int(span['bbox'][2]) * px, int(span['bbox'][3]) * px), (241,75,38), -1)
                                cv2.addWeighted(overlay, 0.3, image_with_rect, 1 - 0.3, 0, image_with_rect)
                                # append to list
                                font_color_error.append({"page": increment_page, "color": color})

        # collect text boxes
        # text_boxes = []
        # for i in range(n_boxes):    
        #     if i != 0:
        #         x, y, w, h = new_data['left'][i], new_data['top'][i], new_data['width'][i], new_data['height'][i]
        #         text_boxes.append((x, y, w, h))

        # # calculate margins and spacings with parameters: IMAGE and TEXT BOXES 
        # top_margin, bottom_margin, left_margin, right_margin, min_x, max_x, spacings, spacing_idx = calculate(image_with_rect, text_boxes)
        # # cv2.cvtColor(image_with_rect, cv2.COLOR_RGB2BGR)

        # # draw margins and spacing on the image
        # margin_ret = margin(image_with_rect, top_margin, bottom_margin, left_margin, right_margin, margins_json)
        # margin_error.append({"page": increment_page, "margins_arr": margin_ret})
        margin_error.append({"page": increment_page, 'margins_arr': [{'top_margin': 'N/A'}, {'bottom_margin': 'N/A'}, {'left_margin': 'N/A'}, {'right_margin': 'N/A'}]})
        
        # spacings_ret = spacing(image_with_rect, spacings, spacing_idx, text_boxes, min_x, max_x, accepted_spacings)
        # spacing_error.append({"page": increment_page, "spacings_arr": spacings_ret})
        spacing_error.append({"page": increment_page, "spacings_arr": []})

        image_path = f'{directory}\\page_{increment_page}.png'

        fig, ax = plt.subplots(figsize=(20, 25))

        # remove image axis
        ax.imshow(image_with_rect)
        ax.axis('off')

        fig.savefig(image_path, bbox_inches='tight', pad_inches=0)
        plt.close(fig)

        image_paths.append(image_path)

        # BREAK THE LOOP WHEN THE PAGE EQUAL TO 40
        # MAX PAGE: 20
        if increment_page + 1 == 20:
            break

        increment_page += 1
    
    return image_paths, errors

from collections import defaultdict, OrderedDict

def cluster_errors(errors):
    grouped_data = defaultdict(lambda: {
        'font_size': [],
        'font_family': set(),
        'font_color': [],
        'spacings_arr': [],
        'margins_arr': []
    })

    for key in ['font_size', 'font_family', 'font_color', 'spacings', 'margins']:
        error_items = errors.get(key, [])
        for item in error_items:
            page = item.get('page')

            if key == 'font_size':
                size = int(item.get('size'))
                grouped_data[page]['font_size'].append(size)

            elif key == 'font_family':
                family = item.get('fonts')
                grouped_data[page]['font_family'].add(family)

            elif key == 'font_color':
                color = item.get('color')
                grouped_data[page]['font_color'].append(color)

            elif key == 'spacings':
                spacings = item.get('spacings_arr')
                grouped_data[page]['spacings_arr'].extend(spacings)

            elif key == 'margins':
                margins = item.get('margins_arr')
                grouped_data[page]['margins_arr'] = margins

    sorted_grouped_data = OrderedDict(sorted(grouped_data.items()))
    result = {page: {key: list(value) if isinstance(value, set) else value for key, value in data.items()} for page, data in sorted_grouped_data.items()}

    return result
