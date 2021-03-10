from flask import Flask,render_template,request,url_for,redirect
import data
from authlib.integrations.flask_client import OAuth

app = Flask(__name__ )

oauth = OAuth(app)

app.config['SECRET_KEY'] = "THIS SHOULD BE SECRET"
app.config['GOOGLE_CLIENT_ID'] = "293203167323-halo1ohjl1aaefome9dbi8jlqvoovgkp.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "p4oGl-vFB4ZjWzukY3UrlrBo"
# app.config['GITHUB_CLIENT_ID'] = "<your github client id>"
# app.config['GITHUB_CLIENT_SECRET'] = "<your github client secret>"

google = oauth.register(
    name = 'google',
    client_id = app.config["GOOGLE_CLIENT_ID"],
    client_secret = app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs = {'scope': 'openid email profile'},
)


@app.route('/')
def index():
      return render_template('index.html')
@app.route('/login/google')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


# Google authorize route
@app.route('/login/google/authorize',methods=["GET","POST"])
def google_authorize(): 
        google = oauth.create_client('google')
        token = google.authorize_access_token()
        resp = google.get('userinfo').json()
        print(f"\n{resp}\n")
        res = data.writes(resp)
        print(res)
        return redirect(url_for('crowdengine'))

@app.route('/crowdengine/')
def crowdengine():
    return render_template('mainpage.html',movie_list = data.mlglist)



@app.route('/crowdengine/<string:name>')
def movie_name(name):
    
    if name not in data.mlglist:
        return render_template('error.html',error="Name Not Found")
    return render_template('movies.html' ,name = name,actor ="vadivelu")

@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html',error='Problem occured')

@app.errorhandler(404)
def page_not_found(e):
    
    return render_template('error.html',error='Page Not found')

@app.route('/crowdengine/pre/')
def pre():
    name = request.args.get('page')
    index = data.mlglist.index(name)
    name = data.page('pre',index)
    return redirect(url_for('movie_name',name = name) )
    
   

@app.route('/crowdengine/next/')
def next():
    name = request.args.get('page')
    index = data.mlglist.index(name)
    name = data.page('next',index)
    return redirect(url_for('movie_name',name = name))

@app.route('/crowdengine/write/',methods=["POST"])   
def write_db():
    
    if request.method == 'POST':
        
        topic=request.form["topic"]
        dur = request.form["Addcontent"]
        color = request.form["Tags"]
        hair = request.form["Levels"]
        print(topic, dur, color, hair)
        data.write(topic=topic,content=dur,tags=color,levels=hair)

    return render_template('movies.html',p="ok" ,name=topic)

@app.route('/download/')
def download():
    return data.get_csv(a = app)

@app.route('/index.html')
def logout():
    
    return redirect(url_for('index.html'))


if __name__ == "__main__":
    app.run(port="5002"),