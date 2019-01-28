============================
COPY COMPARE TOOL (Python 3)
============================

********************************
How to use this tool like a NOOB
********************************

1. Open CMD with admin privilege

.. highlights:: Open folder
.. highlights:: File(top left) -> Open Windows PowerShell -> Open Windows PowerShell as administrator
.. highlights:: Type cmd
.. highlights:: Hit Enter

2. Start Copy Compare S3, S4 or CS cycle

Examples:

.. highlights:: copy_compare.exe 1 GB S3
.. highlights:: copy_compare.exe 800 KB CS --pair 70
.. highlights:: copy_compare.exe 100 MB S4 -P 5 -C 5000
.. highlights:: copy_compare.exe 100 MB S4 --pair 5 --cycle 5000


Note: For running CS (Connect Standby/Modern Standby) you must first install WDTF provide by Microsoft.

**********************
EXE file and arguments
**********************

copy_compare.exe : The executable file to perform copy compare

pwrtest.exe : Microsoft Power Test executable file, remember to install WDTF first.

position 1 : number of file size.

position 2 : unit of file size.

position 3 : sleep state, only support S3(Sleep), S4(Hibernate) and CS(Connect Standby/Modern Standby)

-P, --pair : File pairs to copy and compare. (Default: 1)

-C, --cycle : iteration cycle. (Default: infinity, run until fail)

******************
Note: Install WDTF
******************

1. Download WDK (Click the link in Step 2. We don't need to install Visual Studio)

https://docs.microsoft.com/en-us/windows-hardware/drivers/download-the-wdk

2. Change directory

.. highlights:: cd %programfiles%\\Windows Kits\\10\\Testing\\Runtimes

3. Install WDTF (must use cmd with admin privilege)

.. highlights:: msiexec /i "Windows Driver Testing Framework (WDTF) Runtime Libraries-x64_en-us.msi"

******************************
Note: Compile from source code
******************************

0. Install python 3.6 or above

1. Delete existing `build` and `dist` folder and `*.spec` files

2. Connect to internet

3. Open cmd and run command ``pip install -Ur requirements.txt``

4. Run `compile.bat`

5. Put Microsoft `pwrtest.exe` next to `copy_compare.exe`
