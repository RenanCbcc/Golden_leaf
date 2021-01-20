import os
import io
import base64
import secrets
from PIL import Image


from flask import current_app
from flask_mail import Message



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    image_path  = os.path.join(current_app.root_path, 'static/profile_pic', picture_fn)

    output_size = (256, 256)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(image_path)

    with current_app.open_resource(image_path) as f:        
            profile_pic = base64.b64encode(f.read()).decode('utf-8')

    return profile_pic


def resize_image(string_picture):
    image = base64.b64decode(string_picture)
    filename = 'account.jpg'

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(filename)
    picture_fn = random_hex + f_ext
    image_path  = os.path.join(current_app.root_path, 'static/profile_pic', picture_fn)

    output_size = (256, 256)
    i = Image.open(io.BytesIO(image))
    i.thumbnail(output_size)
    i.save(image_path)
    
    with current_app.open_resource(image_path) as f:        
            profile_pic = base64.b64encode(f.read()).decode('utf-8')

    return profile_pic


def send_email(clerk):
    token = clerk.get_token()
    msg = Message('Requisição de redefinição de senha', sender=current_app.config['FLASKY_MAIL_SENDER'],
                  recipients=[clerk.email])
    msg.body = f''' Para redefinir sua senha, visite o seguinte endereço: {url_for('reset_token', token=token,
                                                                                   _external=True)}
            Se você não fez esta requisição então ignore este email e mudança alguma será feita.
    '''
    mail.send(msg)
