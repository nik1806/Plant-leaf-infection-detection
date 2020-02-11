# Plant-leaf-infection-detection
This is the source code for our work submitted for review at Inderscience journal (IJSHC). The respository contains the code as well as the data used for the simulations. 

The dataset is taken from PlanVillage dataset from Sharada Mohanty https://github.com/spMohanty/PlantVillage-Dataset

The different versions of the dataset are present in the raw directory : <br>
  color : Original RGB images <br>
  grayscale : grayscaled version of the raw images <br>
  segmented : RGB images with just the leaf segmented and color  corrected. <br>

### Execution steps:

#### Training Process
```
1. Place 'data_extraction.py' in Train folder of one leaf folder. e.g..
cp data_extraction.py Bell\ Pepper\ Data\ Set/Train_pep_bac/.
2. Create a text file in leaf folder( eg. Bell Pepper Data Set) with naming 'DiseaseType_result.txt'. e.g..
touch Bell\ Pepper\ Data\ Set/bacterial_result.txt
3. Go to Train folder. eg..
cd Bell\ Pepper\ Data\ Set/Train_pep_bac/
4. Update filename on line 162, with file name created in step 2.
5. Execute the data_extraction file
python data_extraction.py
```


The link to the original paper : https://dx.doi.org/10.1504/IJSHC.2019.101602

If our work helps you, please cite it as:
```
N. Paliwal, P. Vanjani, J.-W. Liu, S. Saini, and A. Sharma. ”Image processing-based intelligent robotic system for assistance of agricultural crops.” International Journal of Social and Humanistic Computing,3(2):191–204, 2019.
```
