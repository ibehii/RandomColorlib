# Github: https://github.com/beh185
# Telegram: https://T.me/dr_xz
# e-mail: BehnamH.dev@gmail.com
# ____________________________________________

import os
import shutil
name = os.name
ospath = os.__file__
ospath = ospath.replace('/os.py', '')
print('Your modules are in : ', ospath)
if name == 'posix' : 
    COPY = input('Do you want to copy RandomColorlib to there? [We will need sudo access] ')
    if(COPY == 'Yes' or COPY == 'yes' or COPY == 'YES'):
        os.system(f'sudo cp -r Rcolor.py {ospath}')
        print("It's done !")
    else:
        print('Copying failed.')



else:
    COPY= input('Do you want to copy RandomColorlib to there? [please open Terminal as administrator for this operation] ')
    if( COPY == 'Yes' or COPY == 'yes' or COPY == 'YES' ):
        shutil.copy('Rcolor.py', ospath)
        print("It's done !")
    else:
        print('Copying failed.')



