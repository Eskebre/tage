from tage import Tage

try:
    from colorama import just_fix_windows_console
    just_fix_windows_console()
except:
    print("In the case colored text or ansi codes don't work properly, install the colorama python module. \'python -m pip install colorama\'")

tage = Tage()

tage.scriptLoad("init.tage")
tage.scriptOpen("init.tage")

while tage.step():
    #print(tage.stack)
    pass

