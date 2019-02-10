<a href="https://wordlift.io"><img src="img/Wl-logo-horizontal.png"/></a>


# SEO image optimization using Computer Vision
### A WordLift experiment to generate image captions

This script uses **Python** with the Microsoft Computer Vision API (provided as part of the [Microsoft Cognitive Services](https://www.microsoft.com/cognitive-services)) to generate meta description for images stored on a WordPress website. 
You will need an API key from Microsoft and the export of your WordPress Media Library that can be done using the WordPress Export Tool. The result is a CSV file containing the URL of the image, the title of the image, the proposed description for the image and a confidence score. The script will skip the analysis if the description is already present in your media library.   

## Instructions
To run the script simply download it and follow these steps: 

### 1. Export WordPress XML Media Contents
  - Login to your WordPress dashboard, and navigate to Tools Export.
  - Choose to export Media content.
  - Click Download Export File and the XML content will be downloaded in .xml format with a date on its file name.
### 2. Add your [Microsoft Computer Vision API Key](https://www.microsoft.com/cognitive-services/en-us/computer-vision-api) 
  - Update [line 16](https://github.com/cyberandy/image-captioning/blob/f669b8ac75757f7a85ff951309ac898d7a618ee2/generate-descriptions.py#L16) 
### 3. Replace the name of the XML file that you exported from WordPress
  - Update [line 31](https://github.com/cyberandy/image-captioning/blob/dcbb1624ef5322d17f7abe07b47c90031282adeb/generate-descriptions.py#L31)
### 4. Make sure you have all the required libraries installed 
If not use `pip install` to install the libraries below: 
  - time 
  - requests
  - operator
  - numpy 
  - pandas
  - xmltodict 
### 5. run the code from the terminal window
  - write `python generate-descriptions.py` 
  
The script will generate a file called *out.csv* that contains a list of the processed images containing their original title, the url of the image, the metadescription generated by the Computer Vision API and a confidence score (this will come handy when you will have to choose if it's worth keeping what the CV has suggested).

## License
The code is free and licensed with the Apache 2.0 License.  
