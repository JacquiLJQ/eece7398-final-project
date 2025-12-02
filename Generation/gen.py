import random
import numpy as np


def generate_random_nets(num_nets, grid_size):
    nets = []
    for i in range(num_nets):
        nx = random.randint(0, grid_size - 1)
        ny = random.randint(0, grid_size - 1)
        nets.append({"name": f"N{i}", "position": (nx, ny)})
    return nets


def find_compatible_nets_for_device(device_x, device_y, nets):
    compatible = []
    for net in nets:
        nx, ny = net["position"]
        if abs(nx - device_x) <= 1 or abs(ny - device_y) <= 1:
            if abs(nx - device_x) + abs(ny - device_y) <= 5:
                if abs(nx - device_x) + abs(ny - device_y) >= 2:
                    compatible.append(net)
    return compatible


def create_device(device_type, index, grid_size):

    dx = random.randint(0, grid_size - 1)
    dy = random.randint(0, grid_size - 1)
    if device_type in ["Ground"]:
        t_count = 1
        dev_name = f"{device_type[0].upper()}{index}"
    elif device_type in [
        "Resistor",
        "Capacitor",
        "Inducer",
        "Diode",
        "Voltage",
        "Current",
    ]:
        t_count = 2
        dev_name = f"{device_type[0].upper()}{index}"  # R1, C2
    else:
        # PMOS/NMOS/NPN
        t_count = 3
        # prefix = "MP" if device_type == "PMOS" else "MN"
        dev_name = f"{device_type}{index}"

    if device_type == "PMOS":
        nodeType = f"pmos"
    elif device_type == "NMOS":
        nodeType = f"nmos"
    elif device_type == "NPN":
        nodeType = f"npn"
    elif device_type == "PNP":
        nodeType = f"pnp"
    elif device_type == "Inducer":
        nodeType = random.choice(
            ["american inductor", "cute inductor", "cute inductor", "cute inductor"]
        )
    elif device_type == "Diode":
        nodeType = f"D"
    elif device_type == "Resistor":
        nodeType = f"R"
    elif device_type == "Capacitor":
        nodeType = f"C"
    elif device_type == "Ground":
        nodeType = f"ground"
    elif device_type == "Voltage":
        nodeType = f"american voltage source"
    elif device_type == "Current":
        nodeType = f"american current source"
    else:
        nodeType = f"ERROR"

    return {
        "type": device_type,
        "name": dev_name,
        "position": (dx, dy),
        "terminal_count": t_count,
        "nodeType": nodeType,
    }


def assign_nets_to_device(device, nets, devices, max_retries=15):
    for _ in range(max_retries):
        dx, dy = device["position"]
        compatible_nets = find_compatible_nets_for_device(dx, dy, nets)
        if len(compatible_nets) >= device["terminal_count"]:
            chosen = random.sample(compatible_nets, k=device["terminal_count"])
            device["nets"] = [net["name"] for net in chosen]
            flag = False
            for dev in devices:
                if dev["position"] == device["position"]:
                    device["position"] = (
                        random.randint(0, grid_size - 1),
                        random.randint(0, grid_size - 1),
                    )
                    flag = True
                if (
                    abs(dev["position"][0] - device["position"][0]) <= 2
                    and abs(dev["position"][1] - device["position"][1]) <= 2
                ):
                    device["position"] = (
                        random.randint(0, grid_size - 1),
                        random.randint(0, grid_size - 1),
                    )
                    flag = True
            if flag:
                continue
            else:
                return device
        else:
            device["position"] = (
                random.randint(0, grid_size - 1),
                random.randint(0, grid_size - 1),
            )
    return None


