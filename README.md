
# File Transfer App
#### Jiaqian Huang.2366

# Files
1. server.py and client.py
2. UI: Tkinter
3. Some optional sample files in client and server folder

# Prerequisite
1. Version python3 <=
2. MAC/Linux Only

# Get started
1. ln the terminal, cd into server folder and open the server.py
```
python3 server.py
```

2. ln another terminal, cd into server folder and open the client.py
```
python3 client.py
```
<br />
** Notice: More connections can be made by adding running client.py in other terminals.

3. input server id which will be listed in the terminal

4. register; a notification will pop up to warn the user if the userID already existed.

5. A main page with three buttons will shown on the screen: list the local files, see the available download files, and leave

6. Option: list the local files
<br />
The user can see the files shared. They are uploaded when the user is registered.
<br />
** Notice: If the user wants to upload more, the user need to leave by clicking the button "leave" and register again.

7. Option: see the available download files
<br />
The user can see available files to download.
<br />
** Notice: When testing, please leave after downloading one file. If user wants to download more, please register again.

8. Option: leave
<br />
** Notice: The user is required to click this button for leaving, or they cant leave later when the page is redirected.

# Additional questions and their answers
1. How to prove available files:
<br />
Open 2 client windows, check the second one by clicking show available files.

2. How to prove 2 clients can be onsite together:
<br />
Open 2 client windows, for the second one check available files to download, you can see other people's file. Leave the first one which registered first by clicking leave button. For the second client, check the available files, there are only this users files.

3. How to prove same files can be onsite:
<br />
When check the available files to download, some files have the same name but they belong to different users.

4. How to prove files with same name wont be oeverlapped when download:
<br />
When check the available files to download, the file will be renamed when local has the same file name.


