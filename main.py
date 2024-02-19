from flask import Flask, render_template, redirect
from data import db_session
from data.users import User, Jobs
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    data_users = db_sess.query(User.id, User.email, User.name, User.surname, User.age, User.speciality).all()
    return render_template('index.html', all=data_users)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    db_session.global_init("db/blogs.db")
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        elif int(form.age.data) < 0:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Возраст не может быть отрицательным")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
