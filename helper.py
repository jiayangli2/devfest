def populate(session, user):
    session['username'] = user.username
    session['fullname'] = user.fullname
    session['phone'] = user.phoen
    session['email'] = user.email
