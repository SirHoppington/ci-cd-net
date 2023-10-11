
from app import db


class Host(db.Model):
    __tablename__ = 'hosts'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable=False)
    hostname = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(128), nullable=False)
    host_relationship = db.relationship("Host_to_Group", back_populates="host")

    def __repr__(self):
        return '<hostname {}>'.format(self.hostname)


class Host_to_Group(db.Model):
    __tablename__ = 'host_to_group'
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key=True)
    host = db.relationship('Host', back_populates='host_relationship')
    group = db.relationship('Group', back_populates='group_relationship')
    
    def __repr__(self):
        return f"host {self.host_id} to group {self.group_id}"


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable=False)
    platform = db.Column(db.String(128), nullable=False)
    group_relationship = db.relationship("Host_to_Group", back_populates="group")

    def __repr__(self):
        return '<name {}>'.format(self.name)

