#Author-volesen
#Description-Generates a superellipse

import adsk.core, adsk.fusion, adsk.cam, traceback, math

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        ui.messageBox('Generating superellipse')

        sketch = create_new_sketch(app)
        generate_curve_in_sketch(sketch)
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


# Fusion

def create_new_sketch(app):
    design = app.activeProduct

    # Get the root component of the active design.
    rootComp = design.rootComponent

    # Create a new sketch on the xy plane.
    sketches = rootComp.sketches
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)

    return sketch

def generate_curve_in_sketch(sketch):
    # Create an object collection for the points.
    points = adsk.core.ObjectCollection.create()

    t_start = 0
    t_end = 2 * math.pi

    num_points = 100
    for i in range(num_points):
        t = t_start + (t_end - t_start) * i / (num_points - 1)

        x, y = parametric_superellipse(t)

        points.add(adsk.core.Point3D.create(x, y, 0))
    
    sketch.sketchCurves.sketchFittedSplines.add(points)
