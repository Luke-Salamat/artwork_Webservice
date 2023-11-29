from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ars.db'
db = SQLAlchemy(app)


class ArtworkModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    artistOrigin = db.Column(db.String(100))
    provenance = db.Column(db.String(100))
    medium = db.Column(db.String(100))
    category = db.Column(db.String(50))
    completionDate = db.Column(db.String(50))
    era = db.Column(db.String(50))
    color = db.Column(db.String(50))
    dimensions = db.Column(db.String(50))
    location = db.Column(db.String(50))
    image = db.Column(db.String(50))
    highestValue = db.Column(db.String(50))
    
# remove this comment to create local database
# with app.app_context():
#     db.create_all()

post_artwork = reqparse.RequestParser()
post_artwork.add_argument("title", type=str, help="title required", required=True)
post_artwork.add_argument("color", type=str, help="color required", required=True)
post_artwork.add_argument("medium", type=str, help="medium required", required=True)
post_artwork.add_argument("era", type=str, help="era required", required=True)

put_artwork = reqparse.RequestParser()
put_artwork.add_argument("title", type=str)
put_artwork.add_argument("color", type=str)
put_artwork.add_argument("medium", type=str)
put_artwork.add_argument("era", type=str)

resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'artist': fields.String,
    'artistOrigin': fields.String,
    'provenance': fields.String,
    'medium': fields.String,
    'category': fields.String,
    'completionDate': fields.String,
    'era': fields.String,
    'color': fields.String,
    'dimensions': fields.String,
    'location': fields.String,
    'image': fields.String,
    'highestValue': fields.String,

}

class postArtwork(Resource):   
    @marshal_with(resource_fields)
    def post(self, art_id):
        args = post_artwork.parse_args()
        artExist = ArtworkModel.query.filter_by(id=art_id).first()
        if artExist:
            abort(409, message="Artwork id taken")
        newArt = ArtworkModel(id=art_id, title=args['title'], artist=args['artist'], artistOrigin=args['artistOrigin'], provenance=args['provenance'], medium=args['medium'], category=args['category'], completionDate=args['completionDate'], era=args['era'], color=args['color'], dimensions=args['dimensions'], location=args['location'], image=args['image'], highestValue=args['highestValue'])
        db.session.add(newArt)
        db.session.commit()
        return newArt, 201

     
class artworkList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        collections = ArtworkModel.query.all()
        artworks = {}
        for artwork in collections:
            artworks[artwork.id] = {'title': artwork.title, 'artist': artwork.artist, 'artistOrigin': artwork.artistOrigin, 'provenance': artwork.provenance, 'medium': artwork.medium, 'category': artwork.category, 'completionDate': artwork.completionDate, 'era': artwork.era, 'color': artwork.color, 'dimensions': artwork.dimensions, 'location': artwork.location, 'image': artwork.image, 'highestValue': artwork.highestValue}
        return artworks    
            
            
class getArtwork(Resource):
    @marshal_with(resource_fields)
    def get(self):
        art_id = request.args.get('id')
        title = request.args.get('title')
        era = request.args.get('era')
        color = request.args.get('color')   
    
        if art_id and title and era and color:
            collections = ArtworkModel.query.all()
            artworks = {}
            for artwork in collections:
                artworks[artwork.id] = {'title': artwork.title, 'artist': artwork.artist, 'artistOrigin': artwork.artistOrigin, 'provenance': artwork.provenance, 'medium': artwork.medium, 'category': artwork.category, 'completionDate': artwork.completionDate, 'era': artwork.era, 'color': artwork.color, 'dimensions': artwork.dimensions, 'location': artwork.location, 'image': artwork.image, 'highestValue': artwork.highestValue}
            return artworks

        if not art_id and not title and not era and not color:
            abort(400, message="Provide either art_id or title")

        if art_id:
            artwork = ArtworkModel.query.get(art_id)
            if not artwork:
                abort(404, message="Artwork id doesn't exist")
            return artwork,200
       

        if title:
            artwork = ArtworkModel.query.filter_by(title=title).first()
            if not artwork:
                abort(404, message="Artwork title doesn't exist")
            return artwork, 200
        
        if era:
            artwork = ArtworkModel.query.filter_by(era=era).first()
            if not artwork:
                abort(404, message="Artwork era doesn't exist")
            return artwork, 200
        
        if color:
            artwork = ArtworkModel.query.filter_by(color=color).first()
            if not artwork:
                abort(404, message="Artwork era doesn't exist")
            return artwork, 200

class putArtwork(Resource):
    @marshal_with(resource_fields)
    def put(self, art_id):
        artwork = ArtworkModel.query.get(art_id)
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
        if 'category' in update_data:
            artwork.category = update_data['category']        
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
        if 'highestValue' in update_data:
            artwork.highestValue = update_data['highestValue']
        db.session.commit()
        return artwork, 200


class deleteArtwork(Resource):
    def delete(self, art_id):
        artExist = ArtworkModel.query.get(art_id)
        if not artExist:
            abort(409, message="Artwork id does not exist, cannot delete")
        db.session.delete(artExist)
        db.session.commit()
        return "Artwork deleted", 201



api.add_resource(deleteArtwork, '/artwork/<int:art_id>')
api.add_resource(postArtwork, '/artwork/<int:art_id>')
api.add_resource(putArtwork, '/artwork/<int:art_id>')
api.add_resource(getArtwork, '/artwork')
api.add_resource(artworkList, '/artwork/list')



if __name__ == '__main__':
    app.run(debug=True)
