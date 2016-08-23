from flask import render_template, jsonify, abort, make_response, request, url_for
from app import app

jsonimages = [ #fake json array of images
{
  "url": "http://imgdirect.s3-website-us-west-2.amazonaws.com/nike.jpg",
  "uri": "https://chriskaschner.pythonanywhere.com/img/api/v1.0/images/1",
  "title": "Nikes"
},
{
  "url": "http://imgdirect.s3-website-us-west-2.amazonaws.com/altra.jpg",
  "uri": "https://chriskaschner.pythonanywhere.com/img/api/v1.0/images/2",
  "title": "Altra"
},
{
  "url": "http://imgdirect.s3-website-us-west-2.amazonaws.com/neither.jpg",
  "uri": "https://chriskaschner.pythonanywhere.com/img/api/v1.0/images/3",
  "title": "3rd cousin"
}
]

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'ReturnPath'} # fake user

    return render_template('index.html',
                            title='Home',
                            user=user,
                            images=jsonimages)


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

@app.route('/img/api/v1.0/images', methods=['GET'])
def get_images():
    return jsonify({'images': [make_public_img(image) for image in jsonimages]})

@app.route('/img/api/v1.0/images/<int:img_id>', methods=['DELETE'])
# @auth.login_required
def delete_image(img_id):
    img = [img for img in images if img['id'] == img_id]
    if len(img) == 0:
        abort(404)
    images.remove(img[0])
    return jsonify({'result': True})
