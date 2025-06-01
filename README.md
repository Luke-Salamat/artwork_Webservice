🎨 Artwork Information API
The Artwork Information API is a standardized and secure interface that allows authorized businesses to retrieve, create, update, and manage artwork and user data. It supports features such as artwork filtering by various attributes, user registration, and authentication.

🔐 Authentication
API Key: Sent in the api_key header.

OAuth2 (Implicit Flow): Authorization via https://artInf.com/oauth/authorize with scopes:

read:artwork

write:artwork

read:user

write:user

🔧 Main Endpoints
📚 Artworks
Method	Endpoint	Description
GET	/artwork	Retrieve artwork list using filters like artworkId, color, era, artist.
POST	/artwork/addArtwork	Add a new artwork.
PUT	/artwork/updateArtwork	Update an existing artwork.
DELETE	/artwork/{artworkId}	Delete an artwork by ID.

👤 Users
Method	Endpoint	Description
POST	/user/register	Register a new user.
POST	/user/login	Log in a user with credentials.
PUT	/user/edit	Update an existing user's details.
DELETE	/user/delete{username}	Delete a user by their username.

