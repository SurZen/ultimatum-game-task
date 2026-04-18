"""
Lightweight PsychoPy stub for headless smoke tests.
This provides minimal `visual`, `core`, `event`, and `gui` APIs
used by `run_ugt.py` so the script can run without PsychoPy.
"""
import time
from types import SimpleNamespace

# visual
class Window:
    def __init__(self, *args, **kwargs):
        self._closed = False
    def flip(self):
        pass
    def close(self):
        self._closed = True

class TextStim:
    def __init__(self, win, text="", height=0.06, color=None, wrapWidth=None, pos=(0,0)):
        self.text = text
        self.height = height
        self.color = color
        self.wrapWidth = wrapWidth
        self.pos = tuple(pos)
    def draw(self):
        # for headless testing, print the text to console (include pos)
        print(f"[TEXT] {self.text} (pos={self.pos})")

class ImageStim:
    def __init__(self, win, image=None, size=None, pos=(0,0)):
        self.image = str(image) if image is not None else ""
        self.size = size
        self.pos = tuple(pos)
    def draw(self):
        print(f"[IMAGE] {self.image} (size={self.size}, pos={self.pos})")

visual = SimpleNamespace(Window=Window, TextStim=TextStim, ImageStim=ImageStim)

# core
class Clock:
    def __init__(self):
        self._start = time.time()
    def getTime(self):
        return time.time() - self._start
    def reset(self):
        self._start = time.time()

def wait(seconds: float):
    time.sleep(seconds)

def quit():
    raise SystemExit()

core = SimpleNamespace(Clock=Clock, wait=wait, quit=quit)

# event
def clearEvents():
    return None

def getKeys(keyList=None):
    # Always return no keys for getKeys checks (no quit pressed)
    return []

def waitKeys(maxWait=None, keyList=None, timeStamped=False):
    # Choose a default non-quit key for advancing
    key = None
    if keyList:
        # Prefer an 'accept' key if present (common default 'a'), else the first non-quit
        for k in keyList:
            if k and k.lower() not in ("escape", "esc"):
                key = k
                break
        if key is None:
            key = keyList[0]
    else:
        key = "a"

    rt = 0.1
    if timeStamped:
        return [(key, rt)]
    return [key]

event = SimpleNamespace(clearEvents=clearEvents, getKeys=getKeys, waitKeys=waitKeys)

# gui
class Dlg:
    def __init__(self, dictionary=None, title=None, order=None):
        self.dictionary = dictionary or {}
        self.title = title
        self.order = order
        self.OK = True

def DlgFromDict(dictionary=None, title=None, order=None):
    # Simulate a dialog that the user accepted (OK)
    print(f"[GUI] DlgFromDict called with: {dictionary}")
    return Dlg(dictionary, title=title, order=order)

gui = SimpleNamespace(DlgFromDict=DlgFromDict)
