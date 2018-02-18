def populate(session, user):
    session['username'] = user.username
    session['fullname'] = user.fullname
    session['phone'] = user.phone
    session['email'] = user.email
