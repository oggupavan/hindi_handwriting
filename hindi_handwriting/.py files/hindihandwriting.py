#MODEL PART


import numpy as np
from keras import layers
from keras.layers import Input,Dense,Activation,ZeroPadding2D,BatchNormalization,Flatten,Conv2D
from keras.layers import AveragePooling2D,MaxPool2D,Dropout,GlobalAvgPool2D,GlobalMaxPool2D,MaxPooling2D
from keras.utils import np_utils,print_summary
import pandas as pd
from keras.models import Sequential
from keras.callbacks import  ModelCheckpoint
import keras.backend as k


data=pd.read_csv("data.csv")
dataset=np.array(data)
np.random.shuffle(dataset)
x=dataset
y=dataset
x=x[:,0:1024]
y=y[:,1024]

# as we have 72000 data elements we are dividing them into test train set of 70000 & 2000
x_train=x[0:70000,:]
x_train=x_train/255.      # in this step we are conerting pixal values varing from 0-255 to (0-1) by dividing it by 255 and making calcluation easy and reducing run time
x_test=x[70000:72001,:]
x_test=x_test/255.    #remember to add . as it indicates that ur using float number not integer


#reshape

y=y.reshape(y.shape[0],1)
y_train=y[0:70000,:]
y_train=y_train.T
y_test=y[70000:72001,:]
y_test=y_test.T






print("number of training examples ="+str(x_train.shape[0]))
print("number of test examples ="+str(x_test.shape[0]))
print("x_train shape:"+str(x_train.shape))
print("x_test shape:"+str(x_test.shape))
print("y_train shape:"+str(y_train.shape))
print("y_test shape:"+str(y_test.shape))




image_x=32
image_y=32

train_y=np_utils.to_categorical(y_train)
test_y=np_utils.to_categorical(y_test)
train_y=train_y.reshape(train_y.shape[1],train_y.shape[2])
test_y=test_y.reshape(test_y.shape[1],test_y.shape[2])
x_train=x_train.reshape(x_train.shape[0],image_x,image_y,1)
x_test=x_test.reshape(x_test.shape[0],image_x,image_y,1)


print("x_train shape:"+str(x_train.shape))
print("y_train shape :"+str(train_y.shape))


# BULINDING MODEL

def keras_model(image_x,image_y):
    num_of_classes=37
    model=Sequential()

    model.add(Conv2D(filters=32,kernel_size=(5,5),input_shape=(image_x,image_y,1),activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2),padding='same'))
    model.add(Conv2D(64,(5,5),activation='relu'))
    model.add(MaxPooling2D(pool_size=(5,5),strides=(5,5),padding='same'))
    model.add(Flatten())
    model.add(Dense(num_of_classes,activation='softmax'))
    model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
    filepath="devanagari.h5"
    checkpoint1=ModelCheckpoint(filepath,monitor='val_acc',verbose=1,save_best_only=True,mode='max')
    callbacks_list=[checkpoint1]

    return model,callbacks_list


model,callbacks_list=keras_model(image_x,image_y)
model.fit(x_train,train_y,validation_data=(x_test,test_y),epochs=15,batch_size=64,callbacks=callbacks_list)
scores=model.evaluate(x_test,test_y,verbose=0)
print("CNN ERROR:%.2f%%"%(100-scores[1]*100))
print_summary(model)
model.save('devanagari.h5')


