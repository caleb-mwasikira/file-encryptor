# file-encryptor

File encryptor is a program that enables users to encrypt and decrypt their files with a passphrase.
It implements the latest cryptographic standards to ensure users data is kept secure within their local machine.


### HOW TO INSTALL

1. Download the source code from github using the command:-

   ``git clone https://github.com/caleb-mwasikira/file-encryptor.git``

   Note:- If you don't have git installed, you can download it from [git's official website](https://git-scm.com/downloads).

2. After downloading the source code `cd` into the file-encyptor directory with

   ``cd file-encryptor``

3. And run

   ``pip3 install``

   To install the program dependencies.

4. To produce an executable for your local machine you need to install pyinstaller on your machine;

   ``pip3 install pyinstaller``

5. Using pyinstaller...

   ``pyinstaller --onefile --name [<YOUR_PREFERRED_APP_NAME> | file-encryptor] file_encryptor.py``

   This will produce an executable in the `file-encryptor/build/` directory.

### HOW TO RUN THE PROGRAM

1. With the executable built for your local machine `cd` into the `file-encryptor/build` directory

   ``cd ./build``

   and run the executable.

   ``./file-encryptor``

2. To view commands that come with the program use

   ``./file-encryptor -h or --help``



