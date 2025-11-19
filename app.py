from flask import Flask, render_template, request
import math

app = Flask(__name__)

# initial rectangle state
state = {
    "top": 120,
    "left": 170,
    "angle": 0,       # rotation in degrees
    "length": 90,     # front-to-back
    "width": 60       # side-to-side
}

MOVE_STEP = 10
ROTATE_STEP = 15
CONTAINER_WIDTH = 400
CONTAINER_HEIGHT = 300

@app.route("/", methods=["GET", "POST"])
def index():
    global state

    if request.method == "POST":
        action = request.form.get("move")

        if action == "rotate":
            state["angle"] = (state["angle"] + ROTATE_STEP) % 360

        elif action in ["forward", "reverse"]:
            rad = math.radians(state["angle"])
            dx = MOVE_STEP * math.cos(rad)
            dy = MOVE_STEP * math.sin(rad)

            if action == "forward":
                state["left"] += dx
                state["top"] += dy
            else:  # reverse
                state["left"] -= dx
                state["top"] -= dy

        elif action == "resize":
            try:
                # Read values from form
                state["length"] = max(1, int(request.form.get("length", state["length"])))
                state["width"] = max(1, int(request.form.get("width", state["width"])))
            except:
                pass

        # clamp inside container based on new dimensions
        state["top"] = max(0, min(CONTAINER_HEIGHT - state["width"], state["top"]))
        state["left"] = max(0, min(CONTAINER_WIDTH - state["length"], state["left"]))

    return render_template("index.html", pos=state)

if __name__ == "__main__":
    app.run(debug=True)
