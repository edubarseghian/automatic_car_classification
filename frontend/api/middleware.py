import json
import time
from uuid import uuid4

import redis
# from model import ml_service
import settings

import pickle
# from model import ml_service

import logging


# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
#db = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
db = redis.StrictRedis(host=settings.REDIS_IP,
                       port=settings.REDIS_PORT, db=settings.REDIS_DB_ID)


def model_predict(image_name):
    """
    Receives an image name and queues the job into Redis.
    Will loop until getting the answer from our ML service.

    Parameters
    ----------
    image_name : str
        Name for the image uploaded by the user.

    Returns
    -------
    prediction, score : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    prediction = None
    score = None

    # Assign an unique ID for this job and add it to the queue.
    # We need to assing this ID because we must be able to keep track
    # of this particular job across all the services
    # TODO
    job_id = str(uuid4())
    print(job_id)
    # Create a dict with the job data we will send through Redis having the
    # following shape:
    # {
    #    "id": str,
    #    "image_name": str,
    # }
    # TODO
    job_data = {
        'id': job_id,
        'image_name': image_name
    }

    # Send the job to the model service using Redis
    # Hint: Using Redis `lpush()` function should be enough to accomplish this.
    # TODO
    newImg2Predict = json.dumps(job_data)
    print(settings.REDIS_QUEUE)
    db.lpush(settings.REDIS_QUEUE, newImg2Predict)

    # Loop until we received the response from our ML model

    while True:
        # Attempt to get model predictions using job_id
        # Hint: Investigate how can we get a value using a key from Redis
        # TODO
        # 12090f1a-2e85-4cb8-bbf5-75b7cfb09ab3

        #job_id = '0b339a0a-89ab-4c4c-a734-b26387ca0e20'
        # if db.exists(job_id) != 0:
        output = db.get(job_id)
        if output is None:
            time.sleep(settings.API_SLEEP)
            continue

        returnPrediction = json.loads(output)
        prediction = returnPrediction['PredictionClas']
        # logging.warning(returnPrediction)
        score = returnPrediction['score']
        db.delete(job_id)
        break
        # Don't forget to delete the job from Redis after we get the results!
        # Then exit the loop
        # TODO

        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)
    return prediction, score

    # break


# a, b = model_predict('C:\\Users\\sotot\\Downloads\\bike.jpg')
