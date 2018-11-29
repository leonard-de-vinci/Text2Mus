from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.keras.models import Model
from tensorflow.keras import backend as K


class AutoMidi():
    """Auto encoder"""
    def __init__(self):
        self.encoder,self.decoder,self.autoencoder = self.getModel()

    def trainGenerator(self, training_generator,validation_generator):
        self.autoencoder.fit_generator(generator=training_generator,
                    validation_data=validation_generator,
                    use_multiprocessing=False,
                    workers=1)
    def predict(self,training_generator):
        
        return self.autoencoder.predict(x)

    def getModel(self):
        input_img = Input(shape=(16,128,10000)) 
        x = Conv2D(1000, (2,2), activation='relu', padding='same')(input_img)
        x = MaxPooling2D((2,2), padding='same')(x)
        x = Conv2D(500, (2,2), activation='relu', padding='same')(x)
        x = MaxPooling2D((2,2), padding='same')(x)
        x = Conv2D(64, (2,2), activation='relu', padding='same')(x)
        encoded = MaxPooling2D((2,2), padding='same')(x)
        x = Conv2D(16, (2,2), activation='relu', padding='same')(encoded)
        x = UpSampling2D((2,2))(x)
        x = Conv2D(500, (2,2), activation='relu', padding='same')(x)
        x = UpSampling2D((2,2))(x)
        x = Conv2D(1000, (2,2), activation='relu', padding='same')(x)
        x = UpSampling2D((2,2))(x)
        decoded = Conv2D(10000, (2,2), activation='sigmoid', padding='same')(x)
        autoencoder = Model(input_img, decoded)
        autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
        return encoded, decoded, autoencoder







