from flask import Blueprint, jsonify, request, render_template
from app import db
from app.models.hosts import Host, Group, Host_to_Group
from app.get_routing import  get_host_bgp
import logging
from app.forms import AddHost, AddGroup
from datetime import datetime

post = Blueprint("post", __name__)


@post.route("/add_host", methods=["GET", "POST"])
def add_host():
    try:
        form = AddHost()
        all_groups = Group.query.all()
        form.group.choices = [(g.id, g.name) for g in all_groups]
        if request.method == "POST":
            host = Host.query.filter_by(name=form.name.data).first()
            if host:
                return jsonify({'message': 'host already exists.'})
            new_host = Host(name=form.name.data, hostname=form.hostname.data, status=form.status.data)
            db.session.add(new_host)
            #group = Group.query.filter_by(id=form.group.data).first()
            group = Group.query.filter_by(id=form.group.data).first()
            print(form.group.data)
            print(group)
            # Add Host to Group Association
            ## TO DO: Add a check to see if already associated
            association = Host_to_Group(added=datetime.utcnow())
            association.group = group
            association.host = new_host
            #new_host.host_relationship.append(association)
            db.session.commit()
            id = db.session.query(Host.id).filter(
                    Host.name == form.name.data).first()
            idInt = str(id).replace('(', '').replace(',', '').replace(')', '')
            return "Great success new host added with ID: {}".format(idInt)

        else:
            #host = db.session.query(Host.name, Host.hostname, Host.status).first()
            return render_template('add_host.html', form=form)
    except Exception as e:
        return f"Error {e} on /add_host"
    

@post.route("/add_group", methods=["GET", "POST"])
def add_group():
    try:
        form = AddGroup()
        if request.method == "POST":
            print("test")
            group = Group.query.filter_by(name=form.name.data).first()
            if group:
                return jsonify({'message': 'group already exists.'})
            new_group = Group(name=form.name.data, platform=form.platform.data)
            db.session.add(new_group)
            db.session.commit()
            id = db.session.query(Group.id).filter(
                    Group.name == form.name.data).first()
            idInt = str(id).replace('(', '').replace(',', '').replace(')', '')
            return "Great success new Group added with ID: {}".format(idInt)

        else:
            #host = db.session.query(Host.name, Host.hostname, Host.status).first()
            return render_template('add_group.html', form=form)
    except Exception as e:
        return f"Error {e} on /add_group"