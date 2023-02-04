
# with app.app_context():
#     db.create_all()






from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)









@app.route("/")
def list_users():
    """List users and show create users form."""

    users = User.query.all()
    return render_template("list.html", users=users)






@app.route("/add_user", methods=["POST"])
def add_user():
    """Add user and redirect to list."""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    
    db.session.add(user)
    db.session.commit()

    return redirect(f"/user/{user.id}")







@app.route("/user/<int:user_id>")
def show_user(user_id):

    user = User.query.get(user_id)

    if (user.posts):
        posts = Post.query.get(user_id)
        if (posts.post_2_tag):
            post_id = posts.id
            post_tags = PostTag.query.get(post_id)

            return render_template("details.html", user=user, posts=posts, post_tags=post_tags)

        return render_template("details.html", user=user, posts=posts)    
    else:
        return render_template("details.html", user=user)










@app.route("/user_edit/<int:user_id>", methods=['GET'])
def edit_user_page(user_id):
    """Edit a User's Details"""

    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)







@app.route("/user_edit/<int:user_id>/editing", methods=['POST'])
def edit_user(user_id):
    """Edit a User's Details"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']


    User.query.get(user_id).first_name=first_name
    User.query.get(user_id).last_name=last_name
    User.query.get(user_id).image_url=image_url


    db.session.commit()


    return redirect("/")









@app.route("/user_delete/<int:user_id>", methods=['GET', 'DELETE'])
def delete_user(user_id):
    """Delete a User"""


    # if (User.query.get(user_id).tags):
    #     for tag in (User.query.get(user_id).tags):
    #         Tag.query.filter_by(id=tag.id).delete()
    #         db.session.commit()


    # if (User.query.get(user_id).posts):       
    #     for post in (User.query.get(user_id).posts):
    #         Post.query.filter_by(id=post.id).delete()
    #         db.session.commit()


    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')








@app.route("/add_post/<int:user_id>", methods=['GET'])
def going_to_post(user_id):

    user = User.query.get_or_404(user_id)
    return render_template("post_form.html", user=user)







@app.route("/add_post/<int:user_id>/posting", methods=['POST'])
def posting(user_id):

    user = User.query.get_or_404(user_id)
    
    new_post = Post(title=request.form['title'], content=request.form['content'], user=user)
    
    
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/user/{user_id}")







@app.route("/posting/<int:post_id>")
def add_post(post_id):

    post = Post.query.get_or_404(post_id)

    user = User.query.get_or_404(post.user_id)


    return render_template("show_post.html", post=post, user=user)






@app.route('/delete/<int:post_id>')
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    if (post.post_2_tag):
        for tag in (post.post_2_tag):
            db.session.delete(tag)
            db.session.commit()

    user_id = post.user_id

    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    
    return redirect(f"/user/{user_id}")
   






@app.route('/edit_post/<int:post_id>', methods=['GET'])
def edit_post(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template('edit_post.html', post=post)








@app.route("/post_edit/<int:post_id>/editing", methods=['GET','POST'])
def editing_post(post_id):


    titles = request.form['title']
    contents = request.form['content']

    Post.query.get(post_id).title=titles
    Post.query.get(post_id).content=contents

    user_id = Post.query.get(post_id).user_id

    db.session.commit()


    return redirect(f"/user/{user_id}")







# Adding tag methods below.
# Not changing/touching anything besides below.







@app.route("/add_tag/<int:user_id>/<int:post_id>", methods=['GET'])
def adding_tag(user_id, post_id):

    user = User.query.get_or_404(user_id)

    post = Post.query.get_or_404(post_id)

    return render_template('create_tag.html', user=user, post=post)











@app.route("/add_tag/<int:user_id>/<int:post_id>/adding_tag", methods=['GET', 'POST'])
def added_tag(user_id, post_id):


    user = User.query.get_or_404(user_id)

    post = Post.query.get_or_404(post_id)

    new_tag = Tag(tag_name=request.form['tag'], user=user)


    db.session.add(new_tag)
    db.session.commit()
    

    new_post_tag = PostTag(post_id=post.id, tag_id=new_tag.id)  
    
    db.session.add(new_post_tag)   
    db.session.commit()


    return redirect(f'/user/{user_id}')








@app.route("/list_tag/<int:user_id>", methods=["GET"])
def list_tags(user_id):


    user = User.query.get(user_id)

    return render_template('list_tags.html', user=user)






# @app.route("/show_tag/<int:tag_id>", methods=["GET"])
# def list_tags(tag_id):





