import tkinter as tk


def draw_state(state):
    root = tk.Tk()

    i = 0
    j = 0
    for x in state["graph"]:
        for y in x:
            if y == -1:
                tk.Label(root, text=y, borderwidth=32, bg="blue").grid(row=j, column=i)
            elif y == -2:
                tk.Label(root, text=y, borderwidth=32, bg="red").grid(row=j, column=i)
            else:
                tk.Label(root, text=y, borderwidth=32).grid(row=j, column=i)
            i += 1
        i = 0
        j += 1

    root.lift()
    root.mainloop()


def draw_route(state, color="yellow"):
    root = tk.Tk()

    i = 0
    j = 0
    for x in state["graph"]:
        for y in x:
            if y == -1:
                tk.Label(root, text=y, borderwidth=32, bg="blue").grid(row=j, column=i)
            elif y == -2:
                tk.Label(root, text=y, borderwidth=32, bg="red").grid(row=j, column=i)
            else:
                tk.Label(root, text=y, borderwidth=32).grid(row=j, column=i)
            i += 1
        i = 0
        j += 1

    for action in state["path"]:
        tk.Label(
            root, text=state["graph"][action[0], action[1]], borderwidth=32, bg=color
        ).grid(row=action[0], column=action[1])

    root.lift()
    root.mainloop()
