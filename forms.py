from wtforms import Form, StringField, TextAreaField, PasswordField, validators

# registreation form
class RegisterForm(Form):
    name = StringField('', [validators.Length(min=1, max=50)],render_kw={"placeholder": "Name"})
    username = StringField('', [validators.Length(min=4, max=50)],render_kw={"placeholder": "Username"})
    email = StringField('', [validators.Length(min=4, max=100)],render_kw={"placeholder": "Email"})
    
    password = PasswordField('', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password does not match')
    ],render_kw={"placeholder": "Password"})
    confirm = PasswordField('',render_kw={"placeholder": "Confirm Password"})

class ArticleForm(Form):
    title = StringField('', [validators.Length(min=1, max=50)],render_kw={"placeholder": "Title"})
    body = StringField('', [validators.Length(min=10)],render_kw={"placeholder": "Article Content"})
