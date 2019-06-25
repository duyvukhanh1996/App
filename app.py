import os
import smtplib
from flask import Flask, render_template, request, redirect, url_for, session
from db import insert_experience, get_all_experience, get_experience_by_name, get_all_users, insert_users, insert_image, get_all_images, get_image_by_owner, delete_image_by_id
app = Flask(__name__)
app.secret_key = "abcxyz00"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', data=get_all_experience(), gallery=get_all_images(), logged_in=True, user=session['username'])
    return render_template('index.html', data=get_all_experience(), gallery=get_all_images(), logged_in=False)


@app.route('/', methods=['POST'])
def sign():
    data_users = get_all_users()
    data = get_all_experience()
    logged_in = False
    if 'signin_username' in request.form:
        signin_username = request.form.get('signin_username')
        signin_password = request.form.get('signin_password')
        for user in data_users:
            if user['username'] == signin_username and user['password'] == signin_password:
                session['username'] = signin_username
                return render_template('index.html', signin_username=signin_username, logged_in=True, data=data, gallery=get_all_images(), user=session['username'])
        return render_template('index.html', signin_username=signin_username, logged_in=False, data=data, gallery=get_all_images(), user=session['username'])
    elif 'signup_username' in request.form:
        signup_username = request.form.get('signup_username')
        signup_password = request.form.get('signup_password')
        message = "Signup completed"
        for user in data_users:
            if signup_username == user['username']:
                message = "Username already exists"
                return render_template('sign_up_noti.html', message=message, logged_in=logged_in, gallery=get_all_images())
        if len(signup_username) < 6 or len(signup_username) > 15 or len(signup_password) < 6 or len(signup_password) > 15:
            message = "Username or password not available"
            return render_template('sign_up_noti.html', message=message, logged_in=logged_in, gallery=get_all_images())
        insert_users(signup_username, signup_password)
        return render_template('sign_up_noti.html', message=message, logged_in=logged_in, gallery=get_all_images())
    else:
        gmail_user = 'duyvukhanhc4e@gmail.com'
        gmail_password = 'vukhanhduy'
        sent_from = gmail_user
        to = request.form.get('email_to_send')
        subject = 'Thank you for subscribing'
        body = 'Thank you for subscribing viet-traveling'

        email_text = """\  
        From: %s  
        To: %s  
        Subject: %s

        %s
        """ % (sent_from, to, subject, body)
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, email_text)
            server.close()
            return render_template('sub_noti.html',message = "Thanks for subscribing")
        except:  
            return render_template('sub_noti.html',message = "Opps!! Some things went wrong!")


@app.route('/logout')
def sign_out():
    del session['username']
    return redirect(url_for('sign'))


@app.route('/gallery')
def gallery():
    x = len(get_all_images()) // 4
    if 'username' in session:
        return render_template('gallery_page.html', logged_in=True, gallery=get_all_images(), x=x, y=len(get_all_images()), user=session['username'])
    return render_template('gallery_page.html', logged_in=False, gallery=get_all_images(), x=x, y=len(get_all_images()))


@app.route('/experience/<a>')
def experience(a):
    page_number = int(a)
    data = get_all_experience()
    max_page_number = len(data)//5 + 1
    du = len(data) % 5
    logged_in = False
    if 'username' in session:
        logged_in = True
        if page_number == max_page_number and du != 0:
            return render_template('experience.html', data=data, page_number=page_number, x=5-du, logged_in=logged_in, user=session['username'], max_page_number=max_page_number)
        return render_template('experience.html', data=data, page_number=page_number, x=0, logged_in=logged_in, user=session['username'], max_page_number=max_page_number)
    else:
        if page_number == max_page_number and du != 0:
            return render_template('experience.html', data=data, page_number=page_number, x=5-du, logged_in=logged_in, max_page_number=max_page_number)
        return render_template('experience.html', data=data, page_number=page_number, x=0, logged_in=logged_in, max_page_number=max_page_number)


@app.route('/post/<name>')
def post(name):
    data = get_experience_by_name(name)
    logged_in = False
    if 'username' in session:
        logged_in = True
        return render_template('apost.html', data=data, logged_in=logged_in, user=session['username'])
    return render_template('apost.html', data=data, logged_in=logged_in)


@app.route('/experience/post/<name>')
def experience_post(name):
    logged_in = False
    if 'username' in session:
        logged_in = True
    return redirect(url_for("post", name=name, logged_in=logged_in))


@app.route('/upload')
def upload_get():
    logged_in = False
    if 'username' in session:
        logged_in = True
        return render_template('upload.html', logged_in=logged_in, user=session['username'])
    return render_template('sign_in_required.html', logged_in=logged_in)


@app.route('/upload', methods=['POST'])
def upload():
    logged_in = False
    if "username" in session:
        logged_in = True
        target = os.path.join(APP_ROOT, 'static/' +
                              'images/' + session["username"])
        print(target)
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist('file'):
            print(file)
            filename = file.filename
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)
            link = "../../static/images/" + \
                session["username"] + "/" + filename
            insert_image(session["username"], link)
        return render_template('uploaded.html', logged_in=logged_in)
    return render_template('sign_in_required.html', logged_in=logged_in)


@app.route('/<username>/gallery')
def user_gallery(username):
    x = len(get_image_by_owner(username)) // 4
    if "username" in session:
        return render_template('gallery_page_owner.html', logged_in=True, gallery=get_image_by_owner(username), x=x, y=len(get_image_by_owner(username)), user=session['username'],owner = username)
    return render_template('gallery_page_owner.html', logged_in=False, gallery=get_image_by_owner(username), x=x, y=len(get_image_by_owner(username)), user = None)


@app.route('/deleted/<image_id>')
def delete_image(image_id):
    delete_image_by_id(image_id)
    return redirect(url_for('user_gallery', username=session['username']))


@app.route('/admin')
def admin():
    if 'username' in session:
        if session['username'] == 'admin123':
            return render_template('admin.html', logged_in=True)
    return render_template('admin_required.html', logged_in=True)


@app.route('/admin', methods=['POST'])
def admin1():
    number_of_p = request.form.get('number_of_p')
    return redirect(url_for('admin2', number_of_p=number_of_p))


@app.route('/admin_post/<number_of_p>')
def admin2(number_of_p):
    if 'username' in session:
        if session['username'] == 'admin123':
            return render_template('admin_post.html', number_of_p=int(number_of_p), logged_in=True)
    return render_template('admin_required.html', logged_in=True)


@app.route('/admin_post/<number_of_p>', methods=['POST'])
def admin3(number_of_p):
    p_list = ["p1", "p2", "p3", "p4", "p5", "p6"]
    content = {}
    name = request.form.get('name')
    for i in range(int(number_of_p)):
        key = p_list[i]
        content.update({key: request.form.get(p_list[i])})
    youtube_embed_link = request.form.get('youtube_embed_link')
    picture_link = request.form.get('picture_link')
    insert_experience(name, content, youtube_embed_link, picture_link)
    return render_template('inserted_post_noti.html', logged_in=True)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
