#ensure that config is passed
import os
import random
from colormap import rgb2hls, hls2rgb

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config["allowed_extensions"] #rewrite this. this is embarassingly bad

def create_dir(path):
    try: os.makedirs(path)
    except: pass

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
        except: print(f"{color}\n{type(color)}")
    return ret

def convert_to_chartjs(ctfs, teams, normalize=True):
    ret_ctfs, ret_teams, scaled_teams=[],[],{}
    for ctf in ctfs:
        scaled_teams[ctf]=normalize_teams(ctfs[ctf]["data"]) if normalize else ctfs[ctf]["data"]
        ret_ctfs.append({"label":ctf, "data": scaled_teams[ctf], "backgroundColor":ctfs[ctf]["backgroundColor"]})
    for index, team in enumerate(teams):
        relative, literal = 0,0
        for ctf in scaled_teams:
            try:
                literal+=ctfs[ctf]["data"][index]
                relative+=scaled_teams[ctf][index]
            except:pass
        ret_teams.append((team, int(relative), int(literal)))
    ret_teams=sorted(ret_teams, key=lambda x: x[1], reverse=True)
    return ret_ctfs, ret_teams

def insert_at_index(inlist, index, value):
    ret, value=inlist, int(value)
    try: ret[index]=value
    except: ret += ([0]*(index-len(ret))+[value])
    return ret

def normalize_teams(ctfs):
    return [100*(value//max(ctfs)) for value in ctfs]