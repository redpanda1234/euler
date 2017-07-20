# Euler & friends

This repo contains a set of two euler's method based numerical
integration tools.  The first, efficient\_nbody, is a Python-based
barnes-hut simulator, which uses a tree-based approximation scheme
(described [here](http://www.cs.princeton.edu/courses/archive/fall03/cs126/assignments/barnes-hut.html)) to try and cut the computational complexity of
the animation.  The second contains starter files + diagrams +
solutions for a CS 5 extra credit assignment at Harvey Mudd College
involving using Euler's method to plot the Lorenz Attractor.  If any
of the instructions below don't work and/o are unclear, please  feel
free to submit an issue report [here](https://github.com/ScriptingBeyondCS/euler/issues) (it would help me out a lot).

## Dependencies

All of my programs require a python3 install.  If you don't have
python on your machine (and are on OSX), see the section on homebrew
below for instructions on installing python.  Otherwise, try googling
for your specific OS.

To run a sample n-body simulation or lorenz animation, you'll first
need to install the dependencies.  First, a brief overview of the
stuff I'm using: my n-body program uses numpy to store most of the
internal data as nice arrays, PIL (python image library / pillow) to
draw each of the individual frames, progressbar2 so that you can tell
how fast your program is going / how far along in the animation it is,
and ffmpeg to stitch each of the individual frames together.  For the
lorenz attractor animations, I use numpy (for similar reasons as
above), and matplotlib to create the animation itself.  Most of these
can be easily fetched (assuming you already have python3 installed)
with

```$ pip install requirements.txt```

Note that the $ just means "type this in the terminal" --- don't
actually paste the $ character into your command line.  Anyways, (if
that doesn't work), you might have to try


```$ pip3 install requirements.txt```

I haven't tested my stuff with python 2.7x yet (and probably won't get
around to doing so anytime soon), so I can't guarantee that anything
will work if you're using an earlier version of python.

To install ffmpeg,
 + If you're on OSX, first install [homebrew](https://brew.sh/) (literally a godsend
   for developing on OSX), then in the terminal type
   ```$ brew install ffmpeg```
   If it's your first time using homebrew, it might ask you something
   about sudo permissions.  Don't worry, brew doesn't bite --- it
   should be safe.

   Basically, homebrew (like pip) is a package manager, meaning it
   facilitates painless installation of packages etc.  It has two main
   commands you'll interact with:
   - ```$ brew install``` and
   - ```$ brew cask install```
   Essentially, ```$ brew install``` is for installing things that you
   interact with on the command line --- e.g., python and ffmpeg.  For
   things that have a graphical user interface (GUI), you use ```$
   brew cask install``` --- as an example, you can ```$ brew cask
   install spotify```

   Note that if you don't have python installed yet, you can ```$ brew
   install python3 ```

   pip, on the other hand, is a package manager specifically for
   python packages.  One might cynically cite [xkcd](https://xkcd.com/927/) upon
   hearing this, but honestly, it's kind of easier this way.

 + If you're on Windows, good luck.  I managed to set it up once on my
   desktop, and then forgot how I did it.  I remember it being
   somewhat painful, though.

 + If you're on Ubuntu / Linux, you probably know what to do anyways
   and/or can figure it out yourself.

### Helpful tidbits if you're just starting out
While you're at it, if you don't have it already, I would highly
recommend interacting with python through the ipython shell.  To get
it, try

```$ pip install ipython```
Or
```$ pip3 install ipython```

To open the ipython shell, you can just type ```ipython``` in your
terminal / command line.  You should see a friendly green ```In[1]
:``` appear.

Finally, for those who don't know, if you want to quickly clone my
project and all of its files, you should first install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) (very
easy with homebrew, as explained below), open your terminal and cd
(command for changind directories) to a convenient directory, then
```$ git clone https://github.com/ScriptingBeyondCS/euler.git```
You can then cd into the euler folder and run everything etc.

## Running programs

I assume you've installed the dependencies.  If you haven't yet, then
the following probably won't work.

+ To run my n-body simulator, you'll want to first cd into the
  efficient\_nbody directory.  Once you're there, you should start the
  ipython shell by typing ```$ ipython``` in your terminal / command
  line.

  - In the ipython shell, load the simulator with
    ```In[1] : run barnes_hut.py```
    Here, the ```In[1] :``` is not something you should actually type
    --- it's just meant to show that you should enter the command in
        the ipython shell.

  - Then, call the wrapper function on one of the raw data files in
    the raw\_data directory.  An example call might be

    ```In[2]: wrapper("galaxy1.txt")```

    You can change a number of the default factors in the simulation
    with keyword arguments.  See the documentation in the file for
    more details (I'll try put the information here in the README
    soon, submit an issue later if I appear to have forgotten to do
    so)!

  - By default, the output video will be written to a tests folder in
    the current directory.  It will create a output movie with both a
    boxed version (showing the recursive tree structure) and an
    unboxed version (with just the masses shown).  Disabling one of
    these _might_ increase the speed of the simulation, but I haven't
    tested this.

  - For more information on the raw data files, see the README in that
    directory.

+ To run the lorenz simulator, cd into eulers_method/solutions, and
  start an ipython shell (instructions above).  Then, just try

  ```In[1]: run animate.py```

  And the plot window should appear.  If you want to plot a different
  system of differential equations with the same animation engine, you
  should modify the ```lorenz_deriv``` function in ```euler.py```, or
  create a new function yourself.  You might need to tweak the intial
  conditions, or modify the axial range limits.  Both of those
  conditions can be changed in the ```animate.py```
