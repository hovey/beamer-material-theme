#!/usr/bin/env python3
import json
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
from colour import Color

__location__ = os.path.realpath(os.getcwd())

config_filepath = os.path.join(__location__, 'config.json')
latex_source_filepath = os.path.join(__location__, 'dist')
latex_source_files = [join(latex_source_filepath, f) for f in listdir(latex_source_filepath) if isfile(join(latex_source_filepath, f))]


with open(config_filepath, 'r') as configFile:
    configJson = configFile.read()

config = json.loads(configJson)

config_map = {
    'primaryColor': {
        'color': None,
        'replace_string': '%PRIMARY_COLOR%'
    },
    'primaryColorLight': {
        'color': None,
        'replace_string': '%PRIMARY_COLOR_LIGHT%'
    },
    'primaryColorDark': {
        'color': None,
        'replace_string': '%PRIMARY_COLOR_DARK%'
    },
    'primaryTextColor': {
        'color': None,
        'replace_string': '%PRIMARY_TEXT_COLOR%'
    },
    'secondaryColor': {
        'color': None,
        'replace_string': '%SECONDARY_COLOR%'
    },
    'secondaryColorLight': {
        'color': None,
        'replace_string': '%SECONDARY_COLOR_LIGHT%'
    },
    'secondaryColorDark': {
        'color': None,
        'replace_string': '%SECONDARY_COLOR_DARK%'
    },
    'secondaryTextColor': {
        'color': None,
        'replace_string': '%SECONDARY_TEXT_COLOR%'
    },
    'accentColor': {
        'color': None,
        'replace_string': '%ACCENT_COLOR%'
    },
    'backgroundColorShadow': {
        'color': None,
        'replace_string': '%BACKGROUND_COLOR_SHADOW%'
    },
    'backgroundColor1': {
        'color': None,
        'replace_string': '%BACKGROUND_COLOR_1%'
    },
    'backgroundColor2': {
        'color': None,
        'replace_string': '%BACKGROUND_COLOR_2%'
    },
    'backgroundColor3': {
        'color': None,
        'replace_string': '%BACKGROUND_COLOR_3%'
    },
    'backgroundColor4': {
        'color': None,
        'replace_string': '%BACKGROUND_COLOR_4%'
    }
}

def read_color_from_json(color_name):
    hex_value = config[color_name]
    if hex_value is None:
        return None
    return Color(str(hex_value))

def get_config_map_color(color_name):
    return config_map[color_name]['color']

def get_config_map_color_replace_string(color_name):
    return config_map[color_name]['replace_string']

def set_config_map_color(color_name, color_value):
    config_map[color_name]['color'] = color_value


def hex_to_rgb(value):
    value = value.lstrip('#')
    return list(int(value[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)


''' Complement the colours in a RGB image
    Written by PM 2Ring 2016.10.08
'''
# Sum of the min & max of (a, b, c)
def hilo(a, b, c):
    if c < b: b, c = c, b
    if b < a: a, b = b, a
    if c < b: b, c = c, b
    return a + c

def complement(r, g, b):
    k = hilo(r, g, b)
    return tuple(k - u for u in (r, g, b))

def color_brighten(color, percentage):
    r = int(255 * color.red)
    g = int(255 * color.green)
    b = int(255 * color.blue)
    p = int(255 * percentage)
    return Color(rgb=(
        min(r + p, 255) / 255,
        min(g + p, 255) / 255,
        min(b + p, 255) / 255)
        )

def color_darken(color, percentage):
    r = int(255 * color.red)
    g = int(255 * color.green)
    b = int(255 * color.blue)
    p = int(255 * percentage)
    return Color(rgb=(
        max(r - p, 0) / 255,
        max(g - p, 0) / 255,
        max(b - p, 0) / 255)
        )

def get_contrast_color(color, bright_color, dark_color):
    return bright_color if color.get_luminance() < 0.6 else dark_color

def replace_in_files(replace_text, replace_value):
    for source_file in latex_source_files:
        file_content = open(source_file, 'r').read()
        # print('reading file: ' + source_file)
        if replace_text in file_content:
            #print('replacing ' + replace_text + ' w/ ' + replace_value)
            open(source_file, 'w').write(file_content.replace(replace_text, replace_value))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~ Read color values from json file ~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

for colorName, colorObject in config_map.items():
    color_from_json = read_color_from_json(colorName)
    set_config_map_color(colorName, color_from_json)

primaryColor = get_config_map_color('primaryColor')
primaryColorLight = get_config_map_color('primaryColorLight')
primaryColorDark = get_config_map_color('primaryColorDark')
primaryTextColor = get_config_map_color('primaryTextColor')
secondaryColor = get_config_map_color('secondaryColor')
secondaryColorLight = get_config_map_color('secondaryColorLight')
secondaryColorDark = get_config_map_color('secondaryColorDark')
secondaryTextColor = get_config_map_color('secondaryTextColor')

if primaryColor is None:
    raise('primaryColor is not defined')
if secondaryColor is None:
    raise('secondaryColor is not defined')

brightTextColor = color_brighten(primaryColor, 0.8)
darkTextColor = color_darken(primaryColor, 0.9)

if primaryColorLight is None:
    set_config_map_color('primaryColorLight', color_brighten(primaryColor, 0.4))
if primaryColorDark is None:
    set_config_map_color('primaryColorDark', color_darken(primaryColor, 0.4))
if primaryTextColor is None:
    set_config_map_color('primaryTextColor', get_contrast_color(primaryColor, brightTextColor, darkTextColor))

if secondaryColorLight is None:
    set_config_map_color('secondaryColorLight', color_brighten(secondaryColor, 0.4))
if secondaryColorDark is None:
    set_config_map_color('secondaryColorDark', color_darken(secondaryColor, 0.4))
if secondaryTextColor is None:
    set_config_map_color('secondaryTextColor', get_contrast_color(secondaryColor, brightTextColor, darkTextColor))


for colorName, _ in config_map.items():
    color = get_config_map_color(colorName)
    replace_string = get_config_map_color_replace_string(colorName)
    if color is None:
        print(f"The color '{colorName}' is still undefined, skipping...")
        continue
    hex_numbers = color.hex_l.lstrip('#') # Must be only the numbers without the '#' for LaTEX
    replace_in_files(replace_string, hex_numbers)