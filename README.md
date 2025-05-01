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

- **Request Type:** `PUT`  
- **Purpose:** Register a new user account.

#### Request Body:
- `username` (String): The desired username.  
- `password` (String): The desired password.

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

### Route: `/login`

- **Request Type:** `POST`  
- **Purpose:** Authenticate a user and log them in

#### Request Body:
- `username` (String): the username of the user.  
- `password` (String): the password of the user.

#### Response Format: JSON

**Success Response Example:**
- **Code:** `200`  
- **Content:**
```json
{
  "message": "User 'newuser123' logged in successfully",
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
- **Code:** `401`  
- **Content:**
```json
{
  "message": "Invalid username or password",
  "status": "error"
} 
```
- **Code:** `401`  
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
  "message": "An internal error occurred during login",
  "status": "error"
} 
```
#### Example Request:
- username: newuser123
- password: securepassword
#### Example Response:
- message: User 'newuser123' logged in successfully
- status: 200

### Route: `/logout`

- **Request Type:** `POST`  
- **Purpose:** Log out the current user.

#### Response Format: JSON

**Success Response Example:**
- **Code:** `200`  
- **Content:**
```json
{
  "message": "User logged out successfully",
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
- **Code:** `401`  
- **Content:**
```json
{
  "message": "Invalid username or password",
  "status": "error"
} 
```
- **Code:** `401`  
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
  "message": "An internal error occurred during login",
  "status": "error"
} 
```






