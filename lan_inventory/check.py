#!/usr/bin/env python3
"""Self-check for the project "LAN Inventory" (u04).

Run it in the project directory:

    python3 check.py

The script reads only the files your program produced. It never runs
your program, so generate the files first, then check them. Each
[fail] line names one requirement; fix it and run the script again.
"""

import csv
import html as html_lib
import os
import re
import sys


class Fail(Exception):
    pass


CHECKS = []
WARNINGS = []


def check(name):
    def register(function):
        CHECKS.append((name, function))
        return function
    return register


def warn(message):
    WARNINGS.append(message)


def read_text(path):
    if not os.path.exists(path):
        raise Fail("%s is missing" % path)
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def read_csv(path):
    if not os.path.exists(path):
        raise Fail("%s is missing" % path)
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        raise Fail("%s is empty" % path)
    return rows


def require_files(*names):
    missing = [name for name in names if not os.path.exists(name)]
    if missing:
        raise Fail("missing: %s" % ", ".join(missing))


def require_notes(*headings):
    text = read_text("notes.md")
    missing = [heading for heading in headings if heading not in text]
    if missing:
        raise Fail("notes.md has no section: %s" % " | ".join(missing))


def read_pnm(path):
    text = read_text(path)
    lines = [line.split("#")[0] for line in text.splitlines()]
    tokens = " ".join(lines).split()
    if not tokens:
        raise Fail("%s is empty" % path)
    magic = tokens[0]
    if magic not in ("P1", "P2", "P3"):
        raise Fail("%s starts with %r; use the text formats P1, P2 or P3" % (path, magic))
    try:
        width = int(tokens[1])
        height = int(tokens[2])
    except (IndexError, ValueError):
        raise Fail("%s: the width and the height are missing from the header" % path)
    index = 3
    maxval = 1
    if magic in ("P2", "P3"):
        try:
            maxval = int(tokens[3])
        except (IndexError, ValueError):
            raise Fail("%s: the maximum value is missing from the header" % path)
        index = 4
    channels = 3 if magic == "P3" else 1
    needed = width * height * channels
    values = tokens[index:]
    if len(values) != needed:
        raise Fail("%s: the header says %dx%d, which needs %d values, but the file has %d"
                   % (path, width, height, needed, len(values)))
    try:
        numbers = [int(value) for value in values]
    except ValueError:
        raise Fail("%s contains a value that is not an integer" % path)
    for number in numbers:
        if number < 0 or number > maxval:
            raise Fail("%s has the value %d, outside 0..%d" % (path, number, maxval))
    return {"magic": magic, "width": width, "height": height,
            "maxval": maxval, "values": numbers, "path": path}


def find_frames(minimum=8):
    if not os.path.isdir("frames"):
        raise Fail("the frames/ directory is missing")
    names = sorted(name for name in os.listdir("frames") if name.endswith(".pgm"))
    if not names:
        raise Fail("frames/ has no .pgm files")
    bad = [name for name in names if not re.match(r"^frame_\d\d\.pgm$", name)]
    if bad:
        raise Fail("these names do not use two digits: %s" % ", ".join(bad[:3]))
    if len(names) < minimum:
        raise Fail("only %d frames; the animation needs at least %d" % (len(names), minimum))
    return ["frames/" + name for name in names]


def numbers_in(text):
    return [float(value) for value in re.findall(r"-?\d+(?:\.\d+)?", text)]


def require_gif(path):
    if not os.path.exists(path):
        raise Fail("%s is missing; build it with the convert command from the brief" % path)
    with open(path, "rb") as handle:
        head = handle.read(6)
    if not head.startswith(b"GIF8"):
        raise Fail("%s does not start with GIF8; is it really a GIF?" % path)


def scan_sources(forbidden):
    for name in sorted(os.listdir(".")):
        if not name.endswith(".py") or name == "check.py":
            continue
        with open(name, encoding="utf-8") as handle:
            for number, line in enumerate(handle, start=1):
                code = line.split("#")[0]
                for token in forbidden:
                    if token in code:
                        warn("%s:%d uses %s; the brief asks for a different tool."
                             % (name, number, token))


