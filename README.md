# 3D_Zipper_Tube_Modeling

This repository provides a way to model any zipper tube, provided the user can supply angles and lengths for the tube.

## Virtual Enviroment Information

### Introduction
Creating a virtual enviroment in python is a great way to seperate different coding projects on your system. A virtual enviroment allows you to select an interpreter, download project-specific packages, and run code so that the code will work the same for anyone on any system. The virtual enviroment takes packages listed in the requirements.txt file and downloads those specific files. 

It is important to note that this step is not necessary. It just provides a great way to organize things on your computer.

### Setup
- You can either clone the repository first, or create a virtual enviroment. I would recommend creating cloning the repository first, and then you can create a virtual enviroment in the same folder by going onto VS Code in the folder with the repository, and using the ctrl+shift+p to bring up the command lines. 
- You can then search for and select create a virtual enviroment. I've been using .venv types mostly. 
- After your enviroment is created, you need to download the files listed in the requirements.txt file. Head to the terminal, locate the same folder, and type **source venv/bin/activate** for linux/mac, or **.venv\Scripts\activate.bat** for windows. This command sources your virtual enviroment, after which you can use **pip install -r requirements.txt** to download all the files you need to your computer