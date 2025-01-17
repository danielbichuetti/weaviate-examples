import weaviate
import datetime
import base64, json, os
import cv2, sys
from own_vec import getFaceEncoding

def testImage(nearImage):
    '''
    This function takes in a dictionary with key as "image" and value as the path of that image.
    Then it finds the most similar image to the uploaded image and returns its label.
    In this, it uses image2vecneural.
    '''
    client = weaviate.Client("http://localhost:8080")
    print("Client created (student_test.py file)")

    res = client.query.get("Students", ["image","labelName"]).with_near_image(nearImage).do()
    print(res['data']['Get']['Students'][0].keys())

    # returning the labelName of the most similar image
    return (res['data']['Get']['Students'][0]['labelName'])

def getFaces(image,write=True):
    '''
    This function takes in an image path as a parameter and then uses OpenCv
    functions to identify faces in the image. Then it saves all those faces as
    separate images in the Faces directory.

    Parameters:
    image - Path of an image.
    '''
    # give image path as parameter
    imagePath = image
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30)
    ) 
    found_faces = []
    print("Found {0} Faces!".format(len(faces)))

    # Below is a standard code available in the OpenCV documentation and on various websites.
    # Refer to https://www.digitalocean.com/community/tutorials/how-to-detect-and-extract-faces-from-an-image-with-opencv-and-python to get more details.
    # I have used code from the above mentioned website to extract faces from an image.

    for (x, y, w, h) in faces:

        cv2.rectangle(image, (x, y), (x+w+20, y+h+20), (0, 255, 0), 2)
        roi_color = image[y:y + h, x:x + w] 
        print("[INFO] Object found. Saving locally.") 
        if write:
            cv2.imwrite("Faces/"+str(w) + str(h) + '_faces.jpg', roi_color) 

            found_faces.append("Faces/"+str(w) + str(h) + '_faces.jpg')
        else:
            found_faces.append(roi_color)
        
    if write:
        status = cv2.imwrite('Squares/faces_detected.jpg', image)
        print ("Image faces_detected.jpg written to filesystem: ",status)
    return found_faces

    
def clean():
    '''
    This functions removes all faces from a Faces directory.
    This can be used after every class, so as to start fresh attendance
    in the next class.
    '''
    for i in os.listdir("Faces/"):
        os.remove(i)
    print("Faces folder cleaned")

def testit(path):

    client = weaviate.Client("http://localhost:8080")
    print("Client created (student_test.py file)")

    test = getFaceEncoding(path)
    nearVector = {"vector": test}
    res = client.query.get("Students", ["labelName", "_additional {certainty}"]).with_near_vector(nearVector).do()
    #print(res)
    ans = res['data']['Get']['Students'][0]['labelName']
    print(ans)
    return ans

# for f in getFaces("C:/Users/aakash/Downloads/a333.jpeg"):
#     print(f)
#     testit(f)
#     print("==================")