from flask_app import app
from flask_app.config.helpers import cloudinaryUpload
from flask import render_template, redirect, session, request, flash, jsonify

from flask_app.models import model_album, model_image, model_albums_has_images, model_business_info

@app.route('/admin/album/create', methods=['POST'])          
def album_create():
    if not model_album.Album.validate(request.form):
        return redirect('/admin/gallery')

    model_album.Album.create(**request.form, user_id=session['uuid'])
    return redirect('/admin/gallery')

@app.route('/admin/album/<int:id>/add_photo', methods=['post'])          
def album_add_photo(id):
    album = model_album.Album.get_one(id=id)
    data = {**request.form}
    if not model_image.Image.validate(data, request.files):
        return redirect(f'/admin/album/{id}/edit')

    for key in request.files:
        resp = cloudinaryUpload(request.files[key], f'/{album.name}', data['name'])
        data['url'] = resp['url']
    
    data['user_id'] = session['uuid']
    image_id = model_image.Image.create(**data)
    model_albums_has_images.AlbumsHasImages.create(image_id=image_id, album_id=album.id)

    return redirect(f'/admin/album/{id}/edit')

@app.route('/admin/album/<int:id>/edit')          
def album_edit(id):
    context = {
        'album': model_album.Album.get_one(id=id),
        'all_photos': model_image.Image.get_all_in_album({'album_id': id})
    }
    return render_template('admin/album_edit.html', **context)

@app.route('/album/<int:id>/update', methods=['POST'])          
def album_update(id):
    return redirect('/')

@app.route('/api/album/<int:id>/update', methods=['POST'])
def api_update(id):
    album = model_album.Album.get_one(id=id)
    data = {**request.form}
    res = {
        'status': 200,
        'id': album.id
    }
    if request.files:
        for key in request.files:
            if request.files[key].content_type != 'application/octet-stream':
                resp = cloudinaryUpload(request.files[key], f'/{album.name}', key)
                data['cover_image_url'] = resp['url']
                res['url'] = resp['url']
    model_album.Album.update_one(id=id, **data)

    return jsonify(res)

@app.route('/admin/album/<int:id>/delete')          
def album_delete(id):
    model_album.Album.delete_one(id=id)
    return redirect('/admin/gallery')


@app.route('/album/<int:id>')
def album_show(id):
    context = {
        'all_photos': model_image.Image.get_all_in_album({'album_id': id}),
        'album': model_album.Album.get_one(id=id),
        'business': model_business_info.BusinessInfo.get_all()[0],
    }
    return render_template('/onlooker/album_show.html', **context)