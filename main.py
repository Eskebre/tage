from tage.tage import Tage

try:
    from colorama import just_fix_windows_console
    just_fix_windows_console()
except:
    pass

tage = Tage()

tage.scriptLoad(tage, "init.tage")
tage.executeCommand(f'open init.tage')

while tage.step():
    #print(tage.stack)
    pass

