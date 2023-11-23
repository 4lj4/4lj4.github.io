# A guide to unpacking "KingPhisher.zip"
- SHA256: 
- VT Link: 
- Sample download: https://github.com/4lj4/4lj4.github.io/blob/main/samples/sample-files/KingPhisher/KingPhisher.zip

I will make this document a bit nicer later, this is just the basics

# Required tools:
- Python
- Pyinstxtractor https://github.com/extremecoders-re/pyinstxtractor
- Pycdc https://github.com/zrax/pycdc
- Windows virtual machine
- x64dbg
- Ghidra

# Stage 1: Identifying usage of ShellExecuteA
Using ghidra, you can decompile the executable and you will find that it has very few imports, one of those being ShellExecuteA.
This is a clear indication that this function is being used for executing some next stage of infection

# Stage 2: Grabbing dropped files from temp using x64dbg
- Load up a VM with the malware sample and x64dbg.
- Open the imports tab and go to shell32 => ShellExecuteA and toggle its breakpoint.
- You can now run the code, and at each breakpoint on the stack you will be able to see the path of files it has dropped/is about to execute
The program drops 3 files:
- actions.exe (pyinstalled Creal grabber)
- update.exe (some crypto miner - needs more investigation)
- kingphisher msi installer
You can copy these files out of temp and analyse them further

# Stage 3: Extracting webhook from actions.exe
Run Pyinstxtractor on actions.exe to dump the pyc files, then run pycdc on Creal.pyc.
This will print the webhook straight onto your screen!

# Stage 4: Troll the webhook
:)

The webhook is still active as of 23rd Nov 2023 14:21 GMT