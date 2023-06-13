# Github: https://github.com/beh185
# Telegram: https://T.me/dr_xz
# e-mail: BehnamH.dev@gmail.com
# ____________________________________________

# import part
import os
import shutil

# get operating system name
os_name = os.name

# get modules of python path
module_path = os.__file__

if os_name == 'nt':
    module_path = module_path.replace('\os.py', '')
    print('Your modules are in : ', module_path)

    # get permission to copy randomcolorlib to modules folder
    copy_permision = input(
        'Do you want to add RandomColorlib to your modules? [please open Terminal as administrator for this operation] -> '
        )
    if (copy_permision.lower() == 'yes' or copy_permision.lower() == 'y'):
        shutil.copy( module_path, 'Rcolor.py')
        print("It's done !")
    else:
        print('Copying failed.')



else:
    module_path = module_path.replace('/os.py', '')
    print('Your modules are in : ', module_path)

    # get permission to copy randomcolorlib to modules folder
    copy_permision = input(
        'Do you want to add RandomColorlib to your modules? [sudo access required] -> '
        )
    if (copy_permision.lower() == 'yes' or copy_permision.lower() == 'y'):
        os.system(f'sudo cp -r Rcolor.py {module_path}')
        print("It's done !")
    else:
        print('Copying failed.')
