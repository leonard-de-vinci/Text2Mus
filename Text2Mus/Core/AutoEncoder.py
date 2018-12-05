from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras import backend as K
from tensorflow.keras.callbacks import ModelCheckpoint


class AutoMidi():
    """Auto encoder"""
    def __init__(self):
        self.autoencoder = self.getModel()
        self.filepath = "weights-e{epoch:02D}va{val_acc:.2f}.hdf5"
        self.weights = "weights.h5"
        self.checkpoint = ModelCheckpoint(self.filepath,save_best_only = True)
        self.callbackList = [self.checkpoint]
    def trainGenerator(self, training_generator,validation_generator):
        self.autoencoder.fit_generator(generator=training_generator,
                        validation_data=None,
                        use_multiprocessing=False,
                        workers=1,
                        callbacks=None,
                        steps_per_epoch = 5)
        
    def predict(self,x):
        return self.decoder.predict(x)
    def getModel(self):
        encoding_dim = 32
        mod = Sequential()
        mod.add(Conv2D(50, (2,2), activation='relu', padding='same', input_shape=(16,128,5000)))
        mod.add(MaxPooling2D((2,2), padding='same'))
        mod.add(Conv2D(10, (2,2), activation='relu', padding='same'))
        mod.add(MaxPooling2D((2,2), padding='same'))
        mod.add(Conv2D(6, (2,2), activation='relu', padding='same'))
        mod.add(MaxPooling2D((2,2), padding='same'))
        mod.add(Conv2D(encoding_dim, (2,2), activation='relu', padding='same'))

        mod.add(UpSampling2D((2,2),name = "a"))
        mod.add(Conv2D(10, (2,2), activation='relu', padding='same',name = "b"))
        mod.add(UpSampling2D((2,2),name ="c"))
        mod.add(Conv2D(50, (2,2), activation='relu', padding='same',name="d"))
        mod.add(UpSampling2D((2,2),name ="e"))
        mod.add(Conv2D(5000, (2,2), activation='sigmoid', padding='same',name ="f"))
        mod.compile(optimizer='adadelta', loss='binary_crossentropy')
        return mod

        #input_img = Input(shape=(16,128,5000))
        #x = Conv2D(500, (2,2), activation='relu', padding='same')(input_img)
        #x = MaxPooling2D((2,2), padding='same')(x)
        #x = Conv2D(100, (2,2), activation='relu', padding='same')(x)
        #x = MaxPooling2D((2,2), padding='same')(x)
        #x = Conv2D(64, (2,2), activation='relu', padding='same')(x)
        #x = MaxPooling2D((2,2), padding='same')(x)
        #encoded = Conv2D(encoding_dim, (2,2), activation='relu', padding='same')(x)
        #x = UpSampling2D((2,2))(encoded)
        #x = Conv2D(100, (2,2), activation='relu', padding='same')(x)
        #x = UpSampling2D((2,2))(x)
        #x = Conv2D(500, (2,2), activation='relu', padding='same')(x)
        #x = UpSampling2D((2,2))(x)
        #decoded = Conv2D(5000, (2,2), activation='sigmoid', padding='same')(x)
        #autoencoder = Model(input_img, decoded)
        #autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
        
        #return autoencoder
    def GetEncoder(self):
        encoder_layer =self.autoencoder.layers[:6]
        encoder = Model(encoder_layer)
        encoded_input = Input(shape=(encoding_dim,))
        encoder.compile(optimizer='adadelta', loss='binary_crossentropy')
        return encoder
    def GetDecoder(self):
        self.autoencoder.save(self.weights)
        dec= Sequential()
        dec.add(UpSampling2D((2,2),name = "a",input_shape = (2,16,32)))
        dec.add(Conv2D(10, (2,2), activation='relu', padding='same',name = "b"))
        dec.add(UpSampling2D((2,2),name ="c"))
        dec.add(Conv2D(50, (2,2), activation='relu', padding='same',name="d"))
        dec.add(UpSampling2D((2,2),name ="e"))
        dec.add(Conv2D(5000, (2,2), activation='sigmoid', padding='same',name ="f"))
        dec.compile(optimizer='adadelta', loss='binary_crossentropy')
        dec.load_weights(self.weights, by_name=True)
        return dec
        











