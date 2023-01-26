### Automatic car classification with AI

# Introduction

We aim to build a service capable of predicting European cars’ make and model based on pictures to automatically categorize vehicles of e-commerce.

As more cars are digitally sold than ever , used car marketplaces are in constant need to automatically process large volumes of images to enhance seller publication times, automatically curate items in the marketplace in order to increase conversion rates, and provide better product discovery and shopping experiences to their customers.


#0.1 Flask ML API
In the end we have built an API to classify cars from photos.

##0.2 Install and run

To run(then stop) the services using compose:

```bash
$ cd frontend
$ docker-compose up --build -d
```

```bash
$ cd frontend
$ docker-compose down
```

Now we can speak about the car classifier per se.

## 1. Install
You can use `Docker` to install all the needed packages and libraries easily. 
Two Dockerfiles are provided for both CPU and GPU support.

- **CPU:**
```bash
$ docker build -t auto_car --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -f docker/Dockerfile .
```
- **GPU:**
```bash
$ docker build -t auto_car --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -f docker/Dockerfile_gpu .
```
### Run Docker

- **CPU:**
```bash
$ docker run --rm --net host -it -v $(pwd):/home/app/src --workdir /home/app/src auto_car bash
```
- **GPU:**

```bash
$docker run --rm --net host --gpus all -it -v $(pwd):/home/app/src --workdir /home/app/src auto_car bash
```

## 2. Dataset
It was stored on a AWS-S3 bucket. It consisted of over 1.6 million images.
It is of course not included in this repo. We do include a tiny sample of 80 images on the eu-car-dataset folder.


### 3. Prepare your data

After downloading, the dataset should look like this:
```
eu-car-dataset/
    ├── abarth-124_spider_2008
    	 	├── 168_1_d6f280fd-09e9-4c32-b03d-c8e16d3d40ea_45217939-5b8c-439f-aa1c-01fc217790c4.jpg
       	├── .....
```
The dataset weighted 187gb, with 1.6 million images, distributed among 6273 subfolders.
There are plenty of broken/empty images, and pictures we do not want to deal with such as :
	* pictures from interior of the car
	* pictures of the steering wheel
	* pictures of cars with theirs doors opened
	* partial pictures of the car
	
We first got rid of the broken images:
```bash
$ cd scripts
$ python3 image_fixer.py "../eu-car-dataset"
```

We then trained a binary classifier to stick with only the desired images. 
We randomly picked 10k images with the script: 
	scripts/sample_random_images.py
We then proceeded to manually label them, and trained a MobileNetV2 through the scripts:
	
	models/MobileNetV2 (creates the model)
	scripts/train.py

The training gave back an accuracy of .98 for the classes [‘auto’, ‘no_auto’]. 
To classify the entire dataset we used: 
```bash
$ cd scripts
$ python3 car_nocar_classiffier.py "../eu-car-dataset"
```

This last script created, on each car model subdirectory, a csv called "car_nocar_class.csv", which indicated for each .jpg file whether it corresponded to a car or not. We considered as a car, the filed classified as cars with a probability of 0.7 or more.

After this step, the useful dataset consisted of roughly 691k images (42% of the original).

### 4. Run car+truck detector on the images.
First we create a new directory for only the cars, according to the csvs "car_nocar_class.csv" previously created on each subdirectory.
We stick with only the cars with prob>0.7 according to the "car_nocar_classifier.py"
At the same time we merge all of the folders for each car model into one; for example:

	"mercedes-benz_v_2016" + "mercedes-benz_v_2017" + "mercedes-benz_v_2018" ----> "mercedes-benz_v"

```bash
$ cd scripts
$ python3 car_nocar_for_yolo.py
```
The new directory will be "eu-car-only_autos".

We use the YoloV5m object detector, to detect cars and trucks on the images.
We want to keep only with the cropped car images, since actually we only want the image that consists of the bounding box for each car. For each original image, we get only the largest detected bounding box(since there may be more than one vehicle per image).
That was for the classes 2 & 7 (cars & trucks).

The runtime of this over the whole cars dataset was approximately 96hs.

```bash
$ python3 run_yolo_allfolders.py
```
We will now have the directory "eu-car-croped_autos"
At this point the directory "eu-car-only_autos" could be deleted with no problem.

But for each car model inside "eu-car-croped_autos", we have subdirectories "car", "truck", "label"
We deal with that in the script:
```bash
$ cd scripts
$ python3 car_truck_merge_after_yolo.py
```
Now we finally have the car images in the folder:
	"data"

At this point the directory "eu-car-only_autos", could be deleted with no problem.

### 5. Train-Test-Validation split
By running the following script, we generate the tables 
	** "table_for_test.csv"
	** "table_for_train.csv"
	** "table_for_val.csv"
```bash
$ cd scripts
$ python3 split_traintestval_1.py
```
They are already stored, there should be no need to run it again.

Then, we use the followings script  to actually make the split.
The proportions are 70-15-15.
We generate the train, test, val subsets in the "data" dataset.
Given some unbalance in the dataset, we ignored car models with less than 150 pictures.

We took into account an important detail: the dataset in general contained for each car, several pictures of it from different angles.
For example, if we had an image named "851_1_vlnlvnflvnjvj.jpg", all of the images starting with "851" on the subdirectory would correspond to the same car. We separate the images in such a way that the same cars/trucks do not remain in separate places, this is necessary since otherwise the model will learn by heart since it has the same car in test and train.
So we made shure all those images would stick together after the train-test-validation split.

```bash
$ cd scripts
$ python3 split_traintestval_2.py
```
The folder "../data" was generated, which we finally use to train our model.
We should end up with:
data/
  ├── train
       ├── abarth-124_spider
       ├── 168_1_d6f280fd-09e9-4c32-b03d-c8e16d3d40ea_45217939-5b8c-439f-aa1c-01fc217790c4.jpg
       ├── .....

  ├── test
	├── abarth-124_spider
    	├── .....
      	├── .....


  ├── val
	├── abarth-124_spider
    	├── .....
      	├── .....
    


### 6. Merging data
After running some initial models, we discovered similarities among the car models.
We decided to merge some classes and ignore others.
We end up with 512 classes.
We trained the models again after this.

```bash
$ cd scripts
$ python3 merge_classes.py
```
### 7. Models
We trained from an EfficientNetB1 network, with 100 epochs.
More details in the folder experiments.


### Weights
We do not include the weights of the final model, necessary for the API.
There were originally in "experiments/exp_final_512_retrain/model.25-0.3795-0.9380.h5"
but they were moved so they could be used by the api, to the directory:

"frontend/uploads/model.25-0.3795-0.9380.h5"

We do not include the weights "weights_for_car_nocar_classifier/model.18-0.0782-0.9802.h5" 

