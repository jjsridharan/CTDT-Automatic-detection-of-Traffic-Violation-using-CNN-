This project will detect traffic violations like helmet detection, number of persons exceeding two and speed violation.

We had prepared our own dataset for helmet detection and it's accuracy is above 90%.

Number of persons is detected using the co-ordinates from bounding box. 
First motorcycle is detected and within certain co-ordinate points if the number of persons are exceeding three we will consider that as Violation. 
For detecting persons and vehicles we are using pre-trained model.

Speed violation is detected using displacement made by the vehicle between two points. (It will work only for particular angle at which camera is placed)

Number of persons violation and speed violation depends exactly on the angle at which camera is placed.

Once any of the above violation is detected, number plate of the corresponding vehicle is found and fine amount is automatically detected from his travel card. (This is our propopsed system for the project)
Fine collection is done through php and mysql.


Necessary Packages
1) Tensorflow
2) Numpy
3) matplotlib
4) PIL
5) cv2

How to run?

1) Install necessary packages.
2) Download the data and HelmetDetections from google drive. (Link : https://drive.google.com/drive/folders/1SlMm6_B3uTt5EW--QHVMzrFoMpKzxYVG)
3) In vehicle_detection.py you have to modify the input video file name. (Line no. 29) Provision for image testing is also there. Edit from lines(132)
4) Create database with name as "id2536892_ctdt" and import the ctdt.sql file present. ( I created a free account in 000webhost. You can also create new account if you want.)
5) Upload Insert.php and Update.php to a website. In Insert.py and Update.py change the links to file accorodingly. 
6) start (python vehicle_detection.py)


Steps 4 and 5 are optional to detect fine amount.

You can visualize bounding box by uncommenting visualization lines in visualization_utils.py.



