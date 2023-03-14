```
  _____            ____            _
 | ____|__ _  __ _| __ )  __ _ ___| | __
 |  _| / _` |/ _` |  _ \ / _` / __| |/ /
 | |__| (_| | (_| | |_) | (_| \__ \   <
 |_____\__, |\__, |____/ \__,_|___/_|\_\
       |___/ |___/
```
# eggbask

A python script to organise all your cool emulation stuff

![](https://github.com/Potat0SSack/eggbask/blob/main/showcase.gif)

___

# Why does this exist?
<details>
  <summary>Click me</summary>
I made this because i wanted to have a simple way to organise emulators and roms into one place. You may say "Why not use RetroArch then?" and that's a valid argument. My response is that i don't like RetroArch's gui and, more importantly atleast for me, RetroArch performs way worse. While i have a moderately good desktop which runs RetroArch just fine, i also have multiple low-end laptops (2GB of RAM, Dual Core proccessor) that run standalone emulators no problem but struggle heavily with RetroArch. Plus they both run linux and navigating file browsers and such on such low-end laptops is a very slow and, to an extent, painful process even after replacing the default desktop environments. However, typing in commands in a terminal is much faster and easier for me personally. And since i couldn't find any tools or utilites that matched my wants, i DIY'd one myself.
</details>

# Features

* Allows you to organise your emulators and ports
* Edit emulator and port configs
* Launch ROMS, emulators and ports all from the command line

More features will be added in the future.
___

# Installation

First make sure you have downloaded click for python by running `pip install click`
if you didn't have it pip will install click as well as any otherr dependencies

After than open your terminal and run
```
  git clone https://github.com/Potat0SSack/eggbask
  cd eggbask
  python eggbask.py
```

After you run the last command you should get a --help list with all of the commands.
