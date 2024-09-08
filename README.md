# Random Color library

[![CodeQL](https://github.com/ibehii/RandomColorlib/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/ibehii/RandomColorlib/actions/workflows/codeql.yml)

https://github.com/ibehii/RandomColorlib/assets/79264026/0daa3c30-3f45-4abc-8343-0d6ce11ee20b

**This Python library makes your terminal output colorful ✨**\
On this Python library, you can access 255 kinds of color randomly!
## YouTube Tutorial 📹
# installation 
For installation, enter this command in your terminal:
> `pip install Rcolor==3.0.1`
## features

- [Change the foreground color](#changing-the-foreground-color)
- [Change the background color](#changing-the-background-color)
- [Change the font (style)](#changing-the-font-style)
- [change the foreground color for each character](#change-the-foreground-color-for-each-character)
- [Change foreground and background color at the same time](#multiple-capabilities)
- [Change foreground and font at the same time](#multiple-capabilities)
- [Change background and font at the same time](#multiple-capabilities)
- [Change foreground, background color and font at the same time](#multiple-capabilities)

---
# Usage
## importing
For importing the library You can use the following:
```python 
# First way 
import Rcolor
Rcolor.<Module Name>

# Easier way
from Rcolor import <Module Name>

# For importing all modules (Not recommended):
from Rcolor import * 
```
------

## **Important tip**
Some terminals like cmd can't support all colors so it's better to use standard colors:
``` python 
import Rcolor

print(Rcolor.standard_fg("Hello, World")) # random foreground color
print(Rcolor.standard_bg("Hello, World")) # random background color
print(Rcolor.standard_rainbow_fg("Hello world")) # to change foreground for each character using standard colors
``` 
- You can use the **Auto** part too, Which doesn't depend on the operating system and automatically detects the operating system

```python
import Rcolor

print(Rcolor.auto_fg("Hello, World")) # Automatic random foreground color
print(Rcolor.auto_bg("Hello, World")) # Automatic random background color
```

## Changing the foreground color
**Make Sure to check [Important tip](#important-tip)**
```python
import Rcolor

print(Rcolor.foreground('Hello, World!'))  # to use 255 colors
print(Rcolor.standard_fg("Hello, World"))  # to use standard color (15 colors).
```
----
## Changing the Background color
**Make Sure to check [Important tip](#important-tip)**

```python
import Rcolor

print(Rcolor.background('Hello, World')) # to use 255 colors
print(Rcolor.standard_bg('Hello, World')) # to use standard color (15 colors).
```
## Changing the font (style)
**Make Sure to check [Important tip](#important-tip)**

```python
import Rcolor
print(Rcolor.style('Hello, World!'))
```
---
## Change the foreground color for each character
**Make Sure to check [Important tip](#important-tip)**
```python
import Rcolor
print(Rcolor.rainbow_fg("Hello world"))
print(Rcolor.standard_rainbow_fg("Hello world"))
```

---
## Multiple capabilities
```python
import Rcolor

# Changes the foreground color and background color at the same time
Rcolor.foreground_background("Hello world")

# Changes the the foreground color and the font at the same time
Rcolor.foreground_style("Hello world")

# Changes the background color and font at the same time
Rcolor.background_style("Hello world")

# Changes foreground color, background color and font at the same time
Rcolor.foreground_background_style("Hello world") 
```
