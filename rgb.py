import math
def rgb2hsv(r:int, g:int, b:int):
    """ Converts an RGB colour to HSV """
    h = 0
    s = 0
    v = 0
    # constrain the values to the range 0 to 1
#     print(f'r: {r}, g: {g}, b: {b}, hue: {h}, saturation: {s}, brightness: {v}')
    r_normal, g_normal, b_normal,  = int(r) / 255, int(g) / 255, int(b) / 255
    cmax = max(r_normal, g_normal, b_normal)
    cmin = min(r_normal, g_normal, b_normal)
    delta = cmax - cmin
    
    # Hue calculation
    if(delta ==0):
        h = 0
    elif (cmax == r_normal):
        h = (60 * (((g_normal - b_normal) / delta) % 6))
    elif (cmax == g_normal):
        h = (60 * (((b_normal - r_normal) / delta) + 2))
    elif (cmax == b_normal):
        h = (60 * (((r_normal - g_normal) / delta) + 4))
    
    # Saturation calculation
    if cmax== 0:
        s = 0
    else:
        s = delta / cmax
        
    # Value calculation
    v = cmax
    
    h = h / 360
    
    colour = {'hue':h,'sat':s,'val':v}
#     print(f'converted colour is: {colour}')
    
    return colour     

def hsv2rgb(hue:float, sat:float, val:float):
    """ Sets the Hue Saturation and Value of the indexed RGB LED"""

    i = math.floor(hue * 6)
    f = hue * 6 - i
    p = val * (1 - sat)
    q = val * (1 - f * sat)
    t = val * (1 - (1 - f) * sat)

    r, g, b = [
        (val, t, p),
        (q, val, p),
        (p, val, t),
        (p, q, val),
        (t, p, val),
        (val, p, q),
    ][int(i % 6)]
    r = int(r*255)
    g = int(g*255)
    b = int(b*255)
    
    colour = {'red':r, 'green': g, 'blue':b}
    
    return colour

def mix(rgb1, rgb2):
    """ Mixes two RGB colours """
    r = (rgb1['red'] + rgb2['red']) / 2
    g = (rgb1['green'] + rgb2['green']) / 2
    b = (rgb1['blue'] + rgb2['blue']) / 2
    return {'red':r, 'green': g, 'blue':b}

def fade(rgb1, rgb2, amount:float):
    """ Fades between two RGB colours """
    r = int((rgb1['red'] * (1 - amount) + rgb2['red'] * amount))
    g = int((rgb1['green'] * (1 - amount) + rgb2['green'] * amount))
    b = int((rgb1['blue'] * (1 - amount) + rgb2['blue'] * amount))
    return {'red':r, 'green': g, 'blue':b}

def hex_to_rgb(hex):
    # converts a hex colour code into RGB
    h = hex.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return r, g, b

def rgb_to_hex(rgb):
    # converts an RGB colour into a hex code
    return '#%02x%02x%02x' % rgb