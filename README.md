# CS551Q Assignment 3

### What is this?
This `README.md` will show the files about CS551Q Assignment 3.

### Use of <script> in Templates
The only JavaScript in this assignment is <script> in html templates for dealing with maps.

# How to run (with pythonanywhere)
Please visit this url to get to the homepage: https://peiheng.pythonanywhere.com/  
Ordinary Account [username: testman, password: test123456!]  
Admin Account [username: codio, password: codio]  
With admin account you can see all the users and orders. Also you can go to the admin control page.  

# How to run through codio (local version)
Use this command:
```bash
source .venv/bin/activate
python3 manage.py runserver 0.0.0.0:8000
```
Then visit this url to get to our homepage: https://sundaycinema-ericregard-8000.codio-box.uk/meteorite/

# Solutions for some common questions:
### Get python version 3.10.7
When open your codio link for this Assignment, firstly checking the python version is necessary. Try with this code:
```bash 
python --version
```
If your python version is 2.7.17, you should download 3.10.7 version. Type the following command:
```bash
pyenv install 3.10.7
```
If you meet an error like '*python-build: definition not found: 3.10.7*', then you should upload your pyenv. Try this:
```bash
cd ~/.pyenv
git pull
```
Then, go back to your working directory:
```bash
cd -
```
Now you should be able to download the version 3.10.7:
```bash
pyenv install 3.10.7
```
After downloading, remember to check the version again. If it's still 2.7.17, try this command:
```bash
pyenv rehash
```

### Download files from github repository
I have created a repository on github for this Assignment, you can download files from it. You can use this commend to download.
```bash
git clone https://github.com/Thorki-Su/CS551Q_Assignment_1.git
```
This will download all the files into your codio as a new folder '*CS551Q_Assignment_3*'. To make edits and commits easier, please move all files out of the folder.

### Get sqlite version 3.49.1
Please use this command to check your sqlite version:
```bash
sqlite3 --version
```
If your version is 3.22, please update the version. In the files downloaded from github, there are prepared sqlite documents.
```bash
cd sqlite-autoconf-3490100
./configure --prefix=$HOME/sqlite
make
make install
```
Then set environment variables so Python uses the new SQLite:
```bash
export PATH="$HOME/sqlite/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/sqlite/lib"
```
Check version again and your sqlite should be 3.49.1

# Usage of Templates
All templates and their usage will be listed here:  
'404.html' and '500.html' for error control.  
'main.html' for the parent template to other templates.  
'homepage.html' for the home page of this software.  
'list.html' for the products list page.  
'detail.html' for the product detail page.  
'compare.html' for the compare page.  
'cart.html' for the cart page.   
'my_orders.html' for the order history page.  
'admin_dashboard.html' for the admin page.  
'login.html' for the log-in page.  
'profile.html' for the user profile page.  
'register.html' for the user register page.  

# Data sources
The meteorite data I used comes from https://www.kaggle.com/datasets/nasa/meteorite-landings/data. You can find the excel file in 'meteorite/meteorite_data/meteorites'.
The open source map tool: https://leafletjs.com/.

# The name in git-log
Thorki Su is the username of Peiheng Su in github.