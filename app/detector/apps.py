from django.apps import AppConfig
from detector.detection_model.resnet_feature_extractor import extract_features
# from detection_model.resnet_feature_extractor import extract_features

class DetectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'detector'

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #                      code inside this will be
    #                     loaded only once
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    predictor = extract_features()
