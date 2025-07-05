# Django Chat Application

A full-featured real-time chat application built with Django, supporting both web and mobile platforms through a hybrid architecture of REST APIs and traditional web views.

## Features

### Core Functionality
- **Real-time Messaging**: WebSocket-powered instant messaging
- **Private Chats**: One-on-one conversations between users
- **Group Chats**: Multi-user group conversations with admin controls
- **File Sharing**: Send and receive files in conversations

- **Online Status**: 
- **Last Seen**: Track when users were last active
- **User Search**: Find and connect with other users
- **Group Join Codes**: Join groups using unique invitation codes

### Technical Features
- **Hybrid Architecture**: REST APIs for mobile apps + Django templates for web
- **Dual Authentication**: JWT tokens for API endpoints + Django sessions for web views
- **WebSocket Support**: Real-time message delivery and status updates
- **Message Persistence**: All messages stored in database

## Installation

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/django-chat-app.git
   cd chat-application
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```


4. **Create superuser**
   ```bash
   cd mychat
   python manage.py createsuperuser
   ```

5. **Run the application**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/token/` | Obtain JWT token pair |
| POST | `/api/token/refresh/` | Refresh JWT token |

### User Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/user/register/` | User registration |
| POST | `/user/login/` | User login |
| POST | `/user/logout/` | User logout |

### Chat Operations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/chat/` | List all private chats |
| POST | `/chat/` | Create new private chat |
| GET | `/chat/<int:chat_id>` | Get messages for specific chat |
| GET | `/group/` | List all group chats |
| POST | `/group/` | Create new group chat |
| GET | `/group/<int:chat_id>` | Get messages for specific group |

### Additional Features
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/search/` | Search users by username |
| POST | `/group-join/` | Join group using invite code |

## Web Pages

### Template Views (Session-based Authentication)
| URL | View | Description |
|-----|------|-------------|
| `/` | Redirect to home | Root redirect |
| `/home/` | Home page | Main dashboard |
| `/chat-web/<int:chat_id>` | Chat interface | Web-based chat UI |
| `/user/register/` | Registration page | User signup form |
| `/user/login/` | Login page | User signin form |

## Authentication Architecture

### Dual Authentication System
- **REST APIs**: JWT-based authentication for mobile apps and API consumers
- **Web Views**: Django session-based authentication for template-rendered pages

### JWT Implementation
```python
POST /api/token/          
POST /api/token/refresh/  

# API requests require Authorization header
Authorization: Bearer <access_token>
```


## API Response Examples

### Get Private Chats
```json
GET /chat/
[
{
  "id": 1,
  "username": "john_doe",
  "lastMessage": "Hello there!",
  "unread": 2,
  "time": "2024-01-15T10:30:00Z"
},
]
```

### Get Messages
```json
GET /chat/1
{
  "id": 1,
  "chatname": "john_doe",
  "messages": [
    {
      "sender": 2,
      "sendername": "jane_smith",
      "time": "2024-01-15T10:30:00Z",
      "text": "Hello there!",
      "read": true,
      "read_by": {
        "john_doe": "2024-01-15T10:31:00Z"
      }
    }
  ],
  "myid": 1,
  "is_online": true,
  "lastseen": "2024-01-15T10:32:00Z"
}
```

### Create Group Chat
```json
POST /group/
{
  "name": "Project Team",
  "members": ["user1", "user2", "user3"]
}
```

## WebSocket Integration

### WebSocket URLs
```python
ws/chat/<int:chat_id>/    # Chat messages WebSocket
ws/file/<int:chat_id>/    # File upload WebSocket
```

### Real-time Features
- **Instant Messaging**: Messages delivered immediately via WebSocket
- **Online Status**: presence tracking (online/offline)
- **Last Seen**: Track when users disconnect
- **Message Persistence**: All messages saved to database
- **File Upload Support**: Real-time file transfer via WebSocket



### Message Format
```javascript
{
    'type': 'message',
    'chat_id': 1,
    'sender': 1,
    'sender_username':'s'
    'text': 'Hello World!',
    'time': '2025-07-04T01:11:52.800Z',
    'read': false,
    'read_by': []
}
```

### WebSocket Consumer Features
- **Authentication Check**: Only authenticated users can connect
- **Automatic Online Status**: Users marked online on connection and offline by closing
- **Database Integration**: Messages automatically saved to database




## File Sharing

### Supported Features
- **File Upload**: Send files through chat interface only if other user is online as diles are not saved to database

## Development

### Key Models
- **Chat**: Represents chat rooms (private/group)
- **Group_pep**: Extended group chat functionality
- **User**: Extended Django user model with extending profile
