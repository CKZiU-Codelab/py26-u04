# Project – LAN Inventory

**Individual Project Brief – Week 6 · u04**

Start: Monday, 16 November 2026. Show the working program on Monday, 23 November 2026.

## The Idea

You build the inventory of a small school network. The program reads `devices.csv` — hostname, IPv4 address, MAC address, room and device type — checks every record, finds duplicated addresses, counts the devices in every subnet and writes three outputs: a readable report, a list of conflicts and a PGM map of the whole network in which one square is one device and its shade is its type.

This is a file database with rules attached. The file stores the facts; the program decides whether the facts are possible. That is the part of network administration that is done by hand in too many schools, and it is the part a Python program does best.

## Why This Project Is Yours

You set up a DHCP server with Linux during your practice week and you liked the network side of it: the light on a card, a cable out to the LAN, addresses that must be unique. You also write small scripts to make your own computer easier to use. This project is that habit one step further: a script that knows the rules of the network and refuses to accept a record that breaks them.

## What You Already Have

- Lists, tuples, indices and slices, `for` and `while` loops.
- Conditions, logical operators and `%s`, `%d` formatting.
- `open()` inside `with`, reading and writing files, and the `csv` module.
- The PGM format: `P2`, width, height, maximum value, then a grid of numbers.

## The New Thing

A network address is not a number and not a word — it is four numbers with a punctuation rule. Find out how to:

1. Split a string into parts and remove spaces and newline characters from the parts.
2. Check whether a string contains only digits, and what `"07".isdigit()` returns.
3. Convert each part to an integer and test the allowed range.
4. Explain why `192.168.0.300` and `192.168.0.010` are both invalid addresses, and which of the two Python accepts.
5. Check the shape of a MAC address: six pairs, hexadecimal characters, one separator.
6. Check whether a file exists before you open it, and what the program should do when it does not.

**Write it down:** Create `notes.md` with `## The New Thing – reading an address`. Describe the validation of one IPv4 address in four short sentences, one per check, and give one address that passes your checks and still looks wrong to a network administrator. Then add `## The New Thing – a missing file` and explain in two sentences what your program does when `devices.csv` is absent.

## The Plan

### Milestone 1 – The inventory file

Create `devices.csv` by hand.

1. Twelve devices: two switches, six computers, two access points, one printer and one server.
2. Include one device with an octet above `255`, one with a duplicated IP address and one with a MAC address of the wrong shape.
3. Use three different rooms, and at least two subnets.

### Milestone 2 – Read, split, check

Create `inventory.py`.

1. Read the file with the `csv` module and print every row with its line number.
2. Validate the IP address octet by octet, then the MAC address, then the presence of every field.
3. Print `OK` or the first reason for failure for each row.
4. Count valid and invalid records.

At the end of this step eleven or twelve rows are marked and the bad ones are named precisely.

### Milestone 3 – Duplicates

1. Compare every IP address with every other IP address in a nested loop.
2. Do the same for MAC addresses and for hostnames.
3. Write `conflicts.csv` with the columns `kind,value,first_line,second_line`.
4. Print a summary: how many conflicts, of which kind.

### Milestone 4 – Subnets and types

1. Group the devices by the first three octets of the address.
2. Count the devices per subnet and per device type, using parallel lists and nested loops.
3. Print the busiest subnet and the most common device type.
4. Warn when a subnet holds more than five devices and say why that matters in a school.

### Milestone 5 – The report

1. Write `report.txt` with a header, the totals, the counts per type and per subnet, and a numbered list of every invalid row with its reason.
2. Format the table with field widths so that the columns line up.
3. Print the report on the screen as well, so that a run shows what the file contains.

### Milestone 6 – The network map

1. Create `network.pgm` with a `P2` header.
2. Draw one square per device, sixteen by sixteen pixels, arranged in the order of the file.
3. Choose a gray value per device type — switch, computer, access point, printer, server — and draw an invalid record as the brightest value.
4. Print a legend to the terminal and the same map as letters, so a person can read it without an image viewer.

## Example

```text
Reading devices.csv
  line 2  sw-core-01    10.0.0.1      aa:bb:cc:00:00:01  serwerownia  switch    OK
  line 3  pc-101        10.0.0.21      aa:bb:cc:00:00:21  sala 101     pc        OK
  line 4  pc-102        10.0.0.21      aa:bb:cc:00:00:22  sala 101     pc        OK
  line 5  ap-201        10.0.0.300     aa:bb:cc:00:00:23  sala 201     ap        invalid: octet 300 out of range
  line 6  printer-01    10.0.1.10      aa:bb:cc:00:00:2   sekretariat  printer   invalid: MAC has 5 pairs

10 valid, 2 invalid
Duplicated IP addresses: 1
Subnets: 10.0.0.0/24 (7), 10.0.1.0/24 (3)

Saved report.txt
Saved conflicts.csv (1 row)
Saved network.pgm (64x48)
```

## Requirements

- One program, `inventory.py`, started from the terminal with `python3 inventory.py`.
- Every address is validated before it is used, and an invalid record is never counted as a device.
- Duplicates are found with nested loops, not by sorting and comparing neighbours.
- `conflicts.csv` is written with the `csv` module and holds the line numbers of both records.
- `report.txt` names every invalid row and its reason; the totals match the counts in the file.
- `network.pgm` has a correct header and one square per record, including the invalid ones.
- The program does not crash when `devices.csv` is missing.

## Files

```text
lan_inventory/
├── devices.csv
├── inventory.py
├── report.txt
├── conflicts.csv
├── network.pgm
├── notes.md
└── check.py
```

Commit the whole directory to your repository and push it before the Monday session. A directory that exists only on your laptop cannot be checked.

Run `python3 check.py` in the project directory before you commit. It reads the files your program produced, not your code, and prints one line per requirement.


## How It Will Be Checked

- The report's valid count plus its invalid count equals the number of data rows.
- Every conflict in `conflicts.csv` can be found in `devices.csv` at the two given lines.
- The per-subnet counts add up to the number of valid devices.
- Squares in `network.pgm` match the legend and the file order.
- Removing `devices.csv` produces a clear message, not a traceback.
- You can explain your octet check to someone who has never seen an IPv4 address.

**Hint:** Validate a string before you convert it. `int("10a")` raises an error, and an error in the middle of a nested loop stops the whole report — check first, convert second, and keep the reason in a variable so you can write it out later.

**Additional challenge:** Add a generated address plan: for every room, propose the next free address in the room's subnet and write `proposal.csv`. Keep the addresses stable between runs, so that the same input always produces the same proposal, and describe in `notes.md` how you prevented an address from being proposed twice.

## Suggested Learning Resources

- [String methods – `split`, `strip`, `isdigit`, `lower`](https://docs.python.org/3/library/stdtypes.html#string-methods)
- [The `os.path` module – checking whether a file exists](https://docs.python.org/3/library/os.path.html)
- [The `csv` module – reading and writing tabular data](https://docs.python.org/3/library/csv.html)
- [Netpbm – description of the PGM format](https://netpbm.sourceforge.net/doc/pgm.html)

**Final goal:** By the end of this project, you should have a program that turns a hand-written device list into a validated inventory: it checks addresses, finds duplicates, summarizes subnets, writes a report and a conflict list, and draws the network as a PGM picture — using loops, conditions, lists and file handling from the first five weeks.
