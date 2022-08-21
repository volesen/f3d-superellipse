#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback, math

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        ui.messageBox('Hello script')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# Math

def sgn(x: float) -> float:
    return 1 if x > 0 else -1

def parametric_superellipse(t, a=1, b=1, n=2.5):
    """
    Parametric equation for a superellipse
    """

    x = a * sgn(math.cos(t)) * abs(math.cos(t)) ** (2 / n)
    y = b * sgn(math.sin(t)) * abs(math.sin(t)) ** (2 / n)

    return (x, y)

