from flask import Blueprint, jsonify, request, render_template
from app import db
from app.models.hosts import Host
from app.get_routing import  get_host_bgp
import logging

get = Blueprint("get", __name__)


@get.route("/host/<host>", methods=["GET"])
def get_host(host):
    try:
        host = db.session.query(Host.name, Host.hostname, Host.status).filter_by(name=host).first()
        print(host.name)
        try:
            result =  get_host_bgp(host.name)
            
            print(result[host.name].result)
            # Add drop down to show details - multihop, remove_private_as, bits in/out, flaps etc
            #bgp_details = (result[host.name].result.result["get_bgp_neighbors_detail"])
            #print(result[host.name].result)
            result = result[host.name].result.result["get_bgp_neighbors"]
        except:
            result = {"Error" : "Device unreachable"}
        return render_template('host.html', host=host, result=result)
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
