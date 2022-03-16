
import os
from flask_wtf import FlaskForm
from flask import Flask, render_template, redirect, url_for, make_response, jsonify, request, session
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from model import checkAccount

class FakeFriend(FlaskForm):
    username = StringField('Username', render_kw={"placeholder": "Username"})
    fullname = StringField('Full Name', render_kw={"placeholder": "Full Name"})
    description = StringField('Description', render_kw={"placeholder": "Description"})
    private = BooleanField('It is private profile')
    profilepic = BooleanField('It has profile picture')
    externalurl = BooleanField('It has external URL')
    followers = IntegerField('Number of Followers', render_kw={"placeholder": "Number of Followers"})
    follows = IntegerField('Number of Follows', render_kw={"placeholder": "Number of Follows"})
    posts = IntegerField('Number of Posts', render_kw={"placeholder": "Number of Posts"})
    check = SubmitField('Check!')

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=['GET', 'POST'])
def index():
    form = FakeFriend()
    if request.method == "POST":
        username = form.username.data
        fullname = form.fullname.data
        description = form.description.data
        private = form.private.data
        profilepic = form.profilepic.data
        externalurl = form.externalurl.data
        followers = form.followers.data
        follows = form.follows.data
        posts = form.posts.data
        picture = 0
        isNameEquals = 0
        hasExtUrl = 0
        isPrivate = 0
        if profilepic:
            picture = 1
        nums_username = getCountOfDegits(username)
        nums_fullname = getCountOfDegits(fullname)
        if len(username) != 0:
            nums_username = nums_username / len(username)
        else:
            nums_username = 0
        if len(fullname) != 0:
            nums_fullname = nums_fullname / len(fullname)
        else:
            nums_fullname = 0

        if fullname == username:
            isNameEquals = 1
        if externalurl:
            hasExtUrl = 1
        if private:
            isPrivate = 1
        if posts == None:
            posts = 0
        if followers == None:
            followers = 0
        if follows == None:
            follows = 0
        data = [[picture, nums_username, len(fullname), nums_fullname, isNameEquals, len(description), hasExtUrl, isPrivate, posts, followers, follows]]
        result = checkAccount(data)
        message = "Input data was incorrect"
        if result == 0:
            message = "Not fake account"
        elif result == 1:
            message = "Fake account"
        return redirect(url_for('index', message=message))
    return render_template('index.html', form=form)


def getCountOfDegits(s):
    count = 0
    for i in range(len(s)):
        if '0' <= s[i] <= '9':
            count = count + 1
    return count


if __name__ == '__main__':
    app.run(debug=True)

