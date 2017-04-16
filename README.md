# FYP_tfl

# Stuff to do

- For phase in stage keep in mind that all the non-specified signal groups should show red by assumption

- ~~Make a base case so I don't crawl the file forever -> while line != None: ne6ta~~

- ~~Read from plan array, so you know when stages switch~~

- Edit plan array depending on the PDDL result

- ~~Think of way to exit the program safely (No license for Vissim, Vissim not installed, etc)~~

- ~~Ask Michael about interstages? - Don't think about it~~

- ~~Max green time??? - Don't thnik about it~~

- ~~Supports both tabs and spaces bt replacing tabs with spaces~~

- Handle no such file I guess

- := used when using variables?? Would not support shit like that

- ~~Make sure that the Link names match -> rename everything that has no name~~

- On extracting stages, work with Regex if not lazy enough

- Everything will crash if the signal controller is not VAP

- If original VAP file has no PLAN[x,y] = [];, then it won't work

- Look at COM interface, at Vissim page. Basically when I finish setting new source file, call SaveNet() or SaveNetAs()

- Call BringToFront() so the window requests focus

- Might look onto LoadProject instead of LoadNet, but prolly I won't, too much effort for something that's already fixed
