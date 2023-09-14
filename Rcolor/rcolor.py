# Github: https://github.com/beh185
# Telegram: https://T.me/dr_xz
# e-mail: Behii@tutanota.com
# ____________________________________________

# ======== # import built-in library # ======== #
from random import choice 
from os import name
from json import load

# ======== # random foreground # ======== #
def color(*user_input) -> str:
    '''Change foreground of output to 255 different colors, but it may not work in every terminal.'''
    try:
        # ====== # Opening json file that contain colors code in windows and linux # ====== #
        if(name == 'nt'):
            json_paths: str = __file__.replace('rcolor.py', 'colors\\colors.json')
        else:    
            json_paths: str = __file__.replace('rcolor.py', 'colors/colors.json')
        with open(json_paths , 'r') as f:
            colors: list[str] = load(f).get("colors")
        user_input = list(user_input)
        
        # ======== # make all item in user_input list to string  # ======== #
        for i in user_input:
            if type(i) == str:
                pass
            else:
                user_input[user_input.index(i)] = str(i)

        user_input = ''.join(user_input)
        random_color: str = choice(colors)
        
        return random_color + user_input + '\033[0m'
    except FileNotFoundError:
        pass
        return('\33[31m' + '"colors.json" did not found.\nIt\'s may because the file was moved or deleted' + '\033[0m')        
    except TypeError:
        pass
        return('\33[31m' + f'Input type {type(i)} is not supported' + '\033[0m')

# ======== # random background color # ======== #
def background(*user_input) -> str:
    '''Change background color of output to 255 different colors, but it may not work in every terminal.'''
    try:
        # ====== # Opening json file that contain colors code in windows and linux # ====== #
        if name == 'nt':
            json_paths: str = __file__.replace('rcolor.py', 'colors\background_color.json')
        else:    
            json_paths: str = __file__.replace('rcolor.py', 'colors/background_color.json')
        with open(json_paths, 'r') as f:
            background_color: list[str] = load(f).get("background_color")
        user_input = list(user_input)

        # ======== # make all item in user_input list to string # ======== #
        for i in user_input:
            if type(i) == str:
                pass
            else:
                user_input[user_input.index(i)] = str(i)

        user_input = ''.join(user_input)
        random_color: str = choice(background_color)
        return random_color + user_input + '\033[0m'
    except FileNotFoundError:
        pass
        return('\33[31m' + '"background_color.json" did not found.\nIt\'s may because the file was moved or deleted' + '\033[0m')        
    except TypeError:
        pass
        return('\33[31m' + f'Input type {type(i)} is not supported' + '\033[0m')

# ======== # Random Windows color # ======== #
def windows_color(*user_input) -> str:
    '''Change foreground of output to 15 different colors. It use standard colors so it work in every terminal.'''
    try:
        # ====== # Opening json file that contain colors code in windows and linux # ====== #
        if name == 'nt':
            json_paths: str = __file__.replace('rcolor.py', 'colors\\Windows_color.json')
        else:    
            json_paths: str = __file__.replace('rcolor.py', 'colors/Windows_color.json')
        with open(json_paths, 'r') as f:
            windows_color: list[str] = load(f).get("Windows_color")
        user_input = list(user_input)

        # ======== # make all item in user_input list to string # ======== #
        for i in user_input:
            if type(i) == str:
                pass
            else:
                user_input[user_input.index(i)] = str(i)
        from colorama import just_fix_windows_console
        just_fix_windows_console()
        user_input = ''.join(user_input)
        random_color: str = choice(windows_color)
        return random_color + user_input + '\033[0m'
    except FileNotFoundError:
        pass
        return('\33[31m' + '"Windows_color.json" did not found.\nIt\'s may because the file was moved or deleted' + '\033[0m')        
    except TypeError:
        pass
        return('\33[31m' + f'Input type {type(i)} is not supported' + '\033[0m')

# ======== # Random Windows background color # ======== #
def windows_background(*user_input) -> str : 
    '''Change background color of output to 15 different colors. It use standard colors so it work in every terminal..'''
    try:
        # ====== # Opening json file that contain colors code in windows and linux # ====== #
        if name == 'nt':
            json_paths: str = __file__.replace('rcolor.py', 'colors\\Windows_background.json')
        else:    
            json_paths: str = __file__.replace('rcolor.py', 'colors/Windows_background.json')
        with open(json_paths, 'r') as f:
            Windows_background: list[str] = load(f).get("Windows_background")
        from colorama import just_fix_windows_console
        just_fix_windows_console()
        user_input = list(user_input)

        # ======== # make all item in user input_list to string # ======== #
        for i in user_input:
            if type(i) == str:
                pass
            else:
                user_input[user_input.index(i)] = str(i)

        user_input = ''.join(user_input)
        random_color: str = choice(Windows_background)
        return random_color + user_input + '\033[0m'
    except FileNotFoundError:
        pass
        return('\33[31m' + '"Windows_background.json" did not found.\nIt\'s may because the file was moved or deleted' + '\033[0m')        
    except TypeError:
        pass
        return('\33[31m' + f'Input type {type(i)} is not supported' + '\033[0m')

