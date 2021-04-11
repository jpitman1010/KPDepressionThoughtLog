"""Server operations. CRUD = create,read,update,delete"""

from model import User,db, Thoughts
from flask import flash, redirect, render_template
import smtplib, ssl


def create_user(email,name, password):
    """Create and return a new user."""

    user = User(email=email,name = name, password=password)
    
    db.session.add(user)
    db.session.commit()

    return user


def get_users_name(email):
    """get user's name for return users"""

    name = db.session.query(User.name).filter_by(email=email).first()
    
    return name[0]


def check_if_in_system(email):
    """Return whether an email has already registered"""

    user_exists_check = db.session.query(User).filter_by(email=email).first()
    
    return not not user_exists_check



def add_thought(email,automatic_thought, distortion, distortion_plot,more_realistic_thought):
    """Create and return a new thought."""
    user_email = db.session.query(User.email).filter_by(email = email).first()
    thought = Thoughts(user_email=user_email,automatic_thought=automatic_thought,distortion=distortion,distortion_plot=distortion_plot,more_realistic_thought=more_realistic_thought)

    db.session.add(thought)
    db.session.commit()

    return thought


def get_last_thought_id(email):
    """get id for most recent thought logged"""

    thought_id = db.session.query(Thoughts.id).filter_by(email=email).last()
    
    return thought_id[0]

def get_list_of_thought_id(email):
    """get id for all thoughts logged"""
    
    thought_id_list = db.session.query(Thoughts.id).filter_by(email=email).all()
    
    return thought_id_list

# def get_automatic_thought_plot(thought_id):
#     """get plot point for specific automatic thought using thought id"""

#     automatic_thought_plot = db.session.query(Thoughts.automatic_thought_plot).filter_by(id = thought_id)
    
#     return automatic_thought_plot

def get_distortion_thought_plot(thought_id):
    """get plot point for specific distortion thought using thought id"""

    distortion_plot = db.session.query(Thoughts.distortion_plot).filter_by(id = thought_id)
   
    return distortion_plot

# def get_more_realistic_thought_plot(thought_id):
#     """get plot point for specific more realistic thought using thought id"""

#     more_realistic_thought_plot = db.session.query(Thoughts.more_realistic_thought_plot).filter_by(id = thought_id)
    
#     return more_realistic_thought_plot


def get_automatic_thought(thought_id):
    """get thought for specific automatic thought using thought id"""

    automatic_thought = db.session.query(Thoughts.automatic_thought).filter_by(id = thought_id)
    
    return automatic_thought

def get_distortion_thought(thought_id):
    """get thought for specific distortion thought using thought id"""

    distortion = db.session.query(Thoughts.distortion).filter_by(id = thought_id)
    
    return distortion

def get_more_realistic_thought(thought_id):
    """get thought for specific more realistic thought using thought id"""

    more_realistic_thought = db.session.query(Thoughts.more_realistic_thought).filter_by(id = thought_id)
    
    return more_realistic_thought


# def get_plot_points_for_all_thoughts(email):
#     """get 3 plot points for each thought"""

#     plot_dict = {'automatic_thought': [],'distortion':[], 'more_realistic_thought':[] }

#     for id in get_list_of_thought_id(email):
        
#         plot_1 = get_automatic_thought_plot(id)
#         automatic_thought = get_automatic_thought(id)
#         plot_dict['automatic_thought'].append({plot_1, automatic_thought})

#         plot_2 = get_distortion_thought_plot(id)
#         distortion = get_distortion_thought(id)
#         plot_dict['distortion'].append({plot_2, distortion})

#         plot_3 = get_more_realistic_thought_plot(id)
#         more_realistic_thought = get_more_realistic_thought(id)
#         plot_dict['more_realistic_thought'].append({plot_3, more_realistic_thought})
    
#     return plot_dict


if __name__ == '__main__':
    from server import app
    connect_to_db(app)