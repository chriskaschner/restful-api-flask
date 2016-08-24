import numpy as np
import tensorflow as tf
import json
import urllib
from flask import Flask, jsonify, render_template, abort, make_response, request, url_for, Markup
from flask.ext.httpauth import HTTPBasicAuth
from PIL import Image
import markdown

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

###todo replace URL with URI to be overly pedantic
###todo sort out img vs image vs images usage
###todo update example images to reflect good predictions

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
        'url': 'http://imgdirect.s3-website-us-west-2.amazonaws.com/altra.jpg',
        'results': '',
        'resize': False,
        'size': ""
    }
]

def make_public_img(image):
    new_image={}
    for field in image:
        if field == 'id':
            new_image['uri']= url_for('get_image', img_id=image['id'], _external=True)
        else:
            new_image[field] = image[field]
    return new_image

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/markdown')
def get_markdown():
    with open('markdown.txt', 'r') as markdown_file:
        content=markdown_file.read()
    content = Markup(markdown.markdown(content))
    return render_template('markdown.html', **locals())


### test string
### curl -i http://127.0.0.1:5000/img/api/v1.0/images
@app.route('/img/api/v1.0/images', methods=['GET'])
def get_images():
    return jsonify({'images': [make_public_img(image) for image in images]})

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'ReturnPath'} # fake user
    return render_template('index.html',
                            title='Home',
                            user=user,
                            images=images)

### test String
### curl -u ReturnPath:python -i http://127.0.0.1:5000/img/api/v1.0/images/2
@app.route('/img/api/v1.0/images/<int:img_id>', methods=['GET'])
# @auth.login_required
def get_image(img_id):
    img = [img for img in images if img['id'] == img_id]
    if len(img) == 0:
        abort(404)
    return jsonify({'img': img[0]})

### test String
### curl -u ReturnPath:python -i -H "Content-Type: application/json" -X POST -d '{"url":"http://imgdirect.s3-website-us-west-2.amazonaws.com/neither.jpg"}' http://127.0.0.1:5000/img/api/v1.0/images
@app.route('/img/api/v1.0/images', methods=['POST'])
#@auth.login_required
def create_image():
    if not request.json or not 'url' in request.json:
        abort(400)

    image = {
        ### simple way to ensure a unique id, just add 1
        'id' : images[-1]['id'] + 1,
        ### allow an empty title
        'title': request.json.get('title', ""),
        ### url is required, otherwise return error code 400
        'url': request.json['url'],
        'results': request.json.get('results', ""),
        'resize': False,
        'size': ""
    }
    images.append(image)
    return jsonify({'image': make_public_img(image)}), 201

### test string
### curl -u ReturnPath:python -X PUT -H "Content-Type: application/json" -d '{"id":3}' http://127.0.0.1:5000/img/api/v1.0/inference/3
### curl -u ReturnPath:python -X PUT -H "Content-Type: application/json" -d '{"id":2}' http://127.0.0.1:5000/img/api/v1.0/inference/2
@app.route('/img/api/v1.0/inference/<int:img_id>', methods=['PUT'])
# @auth.login_required
def add_inference(img_id):
    img = [img for img in images if img['id'] == img_id]
    if len(img) == 0:
        abort(404)
    if not request.json:
        abort(400)
    url = img[0]['url']
    img[0]['results'] = run_inference_on_image(url)
    return jsonify({'img': img[0]})

### test String
### curl -u ReturnPath:python -i -H "Content-Type: application/json" -X PUT -d '{"title":"C-ron-ron"}' http://127.0.0.1:5000/img/api/v1.0/images/3
@app.route('/img/api/v1.0/images/<int:img_id>', methods=['PUT'])
# @auth.login_required
def update_image(img_id):
    img = [img for img in images if img['id'] == img_id]
    if len(img) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    img[0]['title'] = request.json.get('title', img[0]['title'])
    img[0]['url'] = request.json.get('url', img[0]['url'])
    return jsonify({'img': img[0]})

### test String
### curl -u ReturnPath:python -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5000/img/api/v1.0/images/3
@app.route('/img/api/v1.0/images/<int:img_id>', methods=['DELETE'])
# @auth.login_required
def delete_image(img_id):
    img = [img for img in images if img['id'] == img_id]
    if len(img) == 0:
        abort(404)
    images.remove(img[0])
    return jsonify({'result': True})

### test string
### curl -u ReturnPath:python -i http://127.0.0.1:5000/img/api/v1.0/resize/2
@app.route('/img/api/v1.0/resize/<int:img_id>', methods=['PUT'])
# @auth.login_required
def get_image_dimensions(img_id):
    img = [img for img in images if img['id'] == img_id]
    if len(img) == 0:
        abort(404)
    url = img[0]['url']
    img[0]['size'] = get_image_dims(url)
    return jsonify({'img': img[0]})

###todo add this functionality
# ### test string
# ### curl -u ReturnPath:python -X PUT -H "Content-Type: application/json" -d '{"id":3}' http://127.0.0.1:5000/img/api/v1.0/inference/3
# ## curl -u ReturnPath:python -X PUT -H "Content-Type: application/json" -d '{"id":2}' http://127.0.0.1:5000/img/api/v1.0/inference/2
# @app.route('/img/api/v1.0/resize/<int:img_id>', methods=['PUT'])
# #@auth.login_required
# def resize_image(img_id):
#      ## if bigger than desired size
#      desiredSize = 480
#
#      if img[0]['size']['height'] or img[0]['size']['width'] > desiredSize:
#          print "do work and resize"
#          img[0]['resize'] = True
#      else:
#          img[0]['resize'] = True
#      ## resize image to smaller size
#      ## else set resized to True and move on
#
#
# def resize_image(img_id):
#     img = [img for img in images if img['id'] == img_id]
#     if len(img) == 0:
#         abort(404)
#     if not request.json:
#         abort(400)
#     url = img[0]['url']
#     img[0]['results'] = resize_image(url)
#     img[0]['resize'] = True
#     return jsonify({'img': img[0]})

def get_image_dims(imgURL):
    imagePath, headers = urllib.urlretrieve(imgURL)
    img=Image.open(imagePath)
    width, height = img.size
    size = {
            'height' : height,
            'width': width
        }
    return size

# def resize_image(imgURL):
#     pass
     ## if bigger than desired size
     ## resize image to smaller size
     ## else set resized to True and move on

### Model and Labels files for TensorFlow
modelFullPath = './static/output_graph.pb'
labelsFullPath = './static/output_labels.txt'

def create_graph():
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

def run_inference_on_image(imgURL):
    # answer = None
    ###todo clean up these lists/ dictionaries
    results_dict = {}
    results = []
    results_name = []
    results_score = []
    imagePath, headers = urllib.urlretrieve(imgURL)
    if not tf.gfile.Exists(imagePath):
        tf.logging.fatal('File does not exist %s', imagePath)
        return answer

    image_data = tf.gfile.FastGFile(imagePath, 'rb').read()

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
            # print('%s (score = %.5f)' % (human_string, score))
        # answer = labels[top_k[0]]
        results = zip(results_name, results_score)
        results_dict = {
            "results_name_1": results_name[0],
            "results_score_1": json.JSONEncoder().encode(format(results_score[0], '.4f')),
            "results_name_2": results_name[1],
            "results_score_2": json.JSONEncoder().encode(format(results_score[1], '.4f')),
            "results_name_3": results_name[2],
            "results_score_3": json.JSONEncoder().encode(format(results_score[2], '.4f'))
        }
        return results_dict

if __name__ == '__main__':
    app.run(debug=True)
