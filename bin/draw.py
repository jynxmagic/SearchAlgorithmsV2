import tkinter as tk


def draw_state(state, with_actions=False, color="Yellow", title="Problem"):
    """Draws any state to the screen, with or without route.

    Args:
        state ([dict]): ["graph"]: integer matrix, ["path"]: path robot has taken, ["encoded_state"]: robot_x robot_y target_x target_y
        with_actions ([boolean]): whether to also draw the "path" - added as a 2d array to the state dict.
        color ([String]): Colour to draw the path
        title ([String]): Title of the tkinter window
    """
    root = tk.Tk()
    root.title(title)

    i = 0
    j = 0
    for x in state["graph"]:
        for y in x:
            if y == -1:  # robot
                tk.Label(root, text=y, borderwidth=15, bg="blue").grid(row=j, column=i)
            elif y == -2:  # target
                tk.Label(root, text=y, borderwidth=15, bg="green").grid(row=j, column=i)
            elif y == -3:  # immoveable cells
                tk.Label(root, text=y, borderwidth=15, bg="red").grid(row=j, column=i)
            else:
                tk.Label(root, text=y, borderwidth=15).grid(row=j, column=i)
            i += 1
        i = 0
        j += 1

    if with_actions:
        for action in state["path"]:
            tk.Label(
                root,
                text=state["graph"][action[0], action[1]],
                borderwidth=32,
                bg=color,
            ).grid(row=action[0], column=action[1])

    root.lift()
    root.attributes("-topmost", True)
    root.mainloop()
