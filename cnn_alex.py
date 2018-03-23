from keras.models import Model
from keras.layers import Conv2D,MaxPooling2D,Activation,Dropout,Flatten,Dense,Input

# quick model 
def get_model():
    InputPitch = Input(shape=(256,256,3))
    x = Conv2D(32,(3,3),activation='relu')(InputPitch)
    x = MaxPooling2D(pool_size=(2,2))(x)
    
    x = Conv2D(32,(3,3),activation='relu')(x)
    x = MaxPooling2D(pool_size=(2,2))(x)
    
    x = Conv2D(64,(3,3),activation='relu')(x)
    x = MaxPooling2D(pool_size=(2,2))(x)
    
    flat = Flatten()(x)
    x = Dense(64,activation="relu")(flat)
    x = Dropout(0.5)(x)
    pred = Dense(1,activation='sigmoid')(x)
    
    model = Model(inputs=InputPitch,outputs=pred)
    model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['accuracy'])
    return model
