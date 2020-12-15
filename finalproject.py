# from flask import Flask, render_template, flash, redirect
# from flask_bootstrap import Bootstrap
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired
# from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap(app)

filter_choice= ['Sepia', 'Negative', 'Grayscale', 'Thumbnail', 'None']

class manipulation(FlaskForm):
    user_selection = StringField('Choose a filter: ', validators=[DataRequired()])
    # user_selection.lower()


def filter_selection(filter_choice):
    img = Image.open(f'static/images/user_image.jpg') #this is a placeholder
    filter_choice = filter_choice.lower()
    if filter_choice== 'sepia':
        def sepia(pixel):
            if pixel[0] < 63:
                r,g,b = int(pixel[0]*1.1), pixel[1], int(pixel[2]*.9)
            elif pixel[0]>62 and pixel[0]<192:
                r,g,b = int(pixel[0]*1.15), pixel[1], int(pixel[2]*.85)
            else:
                r = int(pixel[0]*1.08)
                if r>255: r=255
                g,b = pixel[1], pixel[2]//2  
            return r,g,b
        sepia_list = map(sepia, img.getdata())
        img.putdata(list(sepia_list))
    elif filter_choice == 'negative':
        negative_list = [(255-p[0], 255-p[1], 255-p[2]) 
                            for p in img.getdata()]
        img.putdata(negative_list)
    elif filter_choice == 'grayscale':
        new_list = [ ( (a[0]+a[1]+a[2])//3, ) * 3 
                for a in img.getdata() ]

        img.putdata(new_list)
    elif filter_choice == 'thumbnail':
        source = img

        w,h = source.width, source.height

        target = Image.new('RGB', (w, h), 'rosybrown')

        target_x = 0
        for source_x in range(0, source.width, 2):
            target_y = 0
            for source_y in range(0, source.height, 2):
                pixel = source.getpixel((source_x, source_y))
                target.putpixel((target_x, target_y), pixel)
                target_y += 1
            target_x += 1
        img = target

    
    img = img.save('new_photo.jpg')


    return render_template('imagedisplay.html', user_image = img)

@app.route('/', methods=('GET','POST'))
def main_page():
    form = manipulation()
    if form.validate_on_submit():
        filter_selection(form.user_selection.data)
        return redirect('/results')

    return render_template('imageupload.html', form = form)


@app.route('/results', methods=('GET', 'POST'))
def results():
    return render_template('imagedisplay.html')