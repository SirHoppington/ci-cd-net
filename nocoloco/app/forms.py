from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

class AddHost(FlaskForm):
    """Add new host form."""
    name = StringField(
        'Name',
        [DataRequired()],
        id='name'
    )
    hostname = StringField(
        'Hostname',
        [DataRequired()],
        id='hostname'
    )

    group = SelectField(
        'Group',
        coerce=int
    )

    status = StringField(
        'status',
        id='status'
    )

class AddGroup(FlaskForm):
    """Add new group form."""
    name = StringField(
        'Name',
        [DataRequired()],
        id='name'
    )
    platform = StringField(
        'Platform',
        [DataRequired()],
        id='platform'
    )