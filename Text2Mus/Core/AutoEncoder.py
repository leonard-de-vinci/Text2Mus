from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.keras.models import Model
from tensorflow.keras import backend as K
from tensorflow.keras.callbacks import ModelCheckpoint


class AutoMidi():
    """Auto encoder"""
    def __init__(self):
        self.encoder,self.decoder,self.autoencoder = self.getModel()
        self.filepath = "weights-e{epoch:02D}va{val_acc:.2f}.hdf5"
        self.checkpoint = ModelCheckpoint(self.filepath,save_best_only = True)
        self.callbackList = [self.checkpoint]
    def trainGenerator(self, training_generator,validation_generator):
        self.autoencoder.fit_generator(generator=training_generator,
                    validation_data=validation_generator,
                    use_multiprocessing=False,
                    workers=1,
                    callbacks=self.callbackList)
    def predict(self,training_generator):
        
        return self.autoencoder.predict(x)

    def getModel(self):
        encoding_dim = 32
        input_img = Input(shape=(16,128,5000)) 
        x = Conv2D(500, (2,2), activation='relu', padding='same')(input_img)
        x = MaxPooling2D((2,2), padding='same')(x)
        x = Conv2D(100, (2,2), activation='relu', padding='same')(x)
        x = MaxPooling2D((2,2), padding='same')(x)
        x = Conv2D(64, (2,2), activation='relu', padding='same')(x)
        x = MaxPooling2D((2,2), padding='same')(x)
        encoded = Conv2D(encoding_dim, (2,2), activation='relu', padding='same')(x)
        x = UpSampling2D((2,2))(encoded)
        x = Conv2D(100, (2,2), activation='relu', padding='same')(x)
        x = UpSampling2D((2,2))(x)
        x = Conv2D(500, (2,2), activation='relu', padding='same')(x)
        x = UpSampling2D((2,2))(x)
        decoded = Conv2D(5000, (2,2), activation='sigmoid', padding='same')(x)
        autoencoder = Model(input_img, decoded)
        autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
        encoder = Model(input_img,encoded)
        encoded_input = Input(shape=(encoding_dim,))
        decoder_layer = autoencoder.layers[-1]
        decoder = Model(encoded_input, decoder_layer(encoded_input))
        return encoder, decoder, autoencoder







