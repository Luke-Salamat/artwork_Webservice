from flask import Flask, redirect, render_template, request, url_for
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("database")
app.config['SECRET_KEY'] = os.getenv("secretkey")
db = SQLAlchemy(app)




class ArtworkModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    title = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    artistOrigin = db.Column(db.String(100))
    provenance = db.Column(db.String(5))
    medium = db.Column(db.String(100))
    completionDate = db.Column(db.String(50))
    era = db.Column(db.String(50))
    color = db.Column(db.String(50))
    dimensions = db.Column(db.String(50))
    location = db.Column(db.String(50))
    image = db.Column(db.String(50))
    startingbid = db.Column(db.String(50))
    
    
    
# # remove this comment to create local database
# with app.app_context():
#     db.create_all()

resource_fields = {
    'id': fields.Integer,
    'category': fields.String,
    'title': fields.String,
    'artist': fields.String,
    'artistOrigin': fields.String,
    'provenance': fields.String,
    'medium': fields.String,
    'completionDate': fields.String,
    'era': fields.String,
    'color': fields.String,
    'dimensions': fields.String,
    'location': fields.String,
    'image': fields.String,
    'startingbid': fields.String,
}



post_artwork = reqparse.RequestParser()
post_artwork.add_argument("title", type=str, help="title required", required=True)
post_artwork.add_argument("category", type=str, help="category required", required=True)
post_artwork.add_argument("artist", type=str, help="artist required", required=True)
post_artwork.add_argument("artistOrigin", type=str, help="artistOrigin required", required=True)
post_artwork.add_argument("provenance", type=str, help="provenance required", required=True)
post_artwork.add_argument("medium", type=str, help="medium required", required=True)
post_artwork.add_argument("completionDate", type=str, help="completionDate required", required=True)
post_artwork.add_argument("era", type=str, help="era required", required=True)
post_artwork.add_argument("medium", type=str, help="medium required", required=True)
post_artwork.add_argument("color", type=str, help="color required", required=True)
post_artwork.add_argument("dimensions", type=str, help="dimensions required", required=True)
post_artwork.add_argument("location", type=str, help="location required", required=True)
post_artwork.add_argument("image", type=str, help="image required", required=True)
post_artwork.add_argument("startingbid", type=str, help="value required", required=True)

put_artwork = reqparse.RequestParser()
put_artwork.add_argument("title", type=str, help="title required", required=True)
put_artwork.add_argument("title", type=str, help="category required", required=True)
put_artwork.add_argument("artist", type=str, help="artist required", required=True)
put_artwork.add_argument("artistOrigin", type=str, help="artistOrigin required", required=True)
put_artwork.add_argument("provenance", type=str, help="provenance required", required=True)
put_artwork.add_argument("medium", type=str, help="medium required", required=True)
put_artwork.add_argument("completionDate", type=str, help="completionDate required", required=True)
put_artwork.add_argument("era", type=str, help="era required", required=True)
put_artwork.add_argument("medium", type=str, help="medium required", required=True)
put_artwork.add_argument("color", type=str, help="color required", required=True)
put_artwork.add_argument("dimensions", type=str, help="dimensions required", required=True)
put_artwork.add_argument("location", type=str, help="location required", required=True)
put_artwork.add_argument("image", type=str, help="image required", required=True)
put_artwork.add_argument("startingbid", type=str, help="value required", required=True)



    

class postArtwork(Resource):   
    @marshal_with(resource_fields)
    def post(self, art_id):
        key = os.getenv('api_key')
        api_key = request.headers.get('Authorization')
        args = post_artwork.parse_args()
        artExist = ArtworkModel.query.filter_by(id=art_id).first()
        if api_key != key:
            abort(401, message="Invalid API key")
        else:
            if artExist:
                abort(409, message="Artwork id taken")
                
            if args['provenance'] not in ('true', 'false'):
                abort(400, message="Invalid provenance value") 
                
            if args['category'] not in ('painting', 'sculpture', 'drawing'):
                abort(400, message="Invalid category value")  
                
            if args['color'] not in ('warm', 'cool', 'complementary', 'mixed'):
                abort(400, message="Invalid color value")       
            newArt = ArtworkModel(id=art_id, category=args['category'], title=args['title'], artist=args['artist'], artistOrigin=args['artistOrigin'], provenance=args['provenance'], medium=args['medium'], completionDate=args['completionDate'], era=args['era'], color=args['color'], dimensions=args['dimensions'], location=args['location'], image=args['image'], startingbid=args['startingbid'])
            db.session.add(newArt)
            db.session.commit()
            return newArt, 201
                     
