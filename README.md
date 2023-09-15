# Random Color library

[![CodeQL](https://github.com/beh185/RandomColorlib/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/beh185/RandomColorlib/actions/workflows/codeql.yml)

https://user-images.githubusercontent.com/79264026/172701097-337571d8-23fd-45a1-8cdc-72b97acc0176.mp4


**This Python library makes your terminal output colorful ✨**\
On this Python library, you can access 255 kinds of color randomly!\
## YouTube Tutorial 📹
# installation 
For installation, enter this command in your terminal:
> `pip install Rcolor==2.0.3`
## features

- [Change foreground color](#changing-foreground-color)
- [Change background color](#changing-background-color)
- [Change font (style)](#changing-font-style)
- [change foreground color for each character](#change-foreground-color-for-each-character)
- [Change foreground and background color at the same time](#multiple-capabilities)
- [Change foreground and font at the same time](#multiple-capabilities)
- [Change background and font at the same time](#multiple-capabilities)
- [Change foreground and background color and font at the same time](#multiple-capabilities)

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
Some terminal like cmd can't support all colors so it's better to use standard colors:
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

## Changing foreground color
**Make Sure to check [Important tip](#important-tip)**
```python
import Rcolor

print(Rcolor.foreground('Hello, World!'))  # to use 255 colors
print(Rcolor.standard_fg("Hello, World"))  # to use standard color (15 colors).
```
----
## Changing Background color
**Make Sure to check [Important tip](#important-tip)**

```python
import Rcolor

print(Rcolor.background('Hello, World')) # to use 255 colors
print(Rcolor.standard_bg('Hello, World')) # to use standard color (15 colors).
```
## Changing font (style)
**Make Sure to check [Important tip](#important-tip)**

```python
import Rcolor
print(Rcolor.style('Hello, World!'))
```
---
## Change foreground color for each character
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

# Changes foreground color and background color at the same time
Rcolor.foreground_background("Hello world")

# Changes the foreground color and the font at the same time
Rcolor.foreground_style("Hello world")

# Changes background color and font at the same time
Rcolor.background_style("Hello world")

# Changes foreground color and background color and font at the same time
Rcolor.foreground_background_style("Hello world") 
```
