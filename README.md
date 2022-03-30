## **Motivation & Description**

There was a problem of passing a test, which was conducted in a class room using our laptops, when a teacher is floating around to assure everyone is not cheating(doing alt-tab, using phone etc.). And in addition there was a risk of a low/no internet connection at our university.

That's why I spent Sunday creating this thing, and not reading lots of sc(r)um materials.

At the time, this module allows you to set a bunch of keyboard shortcuts to:
* take whole screenshots.
* upload them to the Google Drive.*Your backup person with access to the drive checks screenshots and uploads answers as a text file*
* download this text file
* show its contents as a system tray icon(a few characters at a time, allowing getting next/prev ones)

## **Dependencies & Installation**

* `requirements.txt` (see its comments)
* you should install them globally as icon lib `pystray`(at least) uses some system libs.
* tested on pytnon 3.6.9

## **Usage**

1. Create a google project, enable drive api, create a service account and download its credentials as a `.json` file. 

2. Create a folder in your drive and grant access to it for the service account.

3. Fill in `conf.yaml`:
```yaml
answers_local_filepath: "resources/ans.txt"
answers_remote_filename: "ans.txt"

drive_api_json_path: "resources/client_secrets.json"
drive_dir_name: "screens"

# quality from 0 to 100 of output jpegs
image_quality: 65

icon_image_props:
  font_path: "resources/UbuntuMono-R.ttf"
  font_size: 22
  chars_per_screen: 4
  sizes: [50, 50]
  text_coords: [0, 8]

# icon dropdown menu names
icon_dropdown_names:
  left: left
  right: right
  sync_answers: sync
  toggle_visibility: show/hide
  exit: exit

# command aliases -> class paths
commands_mapping:
  sync_images: "cheattest.commands.gdrive.SyncImagesCommand"
  sync_answers: "cheattest.commands.gdrive.SyncRemoteAnswersCommand"
  make_screen: "cheattest.commands.screenshot.ScreenCommand"
  restart_icon: "cheattest.commands.icon.RestartIconCommand"
  send_left: "cheattest.commands.send_icon.SendLeftIconCommand"
  send_right: "cheattest.commands.send_icon.SendRightIconCommand"
  send_sync: "cheattest.commands.send_icon.SendSyncIconCommand"
  send_toggle: "cheattest.commands.send_icon.SendToggleIconCommand"
```

Notes:
* relative paths are resolved according to the root project directory. 
* `drive_dir_name` - name of the created folder on the google drive.
* `answers_remote_filename` - name of the file with answers under `drive_dir_name`.
* `image_quality` - used to reduce screenshot size using `mogrify -quality ...`, specify 100 to remain images as is.
* `chars_per_screen` - number of characters to be showed at a time. If you specify too big number, they may not fit the icon.
* `sizes`, `text_coords` - icon sizes and text coordinates. 
* Use mono fonts and play with `icon_image_props` options to ensure all the text is visible.
* `commands_mapping`:  
`sync_images` - upload images to the drive(already uploaded images won't be uploaded twice)  
`sync_answers` - download answers from the drive.  
`make_screen` - take screenshot and save it under `resources/images`  
`restart_icon` - kill previous icon processes if there are any and start new one.  
`send_left`/`send_right` - send command to the icon udp unix socket to show previous/next characters. If you send left at a beginning, an end part will be showed and vice versa.
`send_sync` - send command to the icon udp unix socket to load local answers. Note that the current ones won't be showed until you call left or right.  
`send_toggle` - send command to the icon udp unix socket to show/hide icon text. 

4. set up shortcuts for the command aliases by calling: 

`python /path/to/cheattest/cli.py alias1 alias2 ...` 

## **Demonstration**

1) answers file contents: `1:1;2:4,6;`

![image](https://user-images.githubusercontent.com/56230007/160715717-a2c275a0-de89-44ff-8022-7cacd2aa2441.png)

![image](https://user-images.githubusercontent.com/56230007/160715742-0dc9a148-05ed-4461-87d9-ec02ab1d083e.png)

![image](https://user-images.githubusercontent.com/56230007/160715765-b55d32f1-5dfa-4bd9-914c-fd88ad1696d6.png)

![image](https://user-images.githubusercontent.com/56230007/160716478-97fdfed3-81ff-4326-b18f-47e91996dbed.png)


2) `python cli.py make_screen sync_images`

![Screenshot from 2022-03-30 01-17-19](https://user-images.githubusercontent.com/56230007/160716505-8a6a9d66-cc0f-4f4e-91f3-ac5d00ae3a92.png)

![Screenshot from 2022-03-30 01-17-27](https://user-images.githubusercontent.com/56230007/160716519-3ddbf8a7-fc63-4a35-b5dd-69ea9871f340.png)
















