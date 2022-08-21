# Author-volesen
# Description-Generates a superellipse

import adsk.core, adsk.fusion, adsk.cam, traceback, math

# Global list to keep all event handlers in scope.
# This is only needed with Python.
handlers = []


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        # Get the CommandDefinitions collection.
        cmdDefs = ui.commandDefinitions

        # Create a button command definition.
        cmdDef = cmdDefs.addButtonDefinition(
            "GenerateSuperellipse", "Generate Superellipse", "Generate a superellipse"
        )

        # Connect to the command created event.
        onCommandCreated = SuperellipseCommandCreatedEventHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)

        # Execute the command.
        cmdDef.execute()

        # Keep the script running.
        adsk.autoTerminate(False)

    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))


# Event handler for the commandCreated event.
class SuperellipseCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)

        # Get the command
        cmd = eventArgs.command

        # Get the CommandInputs collection to create new command inputs.
        inputs = cmd.commandInputs

        app = adsk.core.Application.get()
        design = adsk.fusion.Design.cast(app.activeProduct)

        width = inputs.addValueInput(
            "width",
            "Width",
            design.unitsManager.defaultLengthUnits,
            adsk.core.ValueInput.createByReal(1.0),
        )

        height = inputs.addValueInput(
            "height",
            "Height",
            design.unitsManager.defaultLengthUnits,
            adsk.core.ValueInput.createByReal(1.0),
        )

        exponent = inputs.addValueInput(
            "exponent", "Exponent", "", adsk.core.ValueInput.createByReal(2.5)
        )

        points = inputs.addIntegerSpinnerCommandInput(
            "points", "Number of points", 1, 1000, 1, 100
        )

        # Connect to the execute event.
        onExecute = SuperellipseCommandExecuteHandler()
        cmd.execute.add(onExecute)
        handlers.append(onExecute)


# Event handler for the execute event.
class SuperellipseCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        # Verify that a sketch is active.
        app = adsk.core.Application.get()
        if app.activeEditObject.objectType != adsk.fusion.Sketch.classType():
            ui = app.userInterface
            ui.messageBox("A sketch must be active for this command.")
            return False

        eventArgs = adsk.core.CommandEventArgs.cast(args)

        inputs = eventArgs.command.commandInputs

        width = inputs.itemById("width").value
        height = inputs.itemById("height").value
        exponent = inputs.itemById("exponent").value
        points = inputs.itemById("points").value

        sketch = adsk.fusion.Sketch.cast(app.activeEditObject)
        draw_superellipse(sketch, width, height, exponent, points)

        # Force the termination of the command.
        adsk.terminate()


def draw_superellipse(sketch, width, height, exponent, num_points):
    sketch.isComputeDeferred = True

    points = adsk.core.ObjectCollection.create()

    t_start = 0
    t_end = 2 * math.pi

    for i in range(num_points):
        t = t_start + (t_end - t_start) * i / (num_points - 1)

        x, y = parametric_superellipse(t, width / 2, height / 2, exponent, exponent)

        points.add(adsk.core.Point3D.create(x, y, 0))

    sketch.sketchCurves.sketchFittedSplines.add(points)
    sketch.isComputeDeferred = False


def stop(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Delete the command definition.
        cmdDef = ui.commandDefinitions.itemById("GenerateSuperellipse")
        if cmdDef:
            cmdDef.deleteMe()
    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))


# Math


def sgn(x):
    return 1 if x > 0 else -1


def parametric_superellipse(t, a, b, n, m):
    """
    Parametric equation for a superellipse
    """

    x = a * sgn(math.cos(t)) * abs(math.cos(t)) ** (2 / n)
    y = b * sgn(math.sin(t)) * abs(math.sin(t)) ** (2 / m)

    return (x, y)
