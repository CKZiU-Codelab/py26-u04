# py26-u04 – LAN Inventory

**u04** · Python course 2026/27 · week 6

Each project lives in its own directory, together with the brief, my notes and
the self-check script. The brief is the source of truth; this file only
explains the workflow.

## Week 6 – LAN Inventory

- directory: `lan_inventory/`
- brief: `lan_inventory/PROJEKT.md` (the same text is in `lan_inventory/PROJEKT.pdf`)

## Workflow

1. Fork this repository to your own account (once per repository).
2. Clone your fork and add this repository as `upstream`.
3. Create a branch for the week, for example `w06-lan_inventory`.
4. Work inside `lan_inventory/` only.
5. Run the check before you push:

   ```bash
   cd lan_inventory
   python3 check.py
   ```

6. Commit, push to your fork and open a pull request against `main` here.
7. Answer the review comments in the same pull request.

The first commands, once:

```bash
git clone git@github.com:<your-login>/py26-u04.git
cd py26-u04
git remote add upstream git@github.com:CKZiU-Codelab/py26-u04.git
```

## Rules

- Work only inside `lan_inventory/`.
- Keep the files your program produced: the CSV, the images and the reports.
  They are the result, not a side effect.
- Do not edit `check.py`; it is the teacher's file.
- No secrets and no files from outside the project directory.
