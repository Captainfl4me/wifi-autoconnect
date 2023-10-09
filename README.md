# Welcome to WiFi Auto Connect !
A python script compile in an executable to send a custom request when conneciton to a Wi-Fi. Helping with autoconnection for web-portal.

## Installation
You have two options if you want to use this little program. Either compile from source code to have the very latest version or just download the zip folder via the [release page](https://github.com/Captainfl4me/wifi-autoconnect/releases). And then create the json config file by following the guide below.

### Download
Download the zip folder in the [release page](https://github.com/Captainfl4me/wifi-autoconnect/releases). Then, extract it where you want to store the program and run the installTask.ps1 to automatically create the task in the windows task scheduler to run the executable each time you connect to a Wi-Fi.

### Compile from source code
If you want you can clone this repos. Create a python virtual env with:
```
python -m venv env
```
Activate the python environment
```
.\env\Scripts\Activate.ps1
```
Install dependencies
```
pip install -r requirements.txt
```
Compile the connect.py into an .exe with pyinstaller (dist/connect.exe)
```
pyinstaller connect.spec
```

## How to create config file
First, create a config.json file in the same directory as the script. Then, open the file and write the following:
```json
{
  "sections": [
    {
      "name": "NAME_OF_YOUR_SUBCONFIG",
      "url": "URL_OF_THE_LOGIN_PAGE",
      "SSID": "SSID_OF_THE_WIFI",
      "method": "POST",
      "body": {
        "REQUEST_BODY_KEY": "REQUEST_BODY_VALUE"
      },
      "delay": "DELAY_IN_SECONDS"
    }
  ]
}
```
You can add as many sub-configs as you want, just make sure to choose a different name for each section. 
For example, if you want to add a second subconfig, you can name it [YOUR_SUBCONFIG_NAME2].