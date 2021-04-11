"""Server for KP Depression Class."""
from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import connect_to_db, db, User
import crud
import os
import sys
from jinja2 import StrictUndefined
import os
import json

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_homepage():
    """View homepage"""

    return render_template('login.html')



@app.route('/login', methods=['POST'])
def user_login_post():
    """take user login info and make yummy cookies"""

    email = request.form.get('email')
    password = request.form.get('password')
    name = crud.get_users_name(email)
    
    email_check = crud.check_if_in_system(email)
    if email_check:
        return render_template('automatic_thought.html')
    else:
        return render_template('login.html')

@app.route('/user_registration_route')
def user_reg_route():
    """route to user_registration"""

    return render_template('signup.html')

@app.route('/user_signup', methods=['POST'])
def user_reg_post_intake():
    """take user registration info and make yummy cookies"""

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    email_check = crud.check_if_in_system(email)
    if password == "":
        flash("You must enter in a password.")
        return redirect('/user_registration_route')

    if name == "":
        flash("You must enter in your name.")
        return redirect('/user_registration_route')


    if email_check:
        if email != "":
            flash("A user already exists with that email.  Please try a different email")
        else:
            flash("You must enter in an email address.")
        return redirect('user_registration_route')
    else:
        create_user = crud.create_user(email, name, password)
        flash("Please log in.")
        return render_template('login.html', create_user=create_user,name=name,email=email)


    if not email_check:
        register_user = crud.register_user(email,name)
        return render_template('automatic_thought.html', register_user=register_user,name=name,email=email)
    else:
        return render_template('login.html')

   
@app.route('/automatic_thought', methods=['POST'])
def automatic_thought():
    """take user input for automatic thought"""  
   
    automatic_thought = request.form.get('automaticThought')   

    session['automatic_thought'] = automatic_thought
    print('this is the automatic thought in session',automatic_thought)

    return render_template('distortion.html', automatic_thought=automatic_thought)


@app.route('/distortion', methods=['POST'])
def distortion():
    """take user input for distortion analysis"""  
    
    distortion = request.form.getlist('distortionsList')
    distortion_plot = len(distortion)

    session['distortion'] = distortion
    session['distortion_plot'] = distortion_plot
    
    
    return render_template('moreRealisticThought.html',distortion=json.dumps(distortion), distortion_plot=json.dumps(distortion_plot))


@app.route('/moreRealisticThought', methods=['POST'])
def more_realistic_thought():
    """take user input for more realistic thought"""    

    email = session['email']
    more_realistic_thought = request.form.get('moreRealisticThought')
    print(more_realistic_thought)

    distortion = session['distortion']
    distortion_plot = session['distortion_plot']

    automatic_thought = session['automatic_thought']

    thought = crud.add_thought(email, automatic_thought, distortion, distortion_plot, more_realistic_thought)
    session['thought'] = thought
    return render_template('graph.html', thought = thought)    


@app.route('/graph')
def show_graph():
    """View graph"""

    email = session['email']
    plot_dict = crud.get_plot_points_for_all_thoughts(email)

    session['plot_dict'] = plot_dict

    return render_template('graph.html', plot_dict = plot_dict)


if __name__ == '__main__':
    connect_to_db(app)
    
    app.run(host='0.0.0.0', debug=True, use_reloader=True)