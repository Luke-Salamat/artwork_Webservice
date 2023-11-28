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
    color = db.Column(db.String(50))
    medium = db.Column(db.String(100))
    era = db.Column(db.String(50))

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
    'color': fields.String,
    'medium': fields.String,
    'era': fields.String,

}
          
class artworkList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        collections = ArtworkModel.query.all()
        artworks = {}
        for artwork in collections:
            artworks[artwork.id] = {"title": artwork.title, "color": artwork.color, "medium": artwork.medium}
        return artworks    

        
            
            
class getArtwork(Resource):
    @marshal_with(resource_fields)
    def get(self):
        art_id = request.args.get('id')
        title = request.args.get('title')
        era = request.args.get('era')   
    
        if art_id and title and era:
            collections = ArtworkModel.query.all()
            artworks = {}
            for artwork in collections:
                artworks[artwork.id] = {"title": artwork.title, "color": artwork.color, "medium": artwork.medium}
            return artworks

        if not art_id and not title and not era:
            abort(400, message="Provide either art_id or title")

        if art_id:
            artwork = ArtworkModel.query.get(art_id)
            if not artwork:
                abort(404, message="Artwork id doesn't exist")
            return artwork
       
            

        if title:
            artwork = ArtworkModel.query.filter_by(title=title).first()
            if not artwork:
                abort(404, message="Artwork title doesn't exist")
            return artwork
        
        if era:
            artwork = ArtworkModel.query.filter_by(era=era).first()
            if not artwork:
                abort(404, message="Artwork era doesn't exist")
            return artwork
    
    
class postArtwork(Resource):   
    @marshal_with(resource_fields)
    def post(self, art_id):
        args = post_artwork.parse_args()
        artExist = ArtworkModel.query.filter_by(id=art_id).first()
        if artExist:
            abort(409, message="Artwork id taken")
        newArt = ArtworkModel(id=art_id, title=args['title'], color=args['color'], medium=args['medium'], era=args['era'])
        db.session.add(newArt)
        db.session.commit()
        return newArt, 201

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
        if 'color' in update_data:
            artwork.color = update_data['color']
        if 'medium' in update_data:
            artwork.medium = update_data['medium']
        if 'era' in update_data:
            artwork.era = update_data['era']
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
