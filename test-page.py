from os import remove
from fpdf import FPDF
from PIL import Image, ImageDraw
import argparse

if __name__ == '__main__':
    """
    Use this file to print a test page with the correct offset for your printer so
    you do not waste labeled sheets of paper which can cost a lot of money
    """
    # A4 = 8.27" x 11.69"
    # 8.27" x 300dpi = 2480
    # 11.69" x 300dpi = 3508
    height             = 3508
    width              = 2480
    height_offset      = 0
    x_boxes            = 4
    y_boxes            = 11
    box_height_percent = 25.4 / (297/100.0)
    box_width_percent  = 48.5 / (210/100.0)
    box_height         = box_height_percent * (height/100.0)
    box_width          = box_width_percent * (width/100.0)
    guttering_height   = (height - (box_height * y_boxes)) / 2
    guttering_width    = (width - (box_width * x_boxes)) / 2
    image = Image.new(mode='L', size=(width, height), color=255)

    parser = argparse.ArgumentParser(description='A script to create test pages so you don\'t waste labled sheets')
    parser.add_argument('-os', '--offset', metavar='15', type=int, help='An height offset in pixles to get the boxes lining up with the lables correctly', required=False)

    if args is not None and args.offset is not None and len(args.offset) > 0:
        height_offset = (int)(args.offset)

    draw = ImageDraw.Draw(image)

    for y in range(0, y_boxes + 1):
        y_height = (y * box_height) + guttering_height + height_offset
        column = ((guttering_width, y_height), ((width - guttering_width), y_height))
        draw.line(column, fill=128, width=4)

    for x in range(0, x_boxes + 1):
        x_width = (x * box_width) + guttering_width
        row = ((x_width, guttering_height + height_offset), (x_width, (height - guttering_height + height_offset)))
        draw.line(row, fill=128, width=4)

    del draw

    image.save('test-page.png', 'PNG')

    pdf = FPDF()
    pdf.add_page()
    pdf.image('test-page.png', x=0, y=0, w=210)
    pdf.output("test-page.pdf")

    remove('test-page.png')