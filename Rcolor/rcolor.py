# Github: https://github.com/ibehii
# Telegram: https://T.me/dr_xz
# e-mail: Behii@tutanota.com
# ____________________________________________

# ======== # import built-in library # ======== #
from random import choice
from os import name
from json import load
from pathlib import Path

# ======== # random foreground color# ======== #
colors_path: Path = Path(__file__).parent.resolve() / "colors"

# ======== # random foreground color# ======== #
def foreground(*user_input) -> str:
    '''Change foreground color of output to 255 different colors, but it may not work in every terminal.'''
    try:
        # ====== # Opening json file that contain colors code in windows and unix # ====== #
        foreground_colors_paths: Path = colors_path / 'foreground.json'
        
        with open(foreground_colors_paths , 'r') as f:
            foreground_colors: list[str] = load(f).get("colors")
        user_input = list(user_input)

        # ======== # make all item in user_input list to string  # ======== #
        for i in user_input:
            if type(i) is str:
                pass
            else:
                user_input[user_input.index(i)] = str(i)

        user_input = ''.join(user_input)
        random_color: str = choice(foreground_colors)

        return random_color + user_input + '\033[0m'
    except FileNotFoundError:
        pass
        return('\33[31m' + '"foreground.json" did not found.\nIt\'s may because the file was moved or deleted' + '\033[0m')    
    except TypeError:
        pass
        return('\33[31m' + f'Input type {type(i)} is not supported' + '\033[0m')

# ======== # random background color # ======== #
def background(*user_input) -> str:
    '''Change background color of output to 255 different colors, but it may not work in every terminal.'''
    try:
        # ====== # Opening json file that contain colors code in windows and unix # ====== #
        background_colors_paths: Path = colors_path / 'background_colors.json'
            
        with open(background_colors_paths, 'r') as f:
            background_colors: list[str] = load(f).get("background_color")
        user_input = list(user_input)

        # ======== # make all item in user_input list to string # ======== #
        for i in user_input:
            if type(i) is str:
                pass
            else:
                user_input[user_input.index(i)] = str(i)

        user_input = ''.join(user_input)
        random_color: str = choice(background_colors)
        return random_color + user_input + '\033[0m'
    except FileNotFoundError:
        pass
        return('\33[31m' + '"background_colors.json" did not found.\nIt\'s may because the file was moved or deleted' + '\033[0m')   
    except TypeError:
        pass
        return('\33[31m' + f'Input type {type(i)} is not supported' + '\033[0m')

# ======== # Random foreground color using standard colors # ======== #
def standard_fg(*user_input) -> str:
    '''Change foreground of output to 15 different colors. It use standard colors so it work in every terminal.'''
    try:
        # ====== # Opening json file that contain colors code in windows and unix # ====== #
        standard_colors_paths: Path = colors_path / 'standard_colors.json'
        
        with open(standard_colors_paths, 'r') as f:
            standard_color: list[str] = load(f).get("standard_foreground_colors")
        user_input = list(user_input)

        # ======== # make all item in user_input list to string # ======== #
        for i in user_input:
            if type(i) is str:
                pass
            else:
                user_input[user_input.index(i)] = str(i)
        from colorama import just_fix_windows_console
        just_fix_windows_console()
        user_input = ''.join(user_input)
        random_color: str = choice(standard_color)
        
        return random_color + user_input + '\033[0m'
    
    except FileNotFoundError:
        pass
        return('\33[31m' + '"standard_colors.json" did not found.\nIt\'s may because the file was moved or deleted' + '\033[0m')
    except TypeError:
        pass
        return('\33[31m' + f'Input type {type(i)} is not supported' + '\033[0m')

# ======== # Random background color using standard color # ======== #
def standard_bg(*user_input) -> str :
    '''Change background color of output to 15 different colors. It use standard colors so it work in every terminal..'''
    try:
        # ====== # Opening json file that contain colors code in windows and linux # ====== #
        standard_background_colors_paths: Path = colors_path / 'standard_background.json'
    
        with open(standard_background_colors_paths, 'r') as f:
            standard_background: list[str] = load(f).get("standard_background")
            
        from colorama import just_fix_windows_console
        just_fix_windows_console()
        user_input = list(user_input)

        # ======== # make all item in user input_list to string # ======== #
        for i in user_input:
            if type(i) is str:
                pass
            else:
                user_input[user_input.index(i)] = str(i)

        user_input = ''.join(user_input)
        random_color: str = choice(standard_background)
        
        return random_color + user_input + '\033[0m'
    except FileNotFoundError:
        pass
        return('\33[31m' + '"standard_background.json" did not found.\nIt\'s may because the file was moved or deleted' + '\033[0m')        
    except TypeError:
        pass
        return('\33[31m' + f'Input type {type(i)} is not supported' + '\033[0m')

