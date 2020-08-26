# earthengine-standalone-tools
Standalone tools for Google Earth Engine operations. To get all the tools clone the repo

```bash
git clone https://github.com/samapriya/earthengine-standalone-tools.git
cd earthengine-standalone-tools
```

## eereposnap : [Read the Medium Post Here](https://medium.com/@samapriyaroy/getting-git-right-on-google-earth-engine-e853f6551889)
Tool to create snapshots of earthengine user's Owner, Reader and Writer scripts. Handles issues with git clone in windows and managing repo and permission type.

![repo_extract_headless](https://user-images.githubusercontent.com/6677629/75488708-d440f680-597e-11ea-8590-7d2ee4a90f0d.gif)

## eebasemaps
Google Earth Engine already has tools for you to set some basemaps for example

```js
Map.setOptions('SATELLITE') or Map.setOptions('HYBRID')
```

and so on however what if you want some variety and turns out there is a whole array of snazzy basemaps in a [user contributed website called Snazzy maps](https://snazzymaps.com/) and you can use them in Google Earth Engine. 

This too allows you to convert a snazzy map url directly into a Google Earth Engine Snippet and use it by simply using a snazzy maps url. Here are a few steps

#### To Intsall 
Make sure you have python3 installed and then migrate to the folder inside the cloned repo

```bash
pip install -r requirements.txt
```

#### Usage
* Get the Snazzy Maps URL

![snazzy_maps_get](https://user-images.githubusercontent.com/6677629/91254262-e46c3f80-e72f-11ea-8e66-e16025d46bb4.gif)

* Use the url to generate or export the GEE snippet for the Snazzy map and then use it in Google Earth Engine.

![snazzy_maps_text](https://user-images.githubusercontent.com/6677629/91254270-ecc47a80-e72f-11ea-97d1-a96695473edc.gif)

