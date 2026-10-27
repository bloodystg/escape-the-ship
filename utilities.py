import settings # gives us the window WIDTH and HEIGHT


def height_prct(percentage): # turn a percent of the window's height into pixels
    return (settings.HEIGHT / 100) * percentage # e.g. 25% of 720 = 180 pixels

def width_prct(percentage): # turn a percent of the window's width into pixels
    return (settings.WIDTH/ 100) * percentage # e.g. 25% of 1440 = 360 pixels