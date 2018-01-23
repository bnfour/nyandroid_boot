# ![nyancat](http://telegra.ph/file/d21338914a31033f4be45.gif) nyandroid_boot
Quick and dirty Python script to generate nyancat boot anmations for Android, designed with 1280×800 in mind.

This script generates a [bootanimation.zip](https://android.googlesource.com/platform/frameworks/base/+/master/cmds/bootanimation/FORMAT.md) file
which contains a seamlessly looping boot animation where a nyancat flies from beyond the left edge of the screen to center and stays there until device is booted.

This script depends on [Pillow](https://pillow.readthedocs.io).

Image mockup via [placeit](https://placeit.net):

![mockup](http://telegra.ph/file/0637fcdb757aef351d75b.png)

Image is cropped to 800×800 by default for performance reasons. Looks like KitKat does not support background color setting. 

## Animation installation
**Do understand what are you doing, don't do stuff just because internets told you so.**

*Root is needed.*

copy resulting `bootanimation.zip` to `/system/media` and set it's permissions to `-rw-r--r--`.
