# Stories API Documentation

## Base URL
The API base URL follows the format: `/api/v1`

## Authentication
Most endpoints require authentication using a Bearer token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

Public endpoints that don't require authentication:
- POST /api/v1/auth/login
- POST /api/v1/auth/register
- GET /docs
- GET /redoc
- GET /api/v1/openapi.json
- GET /

## Authentication Endpoints

### Register User
**Endpoint:** `POST /api/v1/auth/register`  
**Authentication Required:** No

**Request Body:**
```json
{
    "email": "string",
    "username": "string",
    "password": "string"
}
```

**Response:** `200 OK`
```json
{
    "id": "uuid",
    "email": "string",
    "username": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

**Error Responses:**
- `400 Bad Request`: Email or username already registered

### Login
**Endpoint:** `POST /api/v1/auth/login`  
**Authentication Required:** No

**Request Body:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Response:** `200 OK`
```json
{
    "access_token": "string",
    "token_type": "bearer"
}
```

### Check Session
**Endpoint:** `GET /api/v1/auth/check-session`  
**Authentication Required:** Yes

**Response:** `200 OK`
```json
{
    "id": "uuid",
    "email": "string",
    "username": "string",
    "fullname": "string",
    "bio": "string",
    "birthday": "date",
    "profile_picture": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing authentication token

## User Endpoints

### Update Profile
**Endpoint:** `PUT /api/v1/users/me`  
**Authentication Required:** Yes

**Request Body:**
```json
{
    "fullname": "string (optional)",
    "bio": "string (optional)",
    "birthday": "date (optional)",
    "profile_picture": "string (optional)"
}
```

**Response:** `200 OK`
```json
{
    "id": "uuid",
    "username": "string",
    "email": "string",
    "fullname": "string",
    "bio": "string",
    "birthday": "date",
    "profile_picture": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### Get Current User Profile
**Endpoint:** `GET /api/v1/users/me`  
**Authentication Required:** Yes

**Response:** `200 OK`
```json
{
    "id": "uuid",
    "username": "string",
    "email": "string",
    "fullname": "string",
    "bio": "string",
    "birthday": "date",
    "profile_picture": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### Get User Profile
**Endpoint:** `GET /api/v1/users/{user_id}`  
**Authentication Required:** Yes

**Response:** `200 OK`
```json
{
    "id": "uuid",
    "username": "string",
    "fullname": "string",
    "bio": "string",
    "profile_picture": "string"
}
```

### Follow User
**Endpoint:** `POST /api/v1/users/{user_id}/follow`  
**Authentication Required:** Yes

**Response:** `200 OK`
```json
{
    "id": "uuid",
    "username": "string",
    "fullname": "string",
    "bio": "string",
    "profile_picture": "string"
}
```

**Error Responses:**
- `400 Bad Request`: Cannot follow yourself
- `400 Bad Request`: Already following this user
- `404 Not Found`: User not found

### Get Followers
**Endpoint:** `GET /api/v1/users/me/followers`  
**Authentication Required:** Yes

**Response:** `200 OK`
```json
[
    {
        "id": "uuid",
        "username": "string",
        "fullname": "string",
        "bio": "string",
        "profile_picture": "string"
    }
]
```

### Get Following
**Endpoint:** `GET /api/v1/users/me/following`  
**Authentication Required:** Yes

**Response:** `200 OK`
```json
[
    {
        "id": "uuid",
        "username": "string",
        "fullname": "string",
        "bio": "string",
        "profile_picture": "string"
    }
]
```

## Stories Endpoints

### Create Story
**Endpoint:** `POST /api/v1/stories`  
**Authentication Required:** Yes

**Request Body (multipart/form-data):**
- `media_file`: File (required)
- `caption`: string (optional)

**Response:** `200 OK`
```json
{
    "id": "uuid",
    "media_url": "string",
    "caption": "string",
    "user_id": "uuid",
    "likes_count": 0,
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

**Error Responses:**
- `500 Internal Server Error`: Failed to upload media

### Get Stories Feed
**Endpoint:** `GET /api/v1/stories`  
**Authentication Required:** Yes

**Query Parameters:**
- `skip`: integer (default: 0)
- `limit`: integer (default: 100)

**Response:** `200 OK`
```json
[
    {
        "id": "uuid",
        "media_url": "string",
        "caption": "string",
        "user_id": "uuid",
        "likes_count": integer,
        "created_at": "datetime",
        "updated_at": "datetime"
    }
]
```

### Get My Stories
**Endpoint:** `GET /api/v1/stories/me`  
**Authentication Required:** Yes

**Response:** `200 OK`
```json
[
    {
        "id": "uuid",
        "media_url": "string",
        "caption": "string",
        "user_id": "uuid",
        "likes_count": integer,
        "created_at": "datetime",
        "updated_at": "datetime"
    }
]
```

### Get Story by ID
**Endpoint:** `GET /api/v1/stories/{story_id}`  
**Authentication Required:** Yes

**Response:** `200 OK`
```json
{
    "id": "uuid",
    "media_url": "string",
    "caption": "string",
    "user_id": "uuid",
    "likes_count": integer,
    "seen_by": [
        {
            "id": "uuid",
            "username": "string",
            "fullname": "string"
        }
    ],
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

**Error Responses:**
- `404 Not Found`: Story not found

### Like Story
**Endpoint:** `POST /api/v1/stories/{story_id}/like`  
**Authentication Required:** Yes

**Response:** `200 OK`
```json
{
    "id": "uuid",
    "media_url": "string",
    "caption": "string",
    "user_id": "uuid",
    "likes_count": integer,
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

**Error Responses:**
- `400 Bad Request`: Already liked this story
- `404 Not Found`: Story not found

### Unlike Story
**Endpoint:** `DELETE /api/v1/stories/{story_id}/unlike`  
**Authentication Required:** Yes

**Response:** `200 OK`
```json
{
    "id": "uuid",
    "media_url": "string",
    "caption": "string",
    "user_id": "uuid",
    "likes_count": integer,
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

**Error Responses:**
- `400 Bad Request`: Not liked this story
- `404 Not Found`: Story not found

### Mark Story as Seen
**Endpoint:** `POST /api/v1/stories/{story_id}/seen`  
**Authentication Required:** Yes

**Response:** `200 OK`
```json
{
    "id": "uuid",
    "media_url": "string",
    "caption": "string",
    "user_id": "uuid",
    "likes_count": integer,
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

**Error Responses:**
- `404 Not Found`: Story not found 