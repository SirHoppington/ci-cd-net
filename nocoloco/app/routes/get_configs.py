from flask import Blueprint, jsonify, request, render_template
from app import db
from app.models.hosts import Host
from app.get_routing import  get_host
import logging

get = Blueprint("get", __name__)


@get.route("/host/<host>", methods=["GET"])
def get_host(host):
    try:
        host = db.session.query(Host.name, Host.hostname, Host.status).first()
        result =  get_host(host.name)
        return render_template('host.html', host=host)
    except Exception as e:
        return f"Error {e} on /cids"

@get.route("/hosts", methods=["GET"])
def get_hosts():
    try:
        hosts = db.session.query(Host).all()
        json = [f"{hosts}"]
        return jsonify(json), 200
    except Exception as e:
        return f"Error {e} on /cids"