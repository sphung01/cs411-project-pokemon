# cs411-project

# Routes Documentation

### Route: `/api/health`

- **Request Type:** `GET`  
- **Purpose:** Verifies that the service is up and running.

#### Request Body:
_None_

#### Response Format: JSON

**Success Response Example:**
- **Code:** `200`  
- **Content:**
```json
{
  "status": "success",
  "message": "Service is running"
}
```

### Route: `/create-user`

- **Request Type:** `POST`  
- **Purpose:** Creates a new user account with a username and password.

#### Request Body:
- `username` (String): User's chosen username.  
- `password` (String): User's chosen password.

#### Response Format: JSON

**Success Response Example:**
- **Code:** `201`  
- **Content:**
```json
{
  "message": "User 'username123' created successfully",
  "status": "success"
} 
```

**Error Response Example:**
- **Code:** `400`  
- **Content:**
```json
{
  "message": "Username and password are required",
  "status": "error"
} 
```
- **Code:** `400`  
- **Content:**
```json
{
  "message": "error string",
  "status": "error"
} 
```
- **Code:** `500`  
- **Content:**
```json
{
  "message": "An internal error occurred while creating users",
  "status": "error",
  "details": "error string"
} 
```
#### Example Request:
- username: newuser123
- password: securepassword
#### Example Response:
- message: User 'username123' created successfully
- status: 200






