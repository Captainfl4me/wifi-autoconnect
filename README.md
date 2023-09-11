# Welcome to WiFi Auto Connect !

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
      }
    }
  ]
}
```
You can add as many sub-configs as you want, just make sure to choose a different name for each section. 
For example, if you want to add a second subconfig, you can name it [YOUR_SUBCONFIG_NAME2].