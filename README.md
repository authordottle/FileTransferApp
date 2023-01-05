
# File Transfer App
## Jiaqian Huang.2366

# What makes it
## One server.py in server folder
## One client.py in client folder
## UI: Tkinter
## Some sample files in client and server folder


# What to require
## python3
## Need to run on the MAC/Linux

# How to start

## ln the terminal:
## cd into server folder and open the server.py
## $ python3 server.py

## ln another terminal:
## cd into server folder and open the client.py
## $ python3 client.py
## ** Notice: More connections can be made by adding running client.py in other terminals.

## First, input server id:
## It will be listed in the terminal.

## Second, register:
## A notification will pop up to warn the user if the userID already existed.

## Third, main page:
## Three buttons will shown on the screen: list the local files, see the available download files, and leave

## list the local files:
## The user can see the files shared. They are uploaded when the user is registered.
## ** Notice: If the user wants to upload more, the user need to leave by clicking the button "leave" and register again.

## see the available download files:
## The user can see available files to download.
## ** Notice: When testing, please leave after downloading one file. If user wants to download more, please register again.

## leave:
## ** Notice: The user need to leave by clicking this button, or they cant leave later when the page is redirected.

## How to prove available files:
## Open 2 client windows, check the second one by clicking show available files.

## How to prove 2 clients can be onsite together:
## Open 2 client windows, for the second one check available files to download, you can see other people's file. Leave the first one which registered first by clicking leave button. For the second client, check the available files, there are only this users files.

## How to prove same files can be onsite:
## When check the available files to download, some files have the same name but they belong to different users.

## How to prove files with same name wont be oeverlapped when download:
## When check the available files to download, the file will be renamed when local has the same file name.