class getArtwork(Resource):
    @marshal_with(resource_fields)
    def get(self):
        key = os.getenv('api_key')
        api_key = request.headers.get('Authorization')
        art_id = request.args.get('id')
        artist = request.args.get('artist')
        era = request.args.get('era')
        color = request.args.get('color')
        category = request.args.get('category')

        if api_key != key:
            abort(401, message="Invalid API key")
        else:
            if art_id:
                artwork = ArtworkModel.query.get(art_id)
                if not artwork:
                    abort(404, message="Artwork id doesn't exist")
                return artwork,200
            elif category:
                artwork = ArtworkModel.query.filter_by(category=category).all()
                if not artwork:
                    abort(404, message="Artwork category doesn't exist")
                return artwork, 200
            elif artist:
                artwork = ArtworkModel.query.filter(ArtworkModel.artist.contains(artist)).all()
                if not artwork:
                    abort(404, message="Artwork artist doesn't exist")
                return artwork, 200
            elif era:
                artwork = ArtworkModel.query.filter(ArtworkModel.era.contains(era)).all()
                if not artwork:
                    abort(404, message="Artwork era doesn't exist")
                return artwork, 200
            elif color:
                artwork = ArtworkModel.query.filter(ArtworkModel.color.contains(color)).all()
                if not artwork:
                    abort(404, message="Artwork color doesn't exist")
                return artwork, 200
            else:
                collections = ArtworkModel.query.all()
                artworks = {}
                for artwork in collections:
                    artworks[artwork] = {"id": artwork.id, "title": artwork.title, "artist": artwork.artist, "artistOrigin": artwork.artistOrigin, "provenance": artwork.provenance, "medium": artwork.medium, "completionDate": artwork.completionDate, "era": artwork.era, "color": artwork.color, "dimensions": artwork.dimensions, "location": artwork.location, "image": artwork.image, "startingbid": artwork.startingbid}
                return collections
        
class putArtwork(Resource):
    @marshal_with(resource_fields)
    def put(self, art_id):
        key = os.getenv('api_key')
        api_key = request.headers.get('Authorization')
        artwork = ArtworkModel.query.get(art_id)
        if api_key != key:
            abort(401, message="Invalid API key")
        else:
            if not artwork:
                abort(404, message="Artwork with given id does not exist")
            
            update_data = request.json  
            if not update_data:
                abort(400, message="No update data provided")
    
            if 'title' in update_data:
                artwork.title = update_data['title']
            if 'artist' in update_data:
                artwork.artist = update_data['artist']
            if 'artistOrigin' in update_data:
                artwork.artistOrigin = update_data['artistOrigin']
            if 'provenance' in update_data:
                artwork.provenance = update_data['provenance']
            if 'medium' in update_data:
                artwork.medium = update_data['medium']    
            if 'completionDate' in update_data:
                artwork.comepletionDate = update_data['completionDate']
            if 'color' in update_data:
                artwork.color = update_data['color']
            if 'era' in update_data:
                artwork.era = update_data['era']
            if 'dimensions' in update_data:
                artwork.dimensions = update_data['dimensions']
            if 'location' in update_data:
                artwork.location = update_data['location']
            if 'image' in update_data:
                artwork.image = update_data['image']
            if 'startingbid' in update_data:
                artwork.startingbid = update_data['startingbid']
            db.session.commit()
            return artwork, 200


class deleteArtwork(Resource):
    def delete(self, art_id):
        key = os.getenv('api_key')
        api_key = request.headers.get('Authorization')
        artExist = ArtworkModel.query.get(art_id)
        if api_key != key:
            abort(401, message="Invalid API key")
        else:
            if not artExist:
                abort(409, message="Artwork id does not exist, cannot delete")
            db.session.delete(artExist)
            db.session.commit()
            return "Artwork deleted", 201



api.add_resource(deleteArtwork, '/artwork/<int:art_id>/')
api.add_resource(postArtwork, '/artwork/<int:art_id>')
api.add_resource(putArtwork, '/artwork/<int:art_id>')
api.add_resource(getArtwork, '/artwork')





if __name__ == '__main__':
    app.run(debug=True)