# ======== # Random style # ======== #
def style(*user_input) -> str:
    '''Change font of output to 3 different font.'''
    try:
        # ====== # Opening json file that contain colors code in windows and linux # ====== #

        style1_colors_paths: Path = colors_path / 'style1.json'
    
        with open(style1_colors_paths, 'r') as f:
            style1: list[str] = load(f).get("style1")
        user_input = list(user_input)

        # ======== # make all item in user_input list to string # ======== #
        for i in user_input:
            if type(i) is str:
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

# ======== # change foreground color for each character # ======== #
def rainbow_fg(user_input: str | int) -> str: #type: ignore
    '''It changes foreground color of every character in the text randomly to 255 different color, but it may not work in every terminal.'''
    user_input: str = str(user_input)
    Final_text: str = str()
    for i in (user_input):
        Final_text: str = Final_text + foreground(i)
    return Final_text

# ======== # to change foreground color for each character using standard colors # ======== #
def standard_rainbow_fg(user_input: str | int) -> str: #type: ignore
    '''It changes foreground color of every character in the text randomly to 15 different color.'''
    user_input: str = str(user_input)
    Final_text: str = str()
    for i in (user_input):
        Final_text: str = Final_text + standard_fg(i)
    return Final_text


# ======== # Automatically detects the operating system and return the correct color # ======== #
def auto_fg(*user_input) -> str:
    '''Automatically detects the operating system and decide to use standard foreground(15 colors) or not standard foregrounds(255 colors)'''
    user_input = list(user_input)
    for i in user_input:
        if type(i) is str:
            pass
        else:
            user_input[user_input.index(i)] = str(i)

    user_input = ''.join(user_input)
    if name == 'nt':
        return standard_fg(user_input)
    else:
        return foreground(user_input)

# ======== # Automatically detects the operating system and return the correct background color # ======== #
def auto_bg(*user_input) -> str:
    '''Automatically detects the operating system and decide to use standard background colors(15 colors) or not standard background colors(255 colors)'''
    user_input = list(user_input)
    for i in user_input:
        if type(i) is str:
            pass
        else:
            user_input[user_input.index(i)] = str(i)

    user_input = ''.join(user_input)
    if name == 'nt':
        return standard_bg(user_input)
    else:
        return background(user_input)

# ======== # return random color and background color # ======== #
def foreground_background(*user_input) -> str:
    '''Change foreground and background color of output randomly at the same time.'''
    user_input = list(user_input)
    for i in user_input:
        if type(i) is str:
            pass
        else:
            user_input[user_input.index(i)] = str(i)

    user_input = ''.join(user_input)
    return auto_fg(auto_bg(user_input))

# ======== # return random color and style # ======== #
def foreground_style(*user_input) -> str:
    '''Change foreground and font of output randomly at the same time.'''
    user_input = list(user_input)
    for i in user_input:
        if type(i) is str:
            pass
        else:
            user_input[user_input.index(i)] = str(i)

    user_input = ''.join(user_input)
    return auto_fg(style(user_input))

# ======== # return random background color and style # ======== #
def background_style(*user_input) -> str:
    '''Change background color and font of output randomly at the same time.'''
    user_input = list(user_input)
    for i in user_input:
        if type(i) is str:
            pass
        else:
            user_input[user_input.index(i)] = str(i)

    user_input = ''.join(user_input)
    return auto_bg(style(user_input))

# ======== # return random color and background color and style # ======== #
def foreground_background_style(*user_input) -> str:
    '''Change foreground, background color and font of output randomly at the same time.'''
    user_input = list(user_input)
    for i in user_input:
        if type(i) is str:
            pass
        else:
            user_input[user_input.index(i)] = str(i)

    user_input = ''.join(user_input)
    return auto_fg(auto_bg(style(user_input)))