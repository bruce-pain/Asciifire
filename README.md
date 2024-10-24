# Asciifire

Asciifire is a web application that converts images into ASCII art. Users can upload images, convert them to ASCII art, and display the results in a gallery. It features user authentication, the ability to categorize images using tags, and a ranking system for ASCII art.

## Features

- **Image to ASCII Art Conversion:** Upload an image and generate its ASCII art version.
- **Multiple Image Conversion:** Users can upload and convert multiple images.
- **Gallery:** View all generated ASCII art images in a public gallery.
- **Export ASCII to Image:** Convert ASCII art back to an image format.
- **Authentication:** Only registered users can save their ASCII art to the gallery.
- **Tagging System:** Categorize images with tags for easy filtering in the gallery.

## Technology Stack

- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **Task Queue:** Celery with RabbitMQ
- **Authentication:** JWT-based authentication
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Deployment:** Docker, Docker Compose

---

## Usage

### 1. Register a User

To register a new user, send a `POST` request to `/auth/register` with the following payload:

```json
{   "username": "your_username",   "password": "your_password" }
```

### 2. Upload an Image for ASCII Conversion

Once registered, authenticate and send a `POST` request to `/images/upload` with the image file.

### 3. View Gallery

Visit the gallery of ASCII art at `/gallery`.

---

## API Endpoints

### Authentication

- `POST /auth/register`: Register a new user.
- `POST /auth/login`: Log in and receive a JWT token.

### Image Conversion

- `POST /images/upload`: Upload an image for ASCII conversion.
- `GET /gallery`: View all generated ASCII art in the gallery.

### Tags

- `POST /tags`: Create a new tag.
- `GET /tags`: List all tags.

### Votes

- `POST /images/{image_id}/vote`: Upvote or downvote an image.

---

## Database Schema

### User

|Field|Type|Description|
|---|---|---|
|`id`|UUID|Unique identifier for the user|
|`username`|String|User’s username|
|`password_hash`|String|Securely hashed password|
|`created_at`|Timestamp|When the user was created|
|`updated_at`|Timestamp|Last time the user was updated|

### Image

|Field|Type|Description|
|---|---|---|
|`id`|UUID|Unique identifier for the image|
|`user_id`|UUID|Foreign key linking to the user|
|`ascii_art`|Text|Generated ASCII art|
|`created_at`|Timestamp|When the image was created|
|`updated_at`|Timestamp|Last time the image was updated|

### Tag

|Field|Type|Description|
|---|---|---|
|`id`|UUID|Unique identifier for the tag|
|`name`|String|Tag name (e.g., "landscape")|

---

## Future Enhancements

- **Social Sharing:** Allow users to share ASCII art on social media platforms.
- **Image Filters:** Add support for image filters before ASCII conversion.
- **Commenting:** Let users leave comments on ASCII art.
- **Mobile App:** Develop a mobile version of the Asciifire app.

---

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License.

