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
