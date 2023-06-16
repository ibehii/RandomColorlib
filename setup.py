# Github: https://github.com/beh185
# Telegram: https://T.me/dr_xz
# e-mail: BehnamH.dev@gmail.com
# ____________________________________________
def windows_installer():
    # import part
    import os
    import shutil
    # getting python modules's path
    module_path = os.__file__
    os.system('pip install colorama')
    os.system('cls')
    
    module_path = module_path.replace('\os.py', '')
    print('Your modules are in : ', module_path)

    # getting permission to copy Randomcolorlib to modules folder
    copy_permission = input(
        'Do you want to add RandomColorlib to your modules[y/n]? (please open Terminal as administrator for this operation) -> '
        )
    if (copy_permission.lower() == 'yes' or copy_permission.lower() == 'y'):
        shutil.copy( module_path, 'Rcolor.py')
        print("It's done !")
    else:
        print('Copying failed.')

def linux_installer():

    # import part
    import os

    # getting python modules's path
    module_path = os.__file__
    module_path = module_path.replace('/os.py', '')

    print('Your modules are in : ', module_path)

    # getting permission to copy Randomcolorlib to modules folder
    copy_permission = input(
        'Do you want to add RandomColorlib to your modules? [Root access required] -> '
        )
    if (copy_permission.lower() == 'yes' or copy_permission.lower() == 'y'):
        os.system(f'sudo cp -r Rcolor.py {module_path}')
        print("It's done !")
    else:
        print('Copying failed.')
    
def installer():
    # get operating system name
    from os import name
    os_name = name
    if os_name == 'nt':
        windows_installer()
    else:
        linux_installer()

if __name__ == '__main__':
    installer()
