# Random Color library
[![CodeQL](https://github.com/beh185/RandomColorlib/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/beh185/RandomColorlib/actions/workflows/codeql.yml)

https://user-images.githubusercontent.com/79264026/172701097-337571d8-23fd-45a1-8cdc-72b97acc0176.mp4


**This Python library makes your terminal output colorful ✨**\
On this Python library, you can access 255 kinds of color randomly!\
**There are just 15 colors for windows(***cmd***) users 😥**
## YouTube Tutorial 📹
# installation 
for installation, first make sure that you're in **RandomColorlib** folder, which **setup.py** exists, \
then enter this command in your terminal:
> `pip install .`
## features

- [Change front color](#changing-front-color)
- [Change background color](#changing-background-color)
- [Change font (style)](#change-font-style)
- [Change front color with background color at same time](#multiple-capabilities)
- [Change front color with font at same time](#multiple-capabilities)
- [Change background with font at same time](#multiple-capabilities)
- [Change front color with background color and font at the same time](#multiple-capabilities)

---
# Usage
## importing
For importing the library You can use the following:
```python 
# First way 
import RandomColor
RandomColor.Rcolor.<Module Name>

# Easier way
from RandomColor import Rcolor

# For importing all modules:
from RandomColor.Rcolor import * 
```
------

## **Important tip**
cmd can't support all colors so it's better to use :
``` python 
from RandomColor import Rcolor

print(Rcolor.windows_color("Hello, World")) # random color
print(Rcolor.windows_background("Hello, World")) # random background
``` 
- You can use the **Auto** part too, Which doesn't depend on the operating system and automatically detects the operating system

```python
from RandomColor import Rcolor

print(Rcolor.auto_color("Hello, World")) # Automatic random color
print(Rcolor.auto_background("Hello, World")) # Automatic random background
```

## Changing font color 
**Make Sure to check [Important tip](#important-tip)**
```python
from RandomColor import Rcolor

print(Rcolor.color('Hello, World!'))
print(Rcolor.windows_color("Hello, World")) 
```
----
## Changing Background color
**Make Sure to check [Important tip](#important-tip)**

```python
from RandomColor import Rcolor

print(Rcolor.background('Hello, World'))
print(Rcolor.windows_background('Hello, World')) 
```
## Changing font (style)
**Make Sure to check [Important tip](#important-tip)**

```python
from RandomColor import Rcolor
Rcolor.style('Hello, World!')
```
---

## Multiple capabilities
```python
from RandomColor import Rcolor

# Change front color with background color at the same time
Rcolor.color_background("Hello world")

# Change the front color with the font at the same time
Rcolor.color_style("Hello world")

# Change background with font at the same time
Rcolor.background_style("Hello world")

# Change front color with background color and font at the same time
Rcolor.color_background_style("Hello world") 
```
