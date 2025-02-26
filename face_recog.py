#Libraries 
import numpy as np
import cv2

# instantiate the camera object and haar cascade
cam = cv2.VideoCapture(0)
face_cas = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# declare the type of font to be used on output window
font = cv2.FONT_HERSHEY_SIMPLEX

# load the data from the numpy matrices and convert to linear vectors
f_01 = np.load('Rajat.npy').reshape((20, 50*50*3))
f_02 = np.load('Sonam.npy').reshape((20, 50*50*3))
f_03 = np.load('Ash.npy').reshape((20, 50*50*3))
f_04 = np.load('Nikita.npy').reshape((20, 50*50*3))

print (f_01.shape, f_02.shape, f_03.shape, f_04.shape)

# create a look-up dictionary
names = {
	0: 'Rajat',
	1: 'Sonam',
	2: 'Ash',
    3: 'Nikita'
}

# create a matrix to store the labels
labels = np.zeros((80, 1))
labels[:20, :] = 0.0	# first 20 for Rajat (0)
labels[20:40, :] = 1.0	# next 20 for Sonam (1)
labels[40:60, :] = 2.0	# last 20 for Ash (2)
labels[60:, :] = 3.0

# combine all info into one data array
data = np.concatenate([f_01, f_02, f_03, f_04])	# (60, 7500)
print (data.shape, labels.shape)	# (60, 1)

# the distance and knn functions we defined earlier
def distance(x1, x2):
    return np.sqrt(((x1-x2)**2).sum())

def knn(x, train, targets, k=5):
    m = train.shape[0]
    dist = []
    for ix in range(m):
        # compute distance from each point and store in dist
        dist.append(distance(x, train[ix]))
    dist = np.asarray(dist)
    indx = np.argsort(dist)
    sorted_labels = labels[indx][:k]
    counts = np.unique(sorted_labels, return_counts=True)
    return counts[0][np.argmax(counts[1])]

while True:
	# get each frame
	ret, frame = cam.read()

	if ret == True:
		# convert to grayscale and get faces
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_cas.detectMultiScale(gray, 1.3, 5)

		# for each face
		for (x, y, w, h) in faces:
			face_component = frame[y:y+h, x:x+w, :]
			fc = cv2.resize(face_component, (50, 50))

			# after processing the image and rescaling
			# convert to linear vector using .flatten()
			# and pass to knn function along with all the data

			lab = knn(fc.flatten(), data, labels)
			# convert this label to int and get the corresponding name
			text = names[int(lab)]

			# display the name
			cv2.putText(frame, text, (x, y), font, 1, (255, 255, 0), 2)

			# draw a rectangle over the face
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
		cv2.imshow('face recognition', frame)

		if cv2.waitKey(1) == 27:
			break
	else:
		print ('Error')

cv2.destroyAllWindows()
