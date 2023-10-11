from app.models.hosts import Host
from app import db

# Return all hosts
def get_all_hosts():
    subs = Host.query.all()
    return subs


# Return a specific host by name
def get_single_host(name):
    sub = db.session.query(Host).filter(Host.name == name).first()
    return sub


# Return a group of hosts