def generate_random_circuit(
    num_nets=8,
    max_resistors=3,
    max_capacitors=3,
    max_pmos=3,
    max_nmos=3,
    max_npn=3,
    max_pnp=3,
    max_inducer=3,
    max_diode=3,
    max_ground=3,
    max_voltage=3,
    max_current=3,
    grid_size=5,
):
    nets = generate_random_nets(num_nets, grid_size)

    num_res = random.randint(1, max_resistors)
    num_cap = random.randint(1, max_capacitors)
    num_p = random.randint(1, max_pmos)
    num_n = random.randint(1, max_nmos)
    num_npn = random.randint(1, max_npn)
    num_pnp = random.randint(1, max_pnp)
    num_inducer = random.randint(1, max_inducer)
    num_diode = random.randint(1, max_diode)
    num_ground = random.randint(1, max_ground)
    num_voltage = random.randint(1, max_voltage)
    num_current = random.randint(1, max_current)
    devices = []
    dev_types = (
        ["Resistor"] * num_res
        + ["Capacitor"] * num_cap
        + ["PMOS"] * num_p
        + ["NMOS"] * num_n
        + ["NPN"] * num_npn
        + ["PNP"] * num_pnp
        + ["Inducer"] * num_inducer
        + ["Diode"] * num_diode
        + ["Ground"] * num_ground
        + ["Voltage"] * num_voltage
        + ["Current"] * num_current
    )
    random.shuffle(dev_types)
    counters = {
        "Resistor": 0,
        "Capacitor": 0,
        "PMOS": 0,
        "NMOS": 0,
        "NPN": 0,
        "PNP": 0,
        "Inducer": 0,
        "Diode": 0,
        "Ground": 0,
        "Voltage": 0,
        "Current": 0,
    }

    for dev_type in dev_types:
        counters[dev_type] += 1
        dev = create_device(dev_type, counters[dev_type], grid_size)
        dev_with_nets = assign_nets_to_device(dev, nets, devices)
        if dev_with_nets is not None:
            devices.append(dev_with_nets)
        else:
            pass

    return nets, devices


if __name__ == "__main__":
    import sys

    filename = sys.argv[1] + ".txt"
    grid_size = random.randint(5, 10)
    nets, devices = generate_random_circuit(
        num_nets=random.randint(40, 50),
        max_resistors=5,
        max_capacitors=5,
        max_pmos=10,
        max_nmos=10,
        max_npn=5,
        max_pnp=5,
        max_inducer=5,
        max_diode=5,
        max_ground=5,
        grid_size=grid_size,
    )
    shwoLines = random.choice([True, False])
    countN = {}
    for net in nets:
        # print(f"{net['name']} @ {net['position']}")
        countN[net["name"]] = 0

    for dev in devices:
        # print(f"{dev['name']:>4} ({dev['type']}) @ {dev['position']} -> {dev['nets']}")
        countN[dev["nets"][0]] += 1
        if dev["terminal_count"] >= 2:
            countN[dev["nets"][1]] += 1
        if dev["terminal_count"] >= 3:
            countN[dev["nets"][2]] += 1
    # lineW = random.randint(1, 3)
    lineW = random.choice([0.5, 0.6, 0.8, 1.0, 1.1, 1.2, 1.3, 1.5])
    print(
        r"""
    \documentclass{standalone}
    \usepackage{circuitikz}
    \usepackage{pgfmath}
    \usepackage{sansmath}
    \begin{document}
    \sansmath
    % 1. Prepare a file handle to write positions into """
        + filename
        + r"""
    \newwrite\posfile
    \immediate\openout\posfile="""
        + filename
        + r"""
          \begin{circuitikz}["""
        + f"line width={lineW-0.3}pt"
        + r"""]
    """
    )
    print(r"""\ctikzset{label/align = straight}""")
    mynet = {}
    for net in nets:
        mynet[net["name"]] = net
    if shwoLines:
        for net in nets:
            if countN[net["name"]] >= 3:
                #  \draw[fill=black] (5,2) circle (2pt);
                nx, ny = net["position"]
                size = lineW + random.randint(1, 2)
                print(f"\\draw[fill=black] ({nx},{ny}) circle (" + str(size) + "pt);")

    for dev in devices:
        dev_x, dev_y = dev["position"]
        rotate = random.choice([0, 90, 180, 270])
        x = random.choice([(1, 1), (1, 1.3), (1.3, 1), (1.5, 1.3), (1.3, 1.5)])
        xscale = x[0]
        yscale = x[1]
        xscale = xscale * random.choice([1, -1]) * lineW
        yscale = yscale * random.choice([1, -1]) * lineW
        if dev["terminal_count"] == 1:
            print(f"\\begin{{scope}}[local bounding box={dev['name']}BB]")
            # print(
            #     f"\\draw ({dev_x},{dev_y}) node[{dev['type'].lower()}, xscale={xscale}, yscale={yscale}]({dev['name']}){{}};"
            # )
            print(
                f"\\draw ({dev_x},{dev_y}) node[{dev['type'].lower()},xscale={xscale}, yscale={yscale},]({dev['name']}){{}};"
            )
            nx, ny = mynet[dev["nets"][0]]["position"]
            print(f"\\end{{scope}}")
            if shwoLines:
                print(f"\\draw ({dev['name']}.center) to ({nx},{ny});")

        if dev["terminal_count"] == 2:
            print(f"\\begin{{scope}}[local bounding box={dev['name']}BB]")
            direction = random.choice(["H", "V"])
            if direction == "H":
                p1x = dev_x + 1
                p1y = dev_y
                p2x = dev_x - 1
                p2y = dev_y
            else:
                p1x = dev_x
                p1y = dev_y + 1
                p2x = dev_x
                p2y = dev_y - 1
                # \draw (0,0)  to[R] (2,0);
            if dev["type"] == "Resistor":
                # print(r"\ctikzset{resistors/scale = " + str(xscale) + "}")
                # print(r"\ctikzset{resistors/width = " + str(yscale) + "}")
                print(
                    r"\ctikzset{resistors/zigs = " + str(random.choice([2, 3, 4])) + "}"
                )
                # if random.choice([0, 1]) == 0:
                if False:
                    print(
                        f"\\draw ({p1x},{p1y}) to[{dev['nodeType']},  l=$R_{random.choice([1,2,3,4,5,'A','B','C','a','b','c','d','D','s','S'])}$] ({p2x},{p2y});"
                    )
                else:
                    print(dev["nodeType"])
                    print(f"\\draw ({p1x},{p1y}) to[{dev['nodeType']}] ({p2x},{p2y});")
            elif dev["type"] == "Capacitor":
                # print(r"\ctikzset{capacitors/scale = " + str(xscale) + "}")
                # print(r"\ctikzset{capacitors/width = " + str(yscale) + "}")
                # print(
                #     r"\ctikzset{capacitors/coils = "
                #     + str(random.choice([3, 4, 5, 6]))
                #     + "}"
                # )
                pass
                # if random.choice([0, 1]) == 0:
                if False:
                    print(
                        f"\\draw ({p1x},{p1y}) to[{dev['nodeType']},  l=$C_{random.choice([1,2,3,4,5,'A','B','C','a','b','c'])}$] ({p2x},{p2y});"
                    )
                else:
                    print(f"\\draw ({p1x},{p1y}) to[{dev['nodeType']}] ({p2x},{p2y});")
            else:
                if dev["type"] == "Inducer":
                    # if random.choice([0, 1]) == 0:
                    if False:
                        print(
                            f"\\draw ({p1x},{p1y}) to[{dev['nodeType']},  l=$L_{random.choice([1,2,3,4,5,'A','B','C','a','b','c'])}$] ({p2x},{p2y});"
                        )
                    else:
                        print(
                            f"\\draw ({p1x},{p1y}) to[{dev['nodeType']}  ] ({p2x},{p2y});"
                        )
                elif dev["type"] == "Voltage":
                    # print(
                    #     f"\\draw ({p1x},{p1y}) to[{dev['nodeType']} ,l=$V_{random.choice([1,2,3,4,5,'A','B','C','a','b','c',r'{in}',r"{out}",r'{DD}'])}$ ] ({p2x},{p2y});"
                    # )
                    print(f"\\draw ({p1x},{p1y}) to[{dev['nodeType']} ] ({p2x},{p2y});")
                elif dev["type"] == "Current":
                    # print(
                    #     f"\\draw ({p1x},{p1y}) to[{dev['nodeType']} ,l=$I_{random.choice([1,2,3,4,5,'A','B','C','a','b','c',r'{in}',r"{out}"])}$ ] ({p2x},{p2y});"
                    # )
                    print(f"\\draw ({p1x},{p1y}) to[{dev['nodeType']} ] ({p2x},{p2y});")
                else:
                    # if random.choice([0, 1]) == 0:
                    if False:
                        print(
                            f"\\draw ({p1x},{p1y}) to[{dev['nodeType']},  l=$D_{random.choice([1,2,3,4,5,'A','B','C','a','b','c'])}$] ({p2x},{p2y});"
                        )
                    else:
                        print(
                            f"\\draw ({p1x},{p1y}) to[{dev['nodeType']}] ({p2x},{p2y});"
                        )
                # \draw (0,0)  to[R] (0,2);
            print(f"\\end{{scope}}")
            if shwoLines:
                nx, ny = mynet[dev["nets"][0]]["position"]
                print(f"\\draw ({p1x},{p1y}) to ({nx},{ny});")

                nx, ny = mynet[dev["nets"][1]]["position"]
                print(f"\\draw ({p2x},{p2y}) to ({nx},{ny});")

        if dev["terminal_count"] == 3:
            #  \draw (5,-5) node[pmos, rotate=0, xscale=-1,yscale=1](transistor){};
            print(f"\\begin{{scope}}[local bounding box={dev['name']}BB]")
            if dev["type"] == "PMOS" or dev["type"] == "NMOS":
                circle = random.choice([0, 1, 2])
                if circle == 0:
                    CIRCLE = ""
                if circle == 1:
                    CIRCLE = "emptycircle"
                if circle == 2:
                    CIRCLE = "nocircle"
                bulk = random.choice([0, 1])
                if bulk == 0:
                    BULK = ""
                if bulk == 1:
                    BULK = "bulk"
                print(
                    f"\\draw ({dev_x},{dev_y}) node[{dev['type'].lower()},{BULK}, rotate={rotate}, xscale={xscale}, yscale={yscale},{CIRCLE},arrowmos]({dev['name']}){{}};"
                )

                # $M_{random.choice([1,2,3,4,5])}$
                #  \node[above] at (111) {M1};
            else:
                print(
                    f"\\draw ({dev_x},{dev_y}) node[{dev['type'].lower()}, rotate={rotate}, xscale={xscale}, yscale={yscale}]({dev['name']}){{}};"
                )
            print(f"\\end{{scope}}")
            # if dev["type"] == "PMOS" or dev["type"] == "NMOS":
            # kind = random.choice([0, 1, 2, 3, 4])
            kind = 4
            if kind == 0:
                print(
                    f"\\node[left, xshift=-13pt] at({dev['name']}BB) {{$M_{random.choice([1,2,3,4,5])}$}};"
                )
            if kind == 1:
                print(
                    f"\\node[above, yshift=13pt] at({dev['name']}BB) {{$M_{random.choice([1,2,3,4,5])}$}};"
                )
            if kind == 2:
                print(
                    f"\\node[right, xshift=13pt] at({dev['name']}BB) {{$M_{random.choice([1,2,3,4,5])}$}};"
                )
            if kind == 3:
                print(
                    f"\\node[below, yshift=-13pt] at({dev['name']}BB) {{$M_{random.choice([1,2,3,4,5])}$}};"
                )
            if kind == 4:
                pass
            if shwoLines:
                nx, ny = mynet[dev["nets"][0]]["position"]
                print(f"\\draw ({dev['name']}.S) to ({nx},{ny});")

                nx, ny = mynet[dev["nets"][1]]["position"]
                print(f"\\draw ({dev['name']}.D) to ({nx},{ny});")

                nx, ny = mynet[dev["nets"][2]]["position"]
                print(f"\\draw ({dev['name']}.G) to ({nx},{ny});")
    #      \path (R1BB.south west); \pgfgetlastxy{\rOneMinX}{\rOneMinY}
    #   \path (R1BB.north east); \pgfgetlastxy{\rOneMaxX}{\rOneMaxY}
    for dev in devices:
        # print(f"\\path ({dev['name']}BB.south west); \\pgfgetlastxy{{\\{dev['name']}MinX}}{{\\{dev['name']}MinY}}")
        # print(f"\\path ({dev['name']}BB.north east); \\pgfgetlastxy{{\\{dev['name']}MaxX}}{{\\{dev['name']}MaxY}}")
        print(
            f"\\path ({dev['name']}BB.south west);"
            + r" \pgfgetlastxy{\rOneMinX}{\rOneMinY}"
        )
        print(
            f"\\path ({dev['name']}BB.north east);"
            + r" \pgfgetlastxy{\rOneMaxX}{\rOneMaxY}"
        )
        print(
            r"""
   \pgfpointanchor{current bounding box}{north west} \pgfgetlastxy{\pgNWx}{\pgNWy}
   \newdimen\canvaswidth
   \newdimen\canvasheight
   \path (current bounding box.south west); \pgfgetlastxy{\canvasminx}{\canvasminy}
   \path (current bounding box.north east); \pgfgetlastxy{\canvasmaxx}{\canvasmaxy}
   \pgfmathsetlength{\canvaswidth}{\canvasmaxx-\canvasminx}
   \pgfmathsetlength{\canvasheight}{\canvasmaxy-\canvasminy}
   \pgfmathsetmacro{\widthratio}{(\rOneMaxX-\rOneMinX)/(\canvaswidth)}
   \pgfmathsetmacro{\heightratio}{(\rOneMaxY-\rOneMinY)/(\canvasheight)}
   \pgfmathsetmacro{\xpositionratio}{(\rOneMinX+\rOneMaxX-\canvasminx-\canvasminx)/2/(\canvaswidth)}
   \pgfmathsetmacro{\ypositionratio}{1-(\rOneMinY+\rOneMaxY-\canvasminy-\canvasminy)/2/(\canvasheight)}
"""
        )

        #   \immediate\write\posfile{0 \xpositionratio \space \ypositionratio \space \widthratio \space \heightratio }
        myClass = 0
        if dev["type"] == "PMOS":
            myClass = "0"
        elif dev["type"] == "NMOS":
            myClass = "1"
        elif dev["type"] == "NPN":
            myClass = "2"
        elif dev["type"] == "PNP":
            myClass = "3"
        elif dev["type"] == "Inducer":
            myClass = "4"
        elif dev["type"] == "Diode":
            myClass = "5"
        elif dev["type"] == "Resistor":
            myClass = "6"
        elif dev["type"] == "Capacitor":
            myClass = "7"
        elif dev["type"] == "Ground":
            myClass = "8"
        elif dev["type"] == "Voltage":
            myClass = "9"
        elif dev["type"] == "Current":
            myClass = "10"
        else:
            myClass = "ERROR"

        print(
            r" \immediate\write\posfile{"
            + myClass
            + r"\space \xpositionratio \space \ypositionratio \space \widthratio \space \heightratio }"
        )

