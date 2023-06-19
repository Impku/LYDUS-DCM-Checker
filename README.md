# LYDUS-DCM-Checker

Scripts for checking the DCM header and evaluating the integrity and accuracy of the labels.

## Information
  version: 1.0.6 (create: November 11, 2022,update: June 18, 2023)
 
 - This program is used to estimate your DICOM file and give a score based on the most
  important 21 features in DICOM header. Data type and data range will be considered
 in the test. 
 - If a score of dicom file is lower then 90, this DICOM file may cause 
 trouble to your research.
 
 This program made by Yonsei Boncentricq Team

## DCM Headers
|   No.  |   DCM_Attribute  |   Attribute Name              |   sampe1            |   sample2                     |
|--------|------------------|-------------------------------|---------------------|-------------------------------|
|   1    |   0018\|1147     |   Field of View Shape         |   RECTANGLE         |   RECTANGLE                   |
|   2    |   0018\|1149     |   Field of View Dimensions    |   378\240           |   410\228                     |
|   3    |   0028\|0030     |   Pixel Spacing               |   0.143\0.143       |   0.20\0.20                   |
|   4    |   0028\|0106     |   Smallest Image Pixel Value  |   0                 |   0                           |
|   5    |   0028\|0107     |   Largest Image Pixel Value   |   16383             |   4095                        |
|   6    |   0008\|002A     |   Acquisition DateTime        |   2.02E+13          |   2.02E+13                    |
|   7    |   0008\|0060     |   Modality                    |   DX                |   CR                          |
|   8    |   0008\|0070     |   Manufacturer                |   DongKang          |   FUJI PHOTO FILM Co., ltd.   |
|   9    |   0008\|1030     |   Study Description           |   L-Spine AP, Lat   |   L-Spine AP, Lat             |
|   10   |   0008\|103E     |   Series Description          |   LAT               |   LSPINE                      |
|   11   |   0010\|0020     |   Patient ID                  |   1382318           |   3445201                     |
|   12   |   0010\|0040     |   Patient's Sex               |   M                 |   F                           |
|   13   |   0010\|1010     |   Patient's Age               |   062Y              |   085Y                        |
|   14   |   0018\|0015     |   Body Part Examined          |   LSPINE            |   PELVIS                      |
|   15   |   0018\|1000     |   Device Serial Number        |   INNOVISION        |   515PM3EJ200001M             |
|   16   |   0018\|1164     |   Imager Pixel Spacing        |   0.143\0.143       |   0.20\0.20                   |
|   17   |   0018\|5101     |   View Position               |   LAT               |   0                           |
|   18   |   0020\|0060     |   Laterality                  |   R                 |   0                           |
|   19   |   0028\|0004     |   Photometric Interpretation  |   MONOCHROME2       |   MONOCHROME1                 |
|   20   |   0028\|0010     |   Rows                        |   3020              |   2140                        |
|   21   |   0028\|0011     |   Columns                     |   1776              |   1760                        |

## Funding
```
This research was supported by a grant of the Korea Health Technology R&D Project through the Korea Health Industry Development Institute (KHIDI),
funded by the Ministry of Health & Welfare, Republic of Korea (grant number : HI17C1234).
```

## Citation
```bibtex
@software{DCM-Checker,
  author = {Sang Wouk Cho, Sookyeoung Han, Namki Hong},
  organization = {Bonecentriq}
  title = {DCM-Checker},
  url = {https://github.com/Impku/LYDUS-DCM-Checker},
  version = {v1.0.0},
  date = {2022-11-11},
}
```
