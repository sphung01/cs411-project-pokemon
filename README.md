# cs411-project

# Routes Documentation

### Route: `/create-user`

- **Request Type:** `POST`  
- **Purpose:** Creates a new user account with a username and password.

#### Request Body:
- `username` (String): User's chosen username.  
- `password` (String): User's chosen password.

#### Response Format: JSON

**Success Response Example:**
- **Code:** `200`  
- **Content:**
```json
{
  "message": "Account created successfully",
  "status": "200"
} 
```

