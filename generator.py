#!/usr/bin/env python

'''
Creates a printable sheet of crypto currency wallets
- Coin ticker
'''

import sys
import os.path
import qrcode
import string
import argparse
import json
from os import remove
from fpdf import FPDF
from math import floor
from PIL import Image
from mnemonic import mnemonic
from binascii import hexlify, unhexlify
from moneywagon import generate_keypair
from random import SystemRandom, randrange


class CryptoSheets:

    # A4 = 8.27" x 11.69"
    # 8.27" x 300dpi = 2480
    # 11.69" x 300dpi = 3508
    height          = 3508
    width           = 2480
    x_boxes         = 4
    y_boxes         = 11
    qr_resize_percent                   = 80
    qr_resize_double_percent            = 100 - ((100 - qr_resize_percent) * 2)
    row_number_size_large               = (200, 50)
    row_number_size_small               = (140, 35)
    row_number_guttering_percent_large  = 6
    row_number_guttering_percent_small  = 3
    icon_resize_percent                 = 30
    icon_guttering_percent              = 6
    box_height_percent                  = 25.4 / (297/100.0)
    box_width_percent                   = 48.5 / (210/100.0)

    def __init__(self, coin = 'btc', sheets = 1, height_offset = 0):
        self.box_height                    = self.box_height_percent * (self.height/100.0)
        self.box_width                     = self.box_width_percent * (self.width/100.0)
        self.guttering_height              = (self.height - (self.box_height * self.y_boxes)) / 2
        self.guttering_width               = (self.width - (self.box_width * self.x_boxes)) / 2
        self.qr_code_public_resized_size   = ((int)(self.box_width), (int)(self.box_width))
        self.qr_code_private_resized_size  = ((int)(self.box_width*(float(self.qr_resize_percent)/100)), (int)(self.box_width*(float(self.qr_resize_percent)/100)))
        self.number_images                 = []
        for x in range(0, 10):
            self.number_images.append(Image.open('images/'+str(x)+'.png')) 

        with open('coins/' + coin + '/info.json') as info_file:
            data = json.load(info_file)

        self.logo_imports()
        self.icon_imports()
        self.wallet_url_imports(data)

        self.mnemo = mnemonic.Mnemonic('english')

        pdf = FPDF()

        for x in range(sheets):
            pdf.add_page()
            self.sheet(coin, data, height_offset)
            pdf.image('sheet.png', x=0, y=0, w=210)
            # TODO: Need to overwrite the file here 25 times with random data and then make it white
            remove('sheet.png')

        pdf.output("crypto-sheets.pdf")

    def sheet(self, coin, data, height_offset):

        if os.path.isfile('test-page.png'):
            sheet = Image.open('test-page.png')
        else:
            sheet = Image.new(mode='L', size=(self.width, self.height), color=255)

        for row_number in range(floor(self.y_boxes / 2)):

            row_offset = (int)((self.box_height * 2) * row_number) + height_offset

            address = self.gen_keys(parent=data['parent'], entropy=self.gen_rand(), create_mnemonic=True)
            qr_code_public = self.qr_code_with_logo(coin, address['public'])
            qr_code_private = self.qr_code_with_logo(coin, address['private'])

            qr_code_public_resized = qr_code_public.resize(self.qr_code_public_resized_size)
            qr_code_private_resized = qr_code_private.resize(self.qr_code_private_resized_size)

            # Adress codes positions
            for x in range(0, self.x_boxes-1):
                if x == 0:
                    x_axis = (int)(self.guttering_width + (self.box_width - self.qr_code_public_resized_size[0]))
                    y_axis = (int)(self.guttering_height + (((self.box_height * 2) - self.qr_code_public_resized_size[1]) / 2)) + row_offset
                    sheet.paste(qr_code_public_resized, (x_axis, y_axis))
                else:
                    x_axis = (int)((self.guttering_width + (self.box_width - self.qr_code_private_resized_size[0])) + (self.box_width * x))
                    y_axis = (int)(self.guttering_height + (((self.box_height * 2) - self.qr_code_private_resized_size[1]) / 2)) + row_offset
                    sheet.paste(qr_code_private_resized, (x_axis, y_axis))

            sheet = self.add_wallet_icons(sheet, (0, row_offset))

            sheet = self.add_wallet_qr_codes(sheet, (0, row_offset))

            sheet = self.add_icons(sheet, (0, row_offset))

            sheet = self.add_row_numbers(sheet, (0, row_offset))

        sheet.save('sheet.png')


    def add_wallet_icons(self, sheet, offset):
        x_axis = (int)(offset[0] + self.guttering_width + (self.box_width * 3) + self.logo_guttering)
        y_axis = (int)(offset[1] + self.guttering_height + self.logo_guttering)
        sheet.paste(self.apple_logo, (x_axis, y_axis))

        x_axis = (int)(offset[0] + self.guttering_width + (self.box_width * 3) + self.logo_guttering)
        y_axis = (int)(offset[1] + self.guttering_height + self.box_height + self.logo_guttering)
        sheet.paste(self.android_logo, (x_axis, y_axis))

        return sheet


    def add_wallet_qr_codes(self, sheet, offset):
        x_axis = (int)(offset[0] + self.guttering_width + (self.box_width * 4) - self.qr_code_apple_wallet_resize_size[0])
        y_axis = (int)(offset[1] + self.guttering_height)
        sheet.paste(self.qr_code_apple_wallet, (x_axis, y_axis))

        x_axis = (int)(offset[0] + self.guttering_width + (self.box_width * 4) - self.qr_code_android_wallet_resize_size[0])
        y_axis = (int)(offset[1] + self.guttering_height + self.box_height)
        sheet.paste(self.qr_code_android_wallet, (x_axis, y_axis))

        return sheet


    def add_icons(self, sheet, offset):
        x_axis = (int)(offset[0] + self.guttering_width + self.box_width + self.icon_guttering)
        y_axis = (int)(offset[1] + self.guttering_height + self.box_height - self.icon_resize_size[1] - self.icon_guttering)
        sheet.paste(self.person_2_icon, (x_axis, y_axis))

        x_axis = (int)(offset[0] + self.guttering_width + self.box_width + self.icon_guttering)
        y_axis = (int)(offset[1] + self.guttering_height + self.box_height + self.icon_guttering)
        sheet.paste(self.person_3_icon, (x_axis, y_axis))

        x_axis = (int)(offset[0] + self.guttering_width + (self.box_width * 2) + self.icon_guttering)
        y_axis = (int)(offset[1] + self.guttering_height + self.box_height - self.icon_resize_size[1] - self.icon_guttering)
        sheet.paste(self.wallet_icon, (x_axis, y_axis))

        x_axis = (int)(offset[0] + self.guttering_width + (self.box_width * 2) + self.icon_guttering)
        y_axis = (int)(offset[1] + self.guttering_height + self.box_height + self.icon_guttering)
        sheet.paste(self.house_icon, (x_axis, y_axis))

        return sheet


    def add_row_numbers(self, sheet, offset):
        # Row numbers
        row_number = self.random_number_as_image()
        row_number_large = row_number.resize(self.row_number_size_large)
        row_number_small = row_number.resize(self.row_number_size_small)
        x_axis = (int)(offset[0] + self.guttering_width + (self.box_width / 2) - (self.row_number_size_small[0] / 2))
        y_axis = (int)(offset[1] + self.guttering_height + (self.row_number_guttering_percent_small * (self.box_width / 100)))
        sheet.paste(row_number_small, (x_axis, y_axis))

        x_axis = (int)(offset[0] + self.guttering_width + (self.box_width / 2) - (self.row_number_size_small[0] / 2))
        y_axis = (int)(offset[1] + self.guttering_height + (self.box_height * 2) - self.row_number_size_small[1] - (self.row_number_guttering_percent_small * (self.box_width /100)))
        sheet.paste(row_number_small, (x_axis, y_axis))

        x_axis = (int)(offset[0] + self.guttering_width + (self.box_width * 1.5) - (self.row_number_size_large[0] / 2))
        y_axis = (int)(offset[1] + self.guttering_height + (self.row_number_guttering_percent_large * (self.box_width / 100)))
        sheet.paste(row_number_large, (x_axis, y_axis))

        x_axis = (int)(offset[0] + self.guttering_width + (self.box_width * 1.5) - (self.row_number_size_large[0] / 2))
        y_axis = (int)(offset[1] + self.guttering_height + (self.box_height * 2) - self.row_number_size_large[1] - (self.row_number_guttering_percent_large * (self.box_width /100)))
        sheet.paste(row_number_large, (x_axis, y_axis))

        x_axis = (int)(offset[0] + self.guttering_width + (self.box_width * 2.5) - (self.row_number_size_large[0] / 2))
        y_axis = (int)(offset[1] + self.guttering_height + (self.row_number_guttering_percent_large * (self.box_width / 100)))
        sheet.paste(row_number_large, (x_axis, y_axis))

        x_axis = (int)(offset[0] + self.guttering_width + (self.box_width * 2.5) - (self.row_number_size_large[0] / 2))
        y_axis = (int)(offset[1] + self.guttering_height + (self.box_height * 2) - self.row_number_size_large[1] - (self.row_number_guttering_percent_large * (self.box_width /100)))
        sheet.paste(row_number_large, (x_axis, y_axis))

        return sheet


    def gen_rand(self):
        foo = SystemRandom()
        length = 32
        chars = string.hexdigits
        return ''.join(foo.choice(chars) for _ in range(length))


    def gen_keys(self, parent, entropy, create_mnemonic):
        addresses = {'public': '', 'private': ''}
        if create_mnemonic == True:
            words = self.mnemo.to_mnemonic(unhexlify(entropy))
            seed = hexlify(self.mnemo.to_seed(words))
        else:
            seed = entropy
        address = generate_keypair(parent, seed)
        addresses['public'] = address['public']['address']
        if create_mnemonic == True:
            addresses['private'] = words
        else:
            addresses['private'] = address['private']['hex']
        return addresses


    def qr_code_with_logo(self, coin, qr_code_string):
        qr_code = qrcode.make(qr_code_string, error_correction=qrcode.constants.ERROR_CORRECT_H).convert('LA')
        if os.path.isfile('coins/' + coin + '/logo.png'):
            logo = Image.open('coins/' + coin + '/logo.png')
            logo_size = ((int)(qr_code.width / 3.41667), (int)(qr_code.height / 3.41667))
            logo_resized = logo.resize(logo_size, Image.ANTIALIAS)
        else:
            sys.exit(coin.upper() + ' logo not present')
        qr_code_width, qr_code_height = qr_code.size
        logo_width, logo_height = logo_resized.size
        qr_code.paste(logo_resized, ((int)((qr_code_width-logo_width)/2), (int)((qr_code_height-logo_height)/2)))

        return qr_code


    def qr_code(self, qr_code_string):

        return qrcode.make(qr_code_string).convert('LA')


    def logo_imports(self):
        apple_logo_original = Image.open('images/apple_logo.png').transpose(Image.ROTATE_90)
        android_logo_original = Image.open('images/android_logo.png').transpose(Image.ROTATE_90)
        apple_logo_resize_size = andriod_logo_resize_size = \
            ((int)(self.box_height * (float(self.qr_resize_double_percent) / 100)), (int)(self.box_height * (float(self.qr_resize_double_percent) / 100)))
        self.apple_logo = apple_logo_original.resize(apple_logo_resize_size)
        self.android_logo = android_logo_original.resize(andriod_logo_resize_size)
        self.logo_guttering =  (self.box_height - apple_logo_resize_size[1]) / 2        


    def icon_imports(self):
        person_1_icon_original = Image.open('images/person_1_icon.jpeg')
        person_2_icon_original = Image.open('images/person_2_icon.jpeg')
        person_3_icon_original = Image.open('images/person_3_icon.jpeg')
        self.icon_resize_size = ((int)(self.box_height * (float(self.icon_resize_percent) / 100)), (int)(self.box_height * (float(self.icon_resize_percent) / 100)))
        self.person_1_icon = person_1_icon_original.resize(self.icon_resize_size)
        self.person_2_icon = person_2_icon_original.resize(self.icon_resize_size)
        self.person_3_icon = person_3_icon_original.resize(self.icon_resize_size)
        wallet_icon_original = Image.open('images/wallet_icon.png')
        house_icon_original = Image.open('images/house_icon.png')
        lock_icon_original = Image.open('images/lock_icon.png')
        self.wallet_icon = wallet_icon_original.resize(self.icon_resize_size)
        self.house_icon = house_icon_original.resize(self.icon_resize_size)
        self.lock_icon = lock_icon_original.resize(self.icon_resize_size)
        self.icon_guttering = self.icon_guttering_percent * (self.box_width / 100)


    def wallet_url_imports(self, data):
        self.qr_code_apple_wallet_resize_size = self.qr_code_android_wallet_resize_size = \
            ((int)(self.box_height), (int)(self.box_height))
        qr_code_apple_wallet_original = self.qr_code(data['wallets']['apple']).transpose(Image.ROTATE_90)
        qr_code_android_wallet_original = self.qr_code(data['wallets']['android']).transpose(Image.ROTATE_90)
        self.qr_code_apple_wallet = qr_code_apple_wallet_original.resize(self.qr_code_apple_wallet_resize_size)
        self.qr_code_android_wallet = qr_code_android_wallet_original.resize(self.qr_code_android_wallet_resize_size)


    def random_number_as_image(self):
        number = str(randrange(0, 10000)).zfill(4)
        number_size = (self.number_images[0].width * 4), self.number_images[0].height
        number_image = Image.new(mode='L', size=number_size, color=255)
        number_image.paste(self.number_images[(int)(number[0])], ((self.number_images[0].width * 0),0))
        number_image.paste(self.number_images[(int)(number[1])], ((self.number_images[0].width * 1),0))
        number_image.paste(self.number_images[(int)(number[2])], ((self.number_images[0].width * 2),0))
        number_image.paste(self.number_images[(int)(number[3])], ((self.number_images[0].width * 3),0))
        return number_image


if __name__ == '__main__':
    default_coin   = 'btc'
    sheets         = 1
    coin           = default_coin
    height_offset  = 0
    parser = argparse.ArgumentParser(description='A script to create A4 sheets of crypto wallets')
    parser.add_argument('-c', '--coin', metavar='btc', help='Coin to create the wallet for', required=False)
    parser.add_argument('-s', '--sheets', metavar='5', type=int, help='The amount of pages you want to print wallets on', required=False)
    parser.add_argument('-os', '--offset', metavar='15', type=int, help='An height offset in pixles to get the qr codes lined up with the lables correctly', required=False)
    args = parser.parse_args()

    if args is not None and args.coin is not None and len(args.coin) > 0:
        if os.path.isdir('coins/'+args.coin) == False:
            print(args.coin.upper() + ' is not a recognised coin')
            sys.exit()
        if os.path.isfile('coins/' + coin + '/info.json') == False:
            print('info.json file does not exist in the coins/' + args.coin + ' directory')
            sys.exit()
        coin = args.coin

    if args is not None and args.sheets is not None:
        sheets = (int)(args.sheets)

    if args is not None and args.offset is not None:
        height_offset = (int)(args.offset)

    CryptoSheets(coin, sheets, height_offset)
