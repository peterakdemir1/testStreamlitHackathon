from keras.preprocessing import image
from keras.applications.vgg16 import VGG16, preprocess_input
# from keras.models import Model
from keras.models import load_model
import numpy as np
import piexif
from PIL import Image
from io import BytesIO
import base64

# this is the VGG16 pre-trained model for image classification
# model = VGG16(weights='imagenet')
# model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
# model.save('vgg16-feature-extractor.h5')
model = load_model('vgg16-feature-extractor.h5')

# extract image features using vgg16
def extract_features(base64_str):
    img_data = base64.b64decode(base64_str)
    img_file = BytesIO(img_data)
    img = Image.open(img_file)
    # img = image.load_img(img_path, target_size=(224,224))
    img = img.resize((224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)

    # get features through predict
    features = model.predict(img)

    return features

# get cosine similarity using image features
def calc_cosine_similarity(features1, features2):
    similarity = np.dot(features1, features2.T)
    cosine_similarity = similarity / (np.linalg.norm(features1) * np.linalg.norm(features2))
    return cosine_similarity[0][0]

# get gps info from image with gps metadata
def get_gps_info(base64_str):
    img_data = base64.b64decode(base64_str)
    img_file = BytesIO(img_data)
    img = Image.open(img_file)
    # Load metadata
    exif_dict = piexif.load(img.info["exif"])

    # Get the GPS data
    gps_info = exif_dict.get('GPS', {})
    return gps_info

# get latitude and longitude gps info; this takes in gps exif dict as input so use the return value of get_gps_info()
def get_coords(gps_data):
    data = {
        "latitude": {
            "degrees": 0.0,
            "minutes": 0.0,
            "seconds": 0.0,
            "direction": "N"
      },
      "longitude": {
            "degrees": 0.0,
            "minutes": 0.0,
            "seconds": 0.0,
            "direction": "W"
      }
    }
    latitude = {
        'degrees': 0.0,
        'minutes': 0.0,
        'seconds': 0.0,
        'direction': 'N'
    }

    longitude = {
        'degrees': 0.0,
        'minutes': 0.0,
        'seconds': 0.0,
        'direction': 'W'
    }

    coordinates = [latitude, longitude]
    latitude['degrees'] = gps_data[2][0][0] / gps_data[2][0][1]
    latitude['minutes'] = gps_data[2][1][0] / gps_data[2][1][1]
    latitude['seconds'] = gps_data[2][2][0] / gps_data[2][2][1]
    latitude['direction'] = gps_data[1].decode('utf-8')

    longitude['degrees'] = gps_data[4][0][0] / gps_data[4][0][1]
    longitude['minutes'] = gps_data[4][1][0] / gps_data[4][1][1]
    longitude['seconds'] = gps_data[4][2][0] / gps_data[4][2][1]
    longitude['direction'] = gps_data[3].decode('utf-8')

    data['latitude'].update(latitude)
    data['longitude'].update(longitude)

    return data