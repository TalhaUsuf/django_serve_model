# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                      what  task celery should do
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import importlib
import logging
from celery import Task
import sys, os
sys.path.append(os.pardir)
from app.detector.detection_model.resnet_feature_extractor import extract_features
from worker import app

class PredictTask(Task):
    """
    Abstraction of Celery's Task class to support loading ML model.
    """
    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        """
        Load model on first call (i.e. first task processed)
        Avoids the need to load model on each task request
        """
        if not self.model:
            logging.info('Loading Model...')
            self.model = extract_features()
            logging.info('Model loaded')
        return self.run(*args, **kwargs)



@app.task(ignore_result=False,
          bind=True,
          base=PredictTask,
          path=('/home/talha/PycharmProjects/django_backend_api/app/detector/detection_model/resnet_feature_extractor', 'features_extract'),
          name='{}.{}'.format(__name__, 'features_extract'))
def give_features(self, data):
    """
    Essentially the run method of PredictTask
    """
    assert isinstance(data, (list,)) , "data must be a list"
    print([i for i in data])
    # out = [self.model.predict(i).cpu().squeeze().list() for i in data]
    out = [self.model.predict(i) for i in data]

    return out