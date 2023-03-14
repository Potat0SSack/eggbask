# eggbask
a python script to organise cool emulation stuff

___

# Why does this exist?
I made this because i wanted to have a simple way to organise emulators and roms into one place. You may say *"Why not use RetroArch then?"* and that's a valid argument. My response is that i don't like RetroArch's gui and, more importantly atleast for me, **RetroArch performs way worse**. While i have a moderately good desktop which runs RetroArch just fine, i also have multiple low-end laptops (2GB of RAM, Dual Core proccessor) that run standalone emulators no problem but struggle *heavily* with RetroArch. Plus they both run linux and navigating file browsers and such on such low-end laptops is a very slow and, to an extent, painful process even after replacing the default desktop environments (no i don't like using stuff like i3 WM). However, typing in commands in a terminal is much faster and easier for me personally. And since i couldn't find any tools or utilites that matched with my wants, i DIY'd one myself.

___

It's probably very poorly written, is missing some crucial features that apps like RetroArch have but it can, *at the very least*, add emulator profiles, add rom directories and run roms with the afore mention emulator profiles. There is also an option to add and run ports but it's also underdeveloped.

I highly doubt this is practical in it's current state but hey, if you want to you can try it out.

___

# Installation
Make a folder somewhere, name it whatever and drop the script in there. Why have a seperate folder? Cause the script makes it's own folders and idk just don't forget about the folder it creates otherwise put it wherever you want.

After that just run the script in a terminal, it should print out an automatic help list with all commands listed. From there just add an emulator via `add emu`, optionally add a rom folder for convinience via `add romfolder` and finally, run the roms you want via `run rom`. Have fun!
