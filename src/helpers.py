#ensure that config is passed
import os
import random
from colormap import rgb2hls, hls2rgb

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config["allowed_extensions"] #rewrite this. this is embarassingly bad

def create_dir(path):
    try: os.makedirs(path)
    except: pass

def normalize_scores():
    pass

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

def adjust_color_lightness(r, g, b, factor):
    h, l, s = rgb2hls(r / 255.0, g / 255.0, b / 255.0)
    l = max(min(l * factor, 1.0), 0.0)
    r, g, b = hls2rgb(h, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))

def darken_color(tup, factor=0.15):
    r, g, b = tup
    return adjust_color_lightness(r, g, b, 1 - factor)

def preconvert_to_chartjs(ctfs):
    ret, color={}, hex_to_rgb("#"+str(hex(random.randint(1000000,16777215)))[2:])
    for ctf in ctfs:
        ret[ctf]={"data":[], "backgroundColor":f"rgb{color+(0.5,)}"}
        try: color=darken_color(color)
        except:
            print(color)
            print(type(color))
    return ret

def convert_to_chartjs(ctfs, scale=True):
    return [{"label":ctf, "data": scale_teams(ctfs[ctf]["data"]) if scale else ctfs[ctf]["data"], "backgroundColor":ctfs[ctf]["backgroundColor"]} for ctf in ctfs]

def insert_at_index(inlist, index, value):
    ret, value=inlist, int(value)
    try: ret[index]=value
    except: ret += ([0]*(index-len(ret))+[value])
    return ret

def scale_teams(ctfs):
    return [100*(value/max(ctfs)) for value in ctfs]