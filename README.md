# ELISAQuant
An app to easily and reproducibly quantify analyte concentration

[ELISAQuant](https://www.google.com)

## To Do:
- Develop visualization for model evaluation
- Finish download data button
- Containerize app
- Deploy app to host

## How to Use ELISAQuant
To use the ELISAQuant app use the data upload tool (displayed below) by following
the steps outlined below.

![Data Upload Tool](/assets/data_upload_tool.png)

### 1. Choose Template

Select the template that you used for your plate. This app provides you with two
option. These options can be observed in the following images.

![Option 1](/assets/option_1.png)

![Option 2](/assets/option_2.png)


### 2. Enter Concentration for Standard Wells
Enter the known analyte concentration of the standards in the corresponding well
of your plate.

### 3. Upload Data
Upload the output of your plate reader by selecting the 'Upload File' button and
selecting your file. This file can be either a 'csv' or 'xls'.
Check out the [example ELISA](https://www.google.com) to see how this file should
be formatted.

### 4. Perform Analysis
After entering the concentration for the standard well and uploading your dataset,
select the 'Perform Analysis' button to predict the concentration of the measured
analyte for each of the sample wells. A 5-parameter logistic model is then fit to
the analyte concentration of the standards and the respective optical density of
the analyte. The model that has been fit is then used to predict the analyte
concentration of your samples.

### 5. Download Your Results
The plot displaying your standard curve and your measured samples can be downloaded
by hovering over the plot until you see the toolbar and select the camera icon.

The 'Download Data' button allows you to download the dataset of the predictions.