#     # === NEW: Add random text labels on schematic ===
#     text_labels = [
#         "VDD",
#         "Vout",
#         "Vin",
#         "node1",
#         "Ibias",
#         "GND",
#         "Vref",
#         "CLK",
#         "out",
#         "bias",
#     ]
#     num_labels = random.randint(3, 8)  # 控制文字数量

#     # 记录每个文字对应的局部 bounding box用于写入 YOLO 标签
#     text_boxes = []

#     for t_idx in range(num_labels):
#         lx = random.uniform(0, grid_size)  # 随机 X 坐标
#         ly = random.uniform(-grid_size / 2, grid_size / 2)  # 随机 Y 坐标
#         label = random.choice(text_labels)
#         rot = random.choice([-20, -10, 0, 10, 20])
#         color = random.choice(["gray", "blue!40", "red!60", "black"])
#         font_size = random.choice(
#             ["\\tiny", "\\scriptsize", "\\footnotesize", "\\small"]
#         )

#         # 为这个文字生成一个局部 bounding box 名字，例如 TXT0, TXT1...
#         box_name = f"TXT{t_idx}"
#         text_boxes.append(box_name)

#         # local bounding box=<box_name> 让 TikZ 为这个文字记录一个 bbox
#         print(
#             f"\\node[{color}, rotate={rot}, local bounding box={box_name}] "
#             f"at ({lx:.2f},{ly:.2f}) {{{font_size} {label}}};"
#         )

