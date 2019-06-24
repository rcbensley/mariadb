## Pre-amble-ramble
I have a love-hate relationship with Python.
I love that it's widely used by students, professionals, scientists, researchers, journalists, etc.
The amount of mind share around python is unprecedented and unmatched.

I hate that it's ubiquity was partly responsible for the demise of Scheme and Lisp. Boo!
I love that some of what makes Lisp awesome is in Python. Yay!

## Versions
|OS|Version|Source|Notes|
|CentOS 7.x|3.4|EPEL| |
|CentOS 7.x|3.6|EPEL|Does not include python36-pip|
|Debian|3.x|Stable| |
|MacOS|3.7|Homebrew|Python 3 is now the default when installing from homebrew, i.e. ```brew install python```|

## Environment
* PATH
* PYTHONPATH
* site-packages, user-packages.

## REPL, Read-Eval-Print-Loop
* ipython

## Editor
Anything you are comfortable in. 

### Editor Plugins
* I use vim and sublimetext. Vim with ctags allows me to explore a project quickly, sublime text has built in file and symbol matching.
* I use autopep8 on the command line to prettify my work.
* I have recovered from my IDE hangover.

## Modules
My DBA favourites:
* Turbodbc, making ODBC great again.
* PyODBC, pure python, more portable than Turobodbc.
* toolz and cytoolz.
* hy, lisp on python!
* tabulate, pretty print your data, impress your friends.
* sqlite, file based database.
* shelve, persist objects.
* configparser, read and write config files, don't hard code your passwords.
* argparse, make your STDIN, STDAWESOME.

No Pandas? No Numpy? No Tensorflow? Well...no. There is always a database at hand!


## Other Resources
* [Alice in Python Project Land](http://veekaybee.github.io/2017/09/26/python-packaging/?utm_source=mybridge&utm_medium=blog&utm_campaign=read_more), nice writeup about the pains of writing and packaging python, with solutions.
* [PyTudes](https://github.com/norvig/pytudes)
* [Composing Programs](http://www.composingprograms.com), the SICP successor for python.
* [Automate the Boring Stuff with Python](https://automatetheboringstuff.com)