def main():
    print("")
    print("Checking the project in %s" % os.getcwd())
    print("")
    passed = 0
    failed = 0
    for name, function in CHECKS:
        try:
            function()
        except Fail as error:
            failed += 1
            print("[fail] %s" % name)
            print("       %s" % error)
        except Exception as error:
            failed += 1
            print("[fail] %s" % name)
            print("       the check itself stopped: %s: %s" % (type(error).__name__, error))
        else:
            passed += 1
            print("[ok]   %s" % name)
    print("")
    for message in WARNINGS:
        print("[warn] %s" % message)
    if WARNINGS:
        print("")
    print("%d passed, %d failed" % (passed, failed))
    if failed:
        print("NOT READY YET - fix the [fail] lines above and run the script again.")
        return 1
    print("PROJECT READY - every automatic check passed. Show the program and notes.md.")
    return 0



@check("the files named in the brief exist")
def files():
    require_files("devices.csv", "inventory.py", "report.txt", "conflicts.csv",
                  "network.pgm", "notes.md")


@check("devices.csv has five columns and at least twelve devices")
def devices():
    rows = read_csv("devices.csv")
    if len(rows) < 13:
        raise Fail("devices.csv has %d lines; a header and twelve devices are expected" % len(rows))
    for number, row in enumerate(rows, start=1):
        if len(row) != 5:
            raise Fail("line %d has %d cells, five expected" % (number, len(row)))


@check("conflicts.csv has the four columns from the brief and at least one row")
def conflicts():
    rows = read_csv("conflicts.csv")
    header = [cell.strip().lower() for cell in rows[0]]
    expected = ["kind", "value", "first_line", "second_line"]
    if header != expected:
        raise Fail("conflicts.csv header is %s; expected %s"
                   % (",".join(header), ",".join(expected)))
    if len(rows) < 2:
        raise Fail("conflicts.csv has a header but no conflict rows")


@check("every conflict can be found in devices.csv at the two given lines")
def conflict_lines():
    devices_lines = read_text("devices.csv").splitlines()
    rows = read_csv("conflicts.csv")
    for number, row in enumerate(rows[1:], start=2):
        if len(row) != 4:
            raise Fail("line %d of conflicts.csv has %d cells" % (number, len(row)))
        value = row[1].strip()
        try:
            targets = [int(row[2]), int(row[3])]
        except ValueError:
            raise Fail("line %d of conflicts.csv has a line number that is not a whole number"
                       % number)
        found = 0
        for target in targets:
            for shift in (0, -1, 1):
                index = target + shift - 1
                if 0 <= index < len(devices_lines) and value in devices_lines[index]:
                    found += 1
                    break
        if found < 2:
            raise Fail("the value %s is not on both given lines of devices.csv "
                       "(line %d of conflicts.csv)" % (value, number))


@check("network.pgm has sixteen-pixel squares, at least twelve of them")
def network():
    image = read_pnm("network.pgm")
    if image["magic"] != "P2":
        raise Fail("network.pgm is %s; the map uses the PGM format P2" % image["magic"])
    if image["width"] % 16 or image["height"] % 16:
        raise Fail("width %d and height %d must both be multiples of 16"
                   % (image["width"], image["height"]))
    squares = (image["width"] // 16) * (image["height"] // 16)
    if squares < 12:
        raise Fail("the picture has %d squares; the file has twelve devices" % squares)


@check("report.txt has a header, the totals and a list of problems")
def report():
    text = read_text("report.txt")
    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) < 5:
        raise Fail("report.txt has %d non-empty lines; a header and the totals are expected"
                   % len(lines))
    if not re.search(r"\d", text):
        raise Fail("report.txt contains no numbers")


@check("notes.md has both research notes")
def notes():
    require_notes("## The New Thing – reading an address",
                  "## The New Thing – a missing file")

if __name__ == "__main__":
    sys.exit(main())