# ======== # Random style # ======== #
def style(*user_input) -> str:
    '''Change font of output to 3 different font.'''
    try:   
        # ====== # Opening json file that contain colors code in windows and linux # ====== #
        if name == 'nt':
            json_paths: str = __file__.replace('rcolor.py', 'colors\\style1.json')
        else:    
            json_paths: str = __file__.replace('rcolor.py', 'colors/style1.json')
        with open(json_paths, 'r') as f:
            style1: list[str] = load(f).get("style1")
        user_input = list(user_input)
        
        # ======== # make all item in user_input list to string # ======== #
        for i in user_input:
            if type(i) == str:
                pass
            else:
                user_input[user_input.index(i)] = str(i)

        user_input = ''.join(user_input)
        random_color: str = choice(style1)
        return random_color + user_input + '\033[0m'
    except FileNotFoundError:
        pass
        return('\33[31m' + '"style1.json" did not found.\nIt\'s may because the file was moved or deleted' + '\033[0m')        
    except TypeError:
        pass
        return('\33[31m' + f'Input type {type(i)} is not supported' + '\033[0m')
    
# ======== # change foreground for each character # ======== #
def chameleons_char(user_input: str | int) -> str: #type: ignore
    ''''''
    user_input: list[str] = list(str(user_input))
    Final_text: str = str()
    for i in enumerate(user_input):
        Final_text: str = Final_text + auto_color() + i + '\033[0m'
    return Final_text
    
    
# ======== # Automatically detects the operating system and return the correct color # ======== #
def auto_color(*user_input) -> str:
    '''Automatically detects the operating system and decide to use standard foreground(15 colors) or not standard foregrounds(255 colors)'''
    user_input = list(user_input)
    for i in user_input:
        if type(i) == str:
            pass
        else:
            user_input[user_input.index(i)] = str(i)

    user_input = ''.join(user_input)
    if name == 'nt':
        return windows_color(user_input)
    else:
        return color(user_input)

# ======== # Automatically detects the operating system and return the correct background color # ======== #
def auto_background(*user_input) -> str:
    '''Automatically detects the operating system and decide to use standard background colors(15 colors) or not standard background colors(255 colors)'''
    user_input = list(user_input)
    for i in user_input:
        if type(i) == str:
            pass
        else:
            user_input[user_input.index(i)] = str(i)

    user_input = ''.join(user_input)
    if name == 'nt':
        return windows_background(user_input)
    else:
        return background(user_input)

# ======== # return random color and background color # ======== #
def color_background(*user_input) -> str:
    '''Change foreground and background color of output randomly at the same time.'''
    user_input = list(user_input)
    for i in user_input:
        if type(i) == str:
            pass
        else:
            user_input[user_input.index(i)] = str(i)

    user_input = ''.join(user_input)
    return auto_color(auto_background(user_input))

# ======== # return random color and style # ======== #
def color_style(*user_input) -> str:
    '''Change foreground and font of output randomly at the same time.'''
    user_input = list(user_input)
    for i in user_input:
        if type(i) == str:
            pass
        else:
            user_input[user_input.index(i)] = str(i)

    user_input = ''.join(user_input)
    return auto_color(style(user_input))

# ======== # return random background color and style # ======== #
def background_style(*user_input) -> str:
    '''Change background color and font of output randomly at the same time.'''
    user_input = list(user_input)
    for i in user_input:
        if type(i) == str:
            pass
        else:
            user_input[user_input.index(i)] = str(i)

    user_input = ''.join(user_input)
    return auto_background(style(user_input))

# ======== # return random color and background color and style # ======== #
def color_background_style(*user_input) -> str:
    '''Change foreground, background color and font of output randomly at the same time.'''
    user_input = list(user_input)
    for i in user_input:
        if type(i) == str:
            pass
        else:
            user_input[user_input.index(i)] = str(i)

    user_input = ''.join(user_input)
    return auto_color(auto_background(style(user_input)))