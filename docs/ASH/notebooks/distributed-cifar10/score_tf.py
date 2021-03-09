import os
import time
import tensorflow as tf
import json

# Called when the deployed service starts
def init():
    global model

    # Get the path where the deployed model can be found.
    model_file_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), '001')
    # model_file_path = model_path + '/obj_segmentation.pkl'
    #model_file_path = "C:\\Users\\v-songshanli\projects\\ashexplore\BIG_FILES\\001"

    model = tf.saved_model.load(model_file_path)

# Handle requests to the service
def run(data):
    try:
        # Pick out the text property of the JSON request.
        # This expects a request in the form of {"text": "some text to score for sentiment"}

        start_at = time.time()
        inputs = json.loads(data)
        img_data_list = inputs["instances"]

        signature_name = inputs["signature_name"]
        infer = model.signatures[signature_name]

        inputs_tensor = tf.constant(img_data_list, dtype=tf.float32)

        res = infer(tf.constant(inputs_tensor))
        return {"predictions": res["dense_1"].numpy().tolist(),
                "elapsed_time": time.time() - start_at}
    except Exception as e:
        error = str(e)
        print(error)
        raise e
