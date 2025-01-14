from tage.tage import Tage

try:
    from colorama import just_fix_windows_console
    just_fix_windows_console()
except:
    pass

tage = Tage()
script = "init.tage"

tage.scriptLoad(tage, script)
tage.executeCommand(f'open {script}')

while tage.step():
    #print(tage.stack)
    pass

