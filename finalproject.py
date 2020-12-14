from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap(app)


filter_choice= ['Sepia', 'Negative', 'Grayscale', 'Thumbnail', 'None']

class manipulation(FlaskForm):
    user_selection = StringField('Choose a filter: ', validators=[DataRequired()])

@app.route('/', methods=('GET','POST'))
def main_page():
    form = manipulation()
    if form.validate_on_submit():

        # def image_data(image_id):
        #     for i in image_info:
        #             img = Image.open(f'images/user_image.jpg') #placeholder
        #             mode = img.mode
        #             myformat = img.format
        #             width = img.width
        #             height = img.height
        #             break
            
            # return render_template('project.html', image = img, img_mode = mode, img_myformat = myformat, img_width = width, img_height = height, myimage_info = image_info)
    #the finalproject.html is a placeholder until I know the actual name of the file.
        def filter_selection():
            img = Image.open(f'images/user_image.jpg') #this is a placeholder
            # filter_choice = ['Sepia', 'Negative', 'Grayscale', 'Thumbnail', 'None']
            if filter_choice == 'Sepia':

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
            elif filter_choice == 'Negative':
                negative_list = [(255-p[0], 255-p[1], 255-p[2]) 
                                    for p in img.getdata()]

                            img.putdata(negative_list)
            elif filter_choice == 'Grayscale':
                new_list = [ ( (a[0]+a[1]+a[2])//3, ) * 3 
                        for a in img.getdata() ]

                img.putdata(new_list)
            elif filter_choice == 'Thumbnail':
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
        
        return render_template('imageuploadtest.html', image = img, user_selection = user_selection)

    return render_template('imageupload.html', form = form)

    # img.show()


win = MyWindow()
win.show()
app.exec_()
