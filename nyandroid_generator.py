# nyancat android boot animation generator
# Bn4, 22/01/18
from PIL import Image
from random import randint
import zipfile
from os import makedirs

# image size and scale multiplier
w, h = 80, 80
image_size = (w, h)
scale = 10
# misc settings
bg_color = (0, 51, 102, 255)
# <3 python
bg_color_hex = "#" + "".join(hex(i)[2::].zfill(2) for i in bg_color[:3:])
animation_fps = 15
# folder to output content before zipping
output_folder = "output"
# ensure there are folders to write
for i in range(2):
    makedirs("{}/part{}/".format(output_folder, i), exist_ok=True)


# abstract sprite class
class Sprite(object):

    filename = None  # filename mask to load images, must have slot for one int
    frames = None  # holds the frames
    frames_counter = 0  # used as number of frames first, then as frame number
    velocity = 0
    position = (0, 0)  # top left angle

    # loads images
    def __init__(self):
        self.frames = tuple(Image.open(self.filename.format(i)).convert("RGBA")
                            for i in range(self.frames_counter))
        self.frames_counter = 0

    # sets position
    def set_position(self, pos):
        self.position = pos

    # moves sprite on x-axis, switches frames
    def update(self):
        x, y = self.position
        x += self.velocity
        self.position = (x, y)
        self.frames_counter = (self.frames_counter + 1) % len(self.frames)

    # pastes itself to background
    def draw(self, canvas):
        img = self.frames[self.frames_counter]
        # image used as mask of itself for transparency
        canvas.paste(img, self.position, img)


# class for nyancat sprite, loads 12 images from nyancat/,
# default velocity is 1, set to 0 on animation part switches
class Nyancat(Sprite):

    filename = "nyancat/frame_{:02d}.gif"
    frames_counter = 12
    velocity = 1


# Star class, similar to Nyancat...
class Star(Sprite):

    filename = "star/frame_{:02d}.gif"
    frames_counter = 6
    velocity = -4

    # ...except it's starting frame is random
    def __init__(self):
        super().__init__()
        self.frames_counter = randint(0, len(self.frames) - 1)

    # also it wraps around screen borders
    def update(self):
        super().update()
        x, y = self.position
        if x < 0:
            x += w
        self.position = (x, y)


# pretty much the Star, but frames go in reverse
class ReversedStar(Star):

    def update(self):
        # it gets a +1 in super's update, -1 in total
        self.frames_counter -= 2
        super().update()


# background to copy
canvas_source = Image.new("RGBA", image_size, bg_color)
# our glorious sprite
nya = Nyancat()
# get it's dimensions and set it properly
nyancat_w, nyancat_h = nya.frames[0].size
nya.set_position((-(nyancat_w + 1), (h - nyancat_h) // 2))
# create a Star instance to peek on its sprite dimensions
tmp = Star()
star_w, star_h = tmp.frames[0].size
del tmp
# all the stars the sky can hold
rendergroup = []
for i in range(h // (star_h + 1)):
    x = randint(0, w)
    y = 1 + (8 * i)
    star = Star() if randint(0, 1) else ReversedStar()
    star.set_position((x, y))
    rendergroup.append(star)
# the first 58 frames are first part (part0) of animation played once
#  58 is the frame count to make cat fly to the center of 800-width screen
# rest is second part (part1) looped to infinity and beyond
part = 0
# keeping track on what to zip later via this list of filenames
filenames = []
# second part consists of 60 frames:
#  it takes 12 frames to fully loop the nyancat
#  and 20 to fully loop the stars
#  least common multiple of 12 and 20 is 60
for i in range(nyancat_w + 1 + 60):
    if i == nyancat_w + 1:
        nya.velocity = 0
        part = 1
    canvas = canvas_source.copy()
    # update and draw stars
    for sprite in rendergroup:
        sprite.update()
        sprite.draw(canvas)
    # update and draw cat
    nya.update()
    nya.draw(canvas)
    # upscale, save, remember the file name
    upscaled = canvas.resize((i * scale for i in image_size)).convert("RGB")
    image_name = "part{}/{:03d}.png".format(part, i)
    upscaled.save(output_folder + "/" + image_name, optimize=True)
    filenames.append(image_name)
# generating the description of the two parts
with open("{}/desc.txt".format(output_folder), 'w') as desc_file:
    desc_file.write("{} {} {}\n".format(w * scale, h * scale, animation_fps))
    # yep, hardcoded
    desc_file.write("p 1 0 part0 {}\n".format(bg_color_hex))
    desc_file.write("p 0 0 part1 {}\n".format(bg_color_hex))
# zipping everything without compression
filenames.append("desc.txt")  # this file also should be zipped
with zipfile.ZipFile("bootanimation.zip", 'w') as zip_file:
    for filename in filenames:
        # we grab files from the output folder, but save them to archive's root
        zip_file.write("{}/{}".format(output_folder, filename), filename)
