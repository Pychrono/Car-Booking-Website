from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, PostForm
from . import db
import json
from .models import UserForm, User, Cars
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 1:
        return render_template("admin.html", user=current_user)
    else:
        flash("Sorry you must be an Admin to Access this page")
        return redirect(url_for('dashboard'))

    
@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id= current_user.id
    name_to_update = User.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.full_name = request.form['full_name']
        name_to_update.email = request.form['email']
        name_to_update.age = request.form['age']
        name_to_update.user_name = request.form['user_name']
        try:
            db.session.commit()
            flash("User Updated Successfully!!")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error! Looks like there was a problem updating ur profile")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("dashboard.html", form=form, name_to_update=name_to_update, id= id)
    return render_template("dashboard.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/rental', methods=[ 'POST', 'GET'])
def rental():
        
    #Grab all the posts from the form
    rental = Cars.query.order_by(Cars.date_posted)
    return render_template("rental.html", rental= rental)

@views.route('/history', methods=[ 'POST', 'GET'])
def history():
    rented = Cars.query.order_by(Cars.date_posted)
    if request.method == 'POST':
        rented = request.form.get('note')
    
    return render_template('history.html', rented=rented)

@views.route('/create_car', methods=[ 'POST', 'GET'])
def create_car():
    form = PostForm()
    if form.validate_on_submit():
        car = Cars(brand=form.brand.data, name=form.name.data, color=form.color.data, location=form.location.data)
        # Clear the form
        form.brand.data = ''
        form.name.data = ''
        form.color.data = ''
        form.location.data = ''
        
        # Add post data to database
        db.session.add(car)
        db.session.commit()
        
        flash("New Car Added")
    return render_template("create_car.html", form=form)