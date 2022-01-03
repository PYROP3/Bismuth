import os

def generate_bots():
    with open("bots.py", "w") as f:
        f.write("available_bots = [\n")
        for path in os.listdir("./bots"):
            if not os.path.isdir(f"./bots/{path}"):
                continue
            pyfiles = [file for file in os.listdir(f"./bots/{path}") if file[-3:] == ".py"]
            if len(pyfiles) == 1:
                f.write("    ('{}','{}','{}'),\n".format(pyfiles[0][:-3], path, pyfiles[0]))
        f.write("]")

if __name__ == "__main__":
    generate_bots()