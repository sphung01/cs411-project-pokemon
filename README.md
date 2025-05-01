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
  "message": "Account created successfully",
  "status": "success"
} 
```