#     TEXT_CLASS_ID = "11"  # 新增11号类别text

#     for box_name in text_boxes:
#         # 这里给文字添加坐标的方式和器件是一样的
#         print(
#             f"\\path ({box_name}.south west);"
#             + r" \pgfgetlastxy{\rOneMinX}{\rOneMinY}"
#         )
#         print(
#             f"\\path ({box_name}.north east);"
#             + r" \pgfgetlastxy{\rOneMaxX}{\rOneMaxY}"
#         )

#         print(
#             r"""
#    \pgfpointanchor{current bounding box}{north west} \pgfgetlastxy{\pgNWx}{\pgNWy}
#    \newdimen\canvaswidth
#    \newdimen\canvasheight
#    \path (current bounding box.south west); \pgfgetlastxy{\canvasminx}{\canvasminy}
#    \path (current bounding box.north east); \pgfgetlastxy{\canvasmaxx}{\canvasmaxy}
#    \pgfmathsetlength{\canvaswidth}{\canvasmaxx-\canvasminx}
#    \pgfmathsetlength{\canvasheight}{\canvasmaxy-\canvasminy}
#    \pgfmathsetmacro{\widthratio}{(\rOneMaxX-\rOneMinX)/(\canvaswidth)}
#    \pgfmathsetmacro{\heightratio}{(\rOneMaxY-\rOneMinY)/(\canvasheight)}
#    \pgfmathsetmacro{\xpositionratio}{(\rOneMinX+\rOneMaxX-\canvasminx-\canvasminx)/2/(\canvaswidth)}
#    \pgfmathsetmacro{\ypositionratio}{1-(\rOneMinY+\rOneMaxY-\canvasminy-\canvasminy)/2/(\canvasheight)}
# """
#         )

#         # 3. 写一行 YOLO 标签： 11 x y w h
#         print(
#             r" \immediate\write\posfile{"
#             + TEXT_CLASS_ID
#             + r"\space \xpositionratio \space \ypositionratio \space \widthratio \space \heightratio }"
#         )



print(
    r"""


 \end{circuitikz}

% 6. Close the file

\immediate\closeout\posfile

\end{document}     """
)
