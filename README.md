# Random Color library for python


     

https://user-images.githubusercontent.com/79264026/172701097-337571d8-23fd-45a1-8cdc-72b97acc0176.mp4


        
On this python library you can access 255 kind of color randomly!
**There is just 15 colors for windows users :(**
## features

- Random color 
- Random background
- Random style
- Random color with random background
- Random color with random style
- Random background with random style
- Random color with random background and random style

---
**Windows Users** have to install [colorama](https://pypi.org/project/colorama/).
for installing : 

>pip install colorama

## **Important tip**
cmd can't support all colors so it's better use :
``` python 
import Rcolor
Rcolor.windows_color("Hello world") # random color
Rcolor.windows_background("Hello world") # random background
``` 
- You can use **Auto** part too, Which doesn't depend on the operating system and automatically detects the operating system
```python
import Rcolor
Rcolor.auto_color("Hello world") # Automatic random color
Rcolor.auto_background("Hello world") # Automatic random background
```

for using random style(font) :
>`Rcolor.style("Hello world")`

### Multiple capabilities ###
```python
import Rcolor
Rcolor.color_background("Hello world") # Random color with Random background
Rcolor.color_style("Hello world") # Random color with Random style
Rcolor.background_style("Hello world") # Random background with style
Rcolor.color_background_style("Hello world") # Random color with random background and random style
```
