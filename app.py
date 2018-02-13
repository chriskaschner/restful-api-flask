import os
import numpy as np
import tensorflow as tf
from urllib.request import urlretrieve
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from PIL import Image

auth = HTTPBasicAuth()
app = Flask(__name__)


@auth.get_password
def get_password(username):
    if username == 'ReturnPath':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized Access'}), 403)


images = [
    {
        'id': 1,
        'title': u'Nikes',
        'url': 'http://imgdirect.s3-website-us-west-2.amazonaws.com/nike.jpg',
        'results': '',
        'resize': False,
        'size': ""
    },
    {
        'id': 2,
        'title': u'Altra',
        'url': 'https://s3-us-west-2.amazonaws.com/imgdirect/altra.jpg',
        'results': '',
        'resize': False,
        'size': ""
    }
]


def make_public_img(image):
    new_image = {}
    for field in image:
        if field == 'id':
            new_image['uri'] = url_for('get_image', img_id=image['id'], _external=True)
        else:
            new_image[field] = image[field]
    return new_image


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


'''
test string 
curl -i http://127.0.0.1:5000/img/api/v1.0/images
'''


@app.route('/img/api/v1.0/images', methods=['GET'])
def get_images():
    return jsonify({'images': [make_public_img(image) for image in images]})


@app.route('/')
@app.route('/index')
def index():
    return "This isn't very interesting, try connecting to http://10la.pythonanywhere.com/img/api/v1.0/images/"


'''
test String
### curl -u ReturnPath:python -i http://127.0.0.1:5000/img/api/v1.0/images/2
### curl -u ReturnPath:python -i http://10la.pythonanywhere.com/img/api/v1.0/images/2
'''


@app.route('/img/api/v1.0/images/<int:img_id>', methods=['GET'])
@auth.login_required
def get_image(img_id):
    img = [img for img in images if img['id'] == img_id]
    if len(img) == 0:
        abort(404)
    return jsonify({'img': img[0]})


'''test String
curl -u ReturnPath:python -i -H "Content-Type: application/json" -X POST -d '{"url":"http://imgdirect.s3-website-us-west-2.amazonaws.com/neither.jpg"}' http://127.0.0.1:5000/img/api/v1.0/images
curl -u ReturnPath:python -i -H "Content-Type: application/json" -X POST -d '{"url":"http://imgdirect.s3-website-us-west-2.amazonaws.com/neither.jpg"}' http://10la.pythonanywhere.com/img/api/v1.0/images
'''


@app.route('/img/api/v1.0/images', methods=['POST'])
@auth.login_required
def create_image():
    if not request.json or 'url' not in request.json:
        abort(400)

    image = {
        # simple way to ensure a unique id, just add 1
        'id': images[-1]['id'] + 1,
        # allow an empty title
        'title': request.json.get('title', ""),
        # url is required, otherwise return error code 400
        'url': request.json['url'],
        'results': request.json.get('results', ""),
        'resize': False,
        'size': ""
    }
    images.append(image)
    return jsonify({'image': make_public_img(image)}), 201


''' test string
 curl -u ReturnPath:python -X PUT -i -H "Content-Type: application/json" -d '{"id":3}' http://127.0.0.1:5000/img/api/v1.0/inference/3
 curl -u ReturnPath:python -X PUT -i -H "Content-Type: application/json" -d '{"id":2}' http://127.0.0.1:5000/img/api/v1.0/inference/1
 curl -u ReturnPath:python -X PUT -i -H "Content-Type: application/json" -d '{"id":2}' http://10la.pythonanywhere.com/img/api/v1.0/inference/1
'''


@app.route('/img/api/v1.0/inference/<int:img_id>', methods=['PUT'])
@auth.login_required
def add_inference(img_id):
    img = [img for img in images if img['id'] == img_id]
    if len(img) == 0:
        abort(404)
    if not request.json:
        abort(400)
    url = img[0]['url']
    img[0]['results'] = run_inference_on_image(url)
    return jsonify({'img': make_public_img(img[0])}), 200


'''
test String
curl -u ReturnPath:python -i -H "Content-Type: application/json" -X PUT -d '{"title":"C-ron-ron"}' http://127.0.0.1:5000/img/api/v1.0/images/3
'''


@app.route('/img/api/v1.0/images/<int:img_id>', methods=['PUT'])
@auth.login_required
def update_image(img_id):
    img = [img for img in images if img['id'] == img_id]
    if len(img) == 0:
        abort(404)
    if not request.json:
        abort(400)
    # todo fix unicode ref
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    img[0]['title'] = request.json.get('title', img[0]['title'])
    img[0]['url'] = request.json.get('url', img[0]['url'])
    return jsonify({'img': img[0]}), 200
    # todo remove this older return statement after verifying functionality
    # return jsonify({'img': make_public_img(img[0])}), 200


'''
test String
curl -u ReturnPath:python -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5000/img/api/v1.0/images/3
'''


@app.route('/img/api/v1.0/images/<int:img_id>', methods=['DELETE'])
@auth.login_required
def delete_image(img_id):
    img = [img for img in images if img['id'] == img_id]
    if len(img) == 0:
        abort(404)
    images.remove(img[0])
    return jsonify({'result': True})


'''
test string
curl -u ReturnPath:python -i -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/img/api/v1.0/resize/2
curl -u ReturnPath:python -i -H "Content-Type: application/json" -X PUT http://10la.pythonanywhere.com/img/api/v1.0/resize/2
'''


@app.route('/img/api/v1.0/resize/<int:img_id>', methods=['PUT'])
@auth.login_required
def get_image_dimensions(img_id):
    img = [img for img in images if img['id'] == img_id]
    if len(img) == 0:
        abort(404)
    url = img[0]['url']
    img[0]['size'] = get_image_dims(url)
    return jsonify({'img': make_public_img(img[0])}), 200


def get_image_dims(img_url):
    image_path, headers = urlretrieve(img_url)
    img = Image.open(image_path)
    width, height = img.size
    size = {
            'height': height,
            'width': width
        }
    return size


# Model and Labels files for TensorFlow
# todo cleanup filenaming
file_names = os.listdir("static")

# modelFullPath = '/static/output_graph.pb'
labelsFullPath = os.path.join("static", file_names[1])
modelFullPath = os.path.join("static", file_names[0])

'''
pythonanywhere handles paths differently, uncomment in production
modelFullPath = '/home/10la/restful-api-flask/static/output_graph.pb'
labelsFullPath = '/home/10la/restful-api-flask/static/output_labels.txt'
'''


def create_graph():
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(img_url):
    results_name = []
    results_score = []
    image_path, headers = urlretrieve(img_url)
    if not tf.gfile.Exists(image_path):
        tf.logging.fatal('File does not exist %s', image_path)
        return None

    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    # Creates graph from saved GraphDef.
    create_graph()

    with tf.Session() as sess:

        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        top_k = predictions.argsort()[-5:][::-1]  # Getting top 5 predictions
        f = open(labelsFullPath, 'rb')
        lines = f.readlines()
        labels = [str(w).replace("\n", "") for w in lines]
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            results_name.append(human_string)
            results_score.append(score)

        results_dict2 = {}
        i = 0
        # todo fix item usage
        for item in results_name:
            results_dict2[i] = {"results_score": format(results_score[i], '.4f'), "results_name": results_name[i]}
            i += 1
        return results_dict2


if __name__ == '__main__':
    app.run()
