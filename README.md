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

🧾 Schema Overview
Artwork Object
json
Copy
Edit
{
  "artworkId": 2023001,
  "title": "Tears!",
  "completionDate": "2002-01-28",
  "color": "blue",
  "medium": "Oil in Canvas",
  "dimensions": "120cm x 100cm",
  "category": "painting",
  "era": "Medieval",
  "location": "Louvre Museum, Paris",
  "image": "https://example.com/artwork.jpg",
  "price": "$100",
  "previousOwners": "Leonardo de Capricorn",
  "artistBirthdate": "1853-01-30",
  "provenance": true
}
User Object
json
Copy
Edit
{
  "username": "theUser",
  "firstName": "John",
  "lastName": "James",
  "email": "doe@email.com",
  "password": "12345",
  "phone": "12345",
  "userStatus": "online"
}
