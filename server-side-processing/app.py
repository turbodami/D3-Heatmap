from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
import os 
from process import processData
from process2 import processData2

# Init app
app = Flask(__name__, static_url_path='', static_folder='client/build', template_folder='client/build')
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# App class/model
class App(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(100), unique=True)
    company_url = db.Column(db.Text(100))
    release_date = db.Column(db.DateTime)
    genre_id = db.Column(db.Integer)
    artwork_large_url = db.Column(db.Text(100))
    seller_name = db.Column(db.Text(100))
    five_star_ratings = db.Column(db.Integer)
    four_star_ratings = db.Column(db.Integer)
    three_star_ratings = db.Column(db.Integer)
    two_star_ratings = db.Column(db.Integer)
    one_star_ratings = db.Column(db.Integer)
    
    def __init__(self, name, company_url, release_date, genre_id, artwork_large_url, seller_name, five_star_ratings, four_star_ratings, three_star_ratings, two_star_ratings, one_star_ratings):
        self.name = name
        self.company_url = company_url
        self.release_date = release_date
        self.genre_id = genre_id
        self.artwork_large_url = artwork_large_url
        self.seller_name = seller_name
        self.five_star_ratings = five_star_ratings
        self.four_star_ratings = four_star_ratings
        self.three_star_ratings = three_star_ratings
        self.two_star_ratings = two_star_ratings
        self.one_star_ratings = one_star_ratings 

# SDK class/model
class SDK(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(100), unique=True)
    slug = db.Column(db.Text(100))
    url = db.Column(db.Text(200))
    description = db.Column(db.Text(300))
   
    def __init__(self, name, slug, url, description):
        self.name = name
        self.slug = slug
        self.url = url
        self.description = description

# App/SDK class/model
class App_SDK(db.Model):
    app_id = db.Column(db.Integer, nullable=False, primary_key=True)
    sdk_id = db.Column(db.Integer, nullable=False, primary_key=True)
    installed = db.Column(db.Boolean, nullable=False)

    def __init__(self, installed):
        self.installed = installed

# App schema
class AppSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'company_url', 'release_date', 'genre_id', 'artwork_large_url', 'seller_name', 'five_star_ratings', 'four_star_ratings', 'three_star_ratings', 'two_star_ratings', 'one_star_ratings')

# SDK schema
class SDKSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'slug', 'url', 'description')

# App/SDK schema
class App_SDKSchema(ma.Schema):
    class Meta:
        fields = ('app_id', 'sdk_id', 'installed')

# Init app schema
app_schema = AppSchema()
apps_schema = AppSchema(many=True)

# Init sdk schema
sdk_schema = SDKSchema()
sdks_schema = SDKSchema(many=True)

# Init app/sdk schema
app_sdk_schema = App_SDKSchema()
app_sdks_schema = App_SDKSchema(many=True)

# Get home
@app.route('/')
def hello():
    return render_template('index.html')

# Get all app table
@app.route('/app', methods=['GET'])
def get_app():
    all_app = App.query.all()
    result = apps_schema.dump(all_app)
    return jsonify(result)

# Get all sdk table
@app.route('/sdk', methods=['GET'])
def get_sdk():
    all_sdk = SDK.query.all()
    result = sdks_schema.dump(all_sdk)
    return jsonify(result)

# Get all app_sdk table
@app.route('/appsdk', methods=['GET'])
def get_app_sdk():
    all_app_sdk = App_SDK.query.all()
    result = app_sdks_schema.dump(all_app_sdk)
    return jsonify(result)

# Produce dataset
@app.route('/process', methods=['POST'])
def get_dataset():
    all_sdk = SDK.query.all()
    result_all_sdk = sdks_schema.dump(all_sdk)
    all_app_sdk = App_SDK.query.all()
    result_all_app_sdk = app_sdks_schema.dump(all_app_sdk)
    
    selectedSDKs = request.json['selectedSDKs']
    selectedSDKs = list(filter(None, selectedSDKs))
   
    #result = processData(result_all_sdk, selectedSDKs, result_all_app_sdk)
    result = processData2(result_all_sdk, result_all_app_sdk, selectedSDKs)

    return jsonify(result)

# Run server
if __name__ == '__main__':
    app.run(debug=True)

