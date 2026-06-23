#training graphCNN algorithm
from keras.utils.np_utils import to_categorical
from keras.models import Sequential, load_model
import os
from keras.layers import Dense
import pickle
import numpy as np
from keras_dgl.layers import GraphCNN #loading Graph Neural Network class
import keras.backend as K
from keras.regularizers import l2
from sklearn.metrics import accuracy_score

data = np.load("model/data.npy", allow_pickle=True)
X_train, X_test, y_train, y_test = data

y_train1 = to_categorical(y_train)
y_test1 = to_categorical(y_test)
#Create GNN model to detect fault from all services
graph_conv_filters = np.eye(1)
graph_conv_filters = K.constant(graph_conv_filters)
graph_model = Sequential()
graph_model.add(GraphCNN(64, 1, graph_conv_filters, input_shape=(X_train.shape[1],), activation='elu', kernel_regularizer=l2(5e-4)))
graph_model.add(GraphCNN(32, 1, graph_conv_filters, input_shape=(X_train.shape[1],), activation='elu', kernel_regularizer=l2(5e-4)))
graph_model.add(GraphCNN(1, 1, graph_conv_filters, input_shape=(X_train.shape[1],), activation='elu', kernel_regularizer=l2(5e-4)))
graph_model.add(Dense(units = 64, activation = 'elu'))
graph_model.add(Dense(units = y_train1.shape[1], activation = 'softmax'))
graph_model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
if os.path.exists("model/gcnn_weights.h5") == False:
    hist = graph_model.fit(X_test, y_test1, batch_size=1, epochs=80, validation_data = (X_test, y_test1), verbose=1)
    graph_model.save_weights("model/gcnn_weights.h5")
else:
    graph_model.load_weights("model/gcnn_weights.h5")
#perform prediction on test data of all services and calculate accuracy and other metrics
pred = []
for i in range(len(X_test)):
    temp = []
    temp.append(X_test[i])
    temp = np.asarray(temp)
    predict = graph_model.predict(temp, batch_size=1)
    predict = np.argmax(predict)
    pred.append(predict)
y_tested = np.argmax(y_test1, axis=1)    
predict = np.asarray(pred)
#calling function to calculate accuracy on predicted data
acc = accuracy_score(y_tested, predict)
print(acc)
