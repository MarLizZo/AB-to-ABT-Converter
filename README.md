# Python AB to ABT Converter

Python tool to convert old AB files into the newest ABT-like format
This was a private project for a friend, but i decided to make it public as there are no public converters out there.

An .AB file contains the configuration of all the control units/modules of a FORD car.

<hr>

### How it works?

-   This tool take an AB as input and return a folder named with the chassis code of the car (taken from the AB obviously).
-   Inside this folder it will create as much folders as control units/modules found inside the AB file.
-   In the end, inside every cu/module folder you'll find the .ABT file ready to be used with the Forscan software.

How to use it to convert your AB file? Very very simple..
Take your AB file and drop it over the .py file :)

<hr>

### Requirements

Latest Python 3 version.
To run this tool you'll also need the package 'colorama'. My tool uses this package to give some colors to the output.
To install colorama simply run this command:

```python
pip install colorama
```

**NOTE: If this does not work, try pip3 instead of pip**

<hr>

### Portable EXE File

I have included an exe portable build in the release page. This exe is built with pyinstaller. If you are not comfortable with Python and you don't want to install it, you have this possibility.
By using the exe file you don't even need to run the pip install command, just drag and drop your AB file over the exe and that's it!
