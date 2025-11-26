# 🔐 Authentication & Authorization - AI Cooking Assistant

Complete authentication and authorization system design using JWT, OAuth 2.0, and role-based access control (RBAC).

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Authentication Flow](#authentication-flow)
3. [JWT Token Strategy](#jwt-token-strategy)
4. [OAuth 2.0 Integration](#oauth-20-integration)
5. [Password Security](#password-security)
6. [Authorization & RBAC](#authorization--rbac)
7. [API Security](#api-security)
8. [Session Management](#session-management)
9. [Security Best Practices](#security-best-practices)
10. [Implementation Details](#implementation-details)

---

## 🎯 Overview

### Authentication Methods

1. **Email/Password** - Traditional registration and login
2. **OAuth 2.0** - Social login (Google, Facebook, Apple)
3. **JWT Tokens** - Stateless authentication
4. **Refresh Tokens** - Long-lived session management

### Security Goals

- ✅ Secure password storage (bcrypt with cost factor 12)
- ✅ Token-based stateless authentication
- ✅ OAuth 2.0 integration for social login
- ✅ Rate limiting and brute force protection
- ✅ CSRF protection for web clients
- ✅ XSS prevention
- ✅ Email verification
- ✅ Password reset flow
- ✅ Multi-device support
- ✅ Token revocation

---

## 🔄 Authentication Flow

### 1. Email/Password Registration

```
┌─────────┐                 ┌─────────┐                 ┌──────────┐
│  Client │                 │   API   │                 │ Database │
└────┬────┘                 └────┬────┘                 └────┬─────┘
     │                           │                           │
     │ POST /auth/register       │                           │
     │ {email, password, name}   │                           │
     ├──────────────────────────>│                           │
     │                           │                           │
     │                           │ Validate input            │
     │                           │ Check email unique        │
     │                           ├──────────────────────────>│
     │                           │<──────────────────────────┤
     │                           │ Email available           │
     │                           │                           │
     │                           │ Hash password (bcrypt)    │
     │                           │                           │
     │                           │ Create user               │
     │                           ├──────────────────────────>│
     │                           │<──────────────────────────┤
     │                           │ User created              │
     │                           │                           │
     │                           │ Generate verification     │
     │                           │ token                     │
     │                           │                           │
     │                           │ Send verification email   │
     │                           │                           │
     │<──────────────────────────┤                           │
     │ 201 Created               │                           │
     │ {user_id, email, ...}     │                           │
     │                           │                           │
```

### 2. Email/Password Login

```
┌─────────┐                 ┌─────────┐                 ┌──────────┐
│  Client │                 │   API   │                 │ Database │
└────┬────┘                 └────┬────┘                 └────┬─────┘
     │                           │                           │
     │ POST /auth/login          │                           │
     │ {email, password}         │                           │
     ├──────────────────────────>│                           │
     │                           │                           │
     │                           │ Find user by email        │
     │                           ├──────────────────────────>│
     │                           │<──────────────────────────┤
     │                           │ User found                │
     │                           │                           │
     │                           │ Verify password (bcrypt)  │
     │                           │                           │
     │                           │ Generate access token     │
     │                           │ (JWT, 1 hour expiry)      │
     │                           │                           │
     │                           │ Generate refresh token    │
     │                           │ (UUID, 30 days expiry)    │
     │                           │                           │
     │                           │ Store refresh token       │
     │                           ├──────────────────────────>│
     │                           │<──────────────────────────┤
     │                           │ Token stored              │
     │                           │                           │
     │                           │ Update last_login         │
     │                           ├──────────────────────────>│
     │                           │                           │
     │<──────────────────────────┤                           │
     │ 200 OK                    │                           │
     │ {access_token,            │                           │
     │  refresh_token,           │                           │
     │  expires_in,              │                           │
     │  user: {...}}             │                           │
     │                           │                           │
```

### 3. Token Refresh Flow

```
┌─────────┐                 ┌─────────┐                 ┌──────────┐
│  Client │                 │   API   │                 │ Database │
└────┬────┘                 └────┬────┘                 └────┬─────┘
     │                           │                           │
     │ POST /auth/refresh        │                           │
     │ {refresh_token}           │                           │
     ├──────────────────────────>│                           │
     │                           │                           │
     │                           │ Validate refresh token    │
     │                           ├──────────────────────────>│
     │                           │<──────────────────────────┤
     │                           │ Token valid & not expired │
     │                           │                           │
     │                           │ Generate new access token │
     │                           │ (JWT, 1 hour expiry)      │
     │                           │                           │
     │                           │ Generate new refresh token│
     │                           │ (UUID, 30 days expiry)    │
     │                           │                           │
     │                           │ Revoke old refresh token  │
     │                           ├──────────────────────────>│
     │                           │<──────────────────────────┤
     │                           │                           │
     │                           │ Store new refresh token   │
     │                           ├──────────────────────────>│
     │                           │                           │
     │<──────────────────────────┤                           │
     │ 200 OK                    │                           │
     │ {access_token,            │                           │
     │  refresh_token,           │                           │
     │  expires_in}              │                           │
     │                           │                           │
```

### 4. OAuth 2.0 Login (Google Example)

```
┌─────────┐     ┌─────────┐     ┌────────────┐     ┌──────────┐
│  Client │     │   API   │     │   Google   │     │ Database │
└────┬────┘     └────┬────┘     └──────┬─────┘     └────┬─────┘
     │               │                 │                 │
     │ Tap "Login    │                 │                 │
     │ with Google"  │                 │                 │
     │               │                 │                 │
     │ GET /auth/    │                 │                 │
     │ oauth/google  │                 │                 │
     ├──────────────>│                 │                 │
     │               │                 │                 │
     │<──────────────┤                 │                 │
     │ 302 Redirect  │                 │                 │
     │ to Google     │                 │                 │
     │               │                 │                 │
     │───────────────────────────────>│                 │
     │ Google Login  │                 │                 │
     │ Page          │                 │                 │
     │               │                 │                 │
     │<───────────────────────────────┤                 │
     │ User approves │                 │                 │
     │               │                 │                 │
     │───────────────────────────────>│                 │
     │ Authorization │                 │                 │
     │ code          │                 │                 │
     │               │                 │                 │
     │<───────────────────────────────┤                 │
     │ Redirect to   │                 │                 │
     │ callback URL  │                 │                 │
     │               │                 │                 │
     │ GET /auth/    │                 │                 │
     │ oauth/google/ │                 │                 │
     │ callback?code │                 │                 │
     ├──────────────>│                 │                 │
     │               │                 │                 │
     │               │ Exchange code   │                 │
     │               │ for access      │                 │
     │               │ token           │                 │
     │               ├────────────────>│                 │
     │               │<────────────────┤                 │
     │               │ Access token    │                 │
     │               │                 │                 │
     │               │ Get user info   │                 │
     │               ├────────────────>│                 │
     │               │<────────────────┤                 │
     │               │ User profile    │                 │
     │               │                 │                 │
     │               │ Find or create  │                 │
     │               │ user            │                 │
     │               ├─────────────────────────────────>│
     │               │<─────────────────────────────────┤
     │               │ User record     │                 │
     │               │                 │                 │
     │               │ Generate JWT    │                 │
     │               │ tokens          │                 │
     │               │                 │                 │
     │<──────────────┤                 │                 │
     │ 200 OK        │                 │                 │
     │ {tokens, user}│                 │                 │
     │               │                 │                 │
```

---

## 🎫 JWT Token Strategy

### Token Structure

**Access Token (JWT):**
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_id_uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user",
    "permissions": ["read:recipes", "write:own_recipes"],
    "exp": 1700000000,
    "iat": 1699996400,
    "jti": "unique_token_id"
  },
  "signature": "..."
}
```

**Refresh Token:**
- Simple UUID stored in database
- Associated with user_id, device_id, IP address
- 30-day expiry
- Can be revoked

### Token Configuration

```python
from datetime import timedelta

JWT_CONFIG = {
    # Access token settings
    "access_token": {
        "secret_key": "your-secret-key-min-32-chars",  # From env variable
        "algorithm": "HS256",
        "expiry": timedelta(hours=1),
        "issuer": "cooking-assistant-api",
        "audience": "cooking-assistant-app"
    },
    
    # Refresh token settings
    "refresh_token": {
        "expiry": timedelta(days=30),
        "max_active_tokens_per_user": 5  # Limit to 5 devices
    }
}
```

### Token Generation

```python
from datetime import datetime, timedelta
import jwt
import uuid
from typing import Dict

def generate_access_token(user: Dict) -> str:
    """Generate JWT access token"""
    now = datetime.utcnow()
    
    payload = {
        "sub": str(user['id']),
        "email": user['email'],
        "name": user['full_name'],
        "role": user['role'],
        "permissions": get_user_permissions(user['role']),
        "exp": now + JWT_CONFIG['access_token']['expiry'],
        "iat": now,
        "jti": str(uuid.uuid4()),
        "iss": JWT_CONFIG['access_token']['issuer'],
        "aud": JWT_CONFIG['access_token']['audience']
    }
    
    token = jwt.encode(
        payload,
        JWT_CONFIG['access_token']['secret_key'],
        algorithm=JWT_CONFIG['access_token']['algorithm']
    )
    
    return token

def generate_refresh_token(user_id: str, device_info: Dict) -> str:
    """Generate and store refresh token"""
    token = str(uuid.uuid4())
    
    # Store in database
    refresh_token_record = {
        "token": token,
        "user_id": user_id,
        "device_id": device_info.get('device_id'),
        "device_name": device_info.get('device_name'),
        "ip_address": device_info.get('ip_address'),
        "user_agent": device_info.get('user_agent'),
        "expires_at": datetime.utcnow() + JWT_CONFIG['refresh_token']['expiry'],
        "created_at": datetime.utcnow()
    }
    
    db.insert("refresh_tokens", refresh_token_record)
    
    return token
```

### Token Validation

```python
from fastapi import HTTPException, status
from jose import JWTError, jwt

def verify_access_token(token: str) -> Dict:
    """Verify and decode JWT access token"""
    try:
        payload = jwt.decode(
            token,
            JWT_CONFIG['access_token']['secret_key'],
            algorithms=[JWT_CONFIG['access_token']['algorithm']],
            issuer=JWT_CONFIG['access_token']['issuer'],
            audience=JWT_CONFIG['access_token']['audience']
        )
        
        # Check if token is expired
        exp = payload.get('exp')
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        
        return payload
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )

async def verify_refresh_token(token: str) -> Dict:
    """Verify refresh token from database"""
    record = await db.fetch_one(
        "SELECT * FROM refresh_tokens WHERE token = :token AND is_revoked = false",
        {"token": token}
    )
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    if record['expires_at'] < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired"
        )
    
    return dict(record)
```

### Token Revocation

```python
async def revoke_refresh_token(token: str):
    """Revoke a refresh token"""
    await db.execute(
        "UPDATE refresh_tokens SET is_revoked = true, revoked_at = :now WHERE token = :token",
        {"token": token, "now": datetime.utcnow()}
    )

async def revoke_all_user_tokens(user_id: str, except_token: str = None):
    """Revoke all refresh tokens for a user (e.g., on password change)"""
    query = """
        UPDATE refresh_tokens 
        SET is_revoked = true, revoked_at = :now 
        WHERE user_id = :user_id AND is_revoked = false
    """
    params = {"user_id": user_id, "now": datetime.utcnow()}
    
    if except_token:
        query += " AND token != :except_token"
        params["except_token"] = except_token
    
    await db.execute(query, params)
```

---

## 🌐 OAuth 2.0 Integration

### Supported Providers

1. **Google** - OAuth 2.0
2. **Facebook** - OAuth 2.0
3. **Apple** - Sign in with Apple

### OAuth Configuration

```python
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()

# Google OAuth
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Facebook OAuth
oauth.register(
    name='facebook',
    client_id=settings.FACEBOOK_APP_ID,
    client_secret=settings.FACEBOOK_APP_SECRET,
    authorize_url='https://www.facebook.com/v12.0/dialog/oauth',
    access_token_url='https://graph.facebook.com/v12.0/oauth/access_token',
    client_kwargs={
        'scope': 'email public_profile'
    }
)

# Apple Sign In
oauth.register(
    name='apple',
    client_id=settings.APPLE_CLIENT_ID,
    client_secret=settings.APPLE_CLIENT_SECRET,  # Generated JWT
    authorize_url='https://appleid.apple.com/auth/authorize',
    access_token_url='https://appleid.apple.com/auth/token',
    client_kwargs={
        'scope': 'name email'
    }
)
```

### OAuth Endpoints

```python
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/auth/oauth", tags=["OAuth"])

@router.get("/google")
async def google_login(request: Request):
    """Initiate Google OAuth flow"""
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request):
    """Handle Google OAuth callback"""
    try:
        # Exchange authorization code for access token
        token = await oauth.google.authorize_access_token(request)
        
        # Get user info from Google
        user_info = await oauth.google.parse_id_token(request, token)
        
        # Find or create user
        user = await find_or_create_oauth_user(
            provider='google',
            provider_user_id=user_info['sub'],
            email=user_info['email'],
            name=user_info.get('name'),
            avatar_url=user_info.get('picture')
        )
        
        # Generate JWT tokens
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user['id'], {
            'device_id': 'web',
            'ip_address': request.client.host,
            'user_agent': request.headers.get('user-agent')
        })
        
        # Redirect to app with tokens (or return JSON for mobile)
        if is_mobile_client(request):
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": 3600,
                "user": user
            }
        else:
            # Redirect to web app with tokens in URL
            return RedirectResponse(
                url=f"{settings.FRONTEND_URL}/auth/callback"
                    f"?access_token={access_token}"
                    f"&refresh_token={refresh_token}"
            )
    
    except Exception as e:
        logger.error(f"OAuth callback error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OAuth authentication failed"
        )

@router.get("/facebook")
async def facebook_login(request: Request):
    """Initiate Facebook OAuth flow"""
    redirect_uri = request.url_for('facebook_callback')
    return await oauth.facebook.authorize_redirect(request, redirect_uri)

@router.get("/facebook/callback")
async def facebook_callback(request: Request):
    """Handle Facebook OAuth callback"""
    # Similar to Google callback
    pass

@router.get("/apple")
async def apple_login(request: Request):
    """Initiate Apple Sign In flow"""
    redirect_uri = request.url_for('apple_callback')
    return await oauth.apple.authorize_redirect(request, redirect_uri)

@router.get("/apple/callback")
async def apple_callback(request: Request):
    """Handle Apple Sign In callback"""
    # Similar to Google callback
    pass
```

### Find or Create OAuth User

```python
async def find_or_create_oauth_user(
    provider: str,
    provider_user_id: str,
    email: str,
    name: str = None,
    avatar_url: str = None
) -> Dict:
    """Find existing user or create new one from OAuth provider"""
    
    # Check if user exists with this OAuth provider
    user = await db.fetch_one("""
        SELECT u.* FROM users u
        JOIN oauth_accounts oa ON u.id = oa.user_id
        WHERE oa.provider = :provider AND oa.provider_user_id = :provider_user_id
    """, {"provider": provider, "provider_user_id": provider_user_id})
    
    if user:
        # Update last login
        await db.execute(
            "UPDATE users SET last_login_at = :now WHERE id = :user_id",
            {"user_id": user['id'], "now": datetime.utcnow()}
        )
        return dict(user)
    
    # Check if user exists with this email
    user = await db.fetch_one(
        "SELECT * FROM users WHERE email = :email",
        {"email": email}
    )
    
    if user:
        # Link OAuth account to existing user
        await db.execute("""
            INSERT INTO oauth_accounts (user_id, provider, provider_user_id, created_at)
            VALUES (:user_id, :provider, :provider_user_id, :now)
        """, {
            "user_id": user['id'],
            "provider": provider,
            "provider_user_id": provider_user_id,
            "now": datetime.utcnow()
        })
        return dict(user)
    
    # Create new user
    user_id = uuid.uuid4()
    
    await db.execute("""
        INSERT INTO users (
            id, email, full_name, avatar_url, 
            email_verified, is_active, created_at, last_login_at
        ) VALUES (
            :id, :email, :name, :avatar_url,
            true, true, :now, :now
        )
    """, {
        "id": user_id,
        "email": email,
        "name": name,
        "avatar_url": avatar_url,
        "now": datetime.utcnow()
    })
    
    # Create OAuth account link
    await db.execute("""
        INSERT INTO oauth_accounts (user_id, provider, provider_user_id, created_at)
        VALUES (:user_id, :provider, :provider_user_id, :now)
    """, {
        "user_id": user_id,
        "provider": provider,
        "provider_user_id": provider_user_id,
        "now": datetime.utcnow()
    })
    
    # Fetch and return created user
    user = await db.fetch_one("SELECT * FROM users WHERE id = :id", {"id": user_id})
    return dict(user)
```

---

## 🔒 Password Security

### Password Hashing

```python
import bcrypt

def hash_password(password: str) -> str:
    """Hash password using bcrypt with cost factor 12"""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )
```

### Password Requirements

```python
import re
from typing import List

def validate_password(password: str) -> tuple[bool, List[str]]:
    """
    Validate password meets security requirements
    
    Requirements:
    - Minimum 8 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 digit
    - At least 1 special character
    """
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least 1 uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least 1 lowercase letter")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least 1 digit")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least 1 special character")
    
    return (len(errors) == 0, errors)
```

### Password Reset Flow

```python
import secrets
from datetime import datetime, timedelta

async def initiate_password_reset(email: str):
    """Initiate password reset process"""
    user = await db.fetch_one(
        "SELECT * FROM users WHERE email = :email",
        {"email": email}
    )
    
    if not user:
        # Don't reveal if email exists (security)
        return {"message": "If email exists, reset link has been sent"}
    
    # Generate reset token
    reset_token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=1)
    
    # Store reset token
    await db.execute("""
        INSERT INTO password_reset_tokens (user_id, token, expires_at, created_at)
        VALUES (:user_id, :token, :expires_at, :now)
    """, {
        "user_id": user['id'],
        "token": reset_token,
        "expires_at": expires_at,
        "now": datetime.utcnow()
    })
    
    # Send reset email
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
    await send_email(
        to=email,
        subject="Reset Your Password",
        template="password_reset",
        context={"reset_link": reset_link, "expires_in": "1 hour"}
    )
    
    return {"message": "If email exists, reset link has been sent"}

async def reset_password(token: str, new_password: str):
    """Reset password using token"""
    # Validate password
    is_valid, errors = validate_password(new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": errors}
        )
    
    # Verify token
    record = await db.fetch_one("""
        SELECT * FROM password_reset_tokens 
        WHERE token = :token AND used_at IS NULL
    """, {"token": token})
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    if record['expires_at'] < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired"
        )
    
    # Update password
    hashed_password = hash_password(new_password)
    await db.execute("""
        UPDATE users 
        SET password_hash = :password_hash, updated_at = :now
        WHERE id = :user_id
    """, {
        "password_hash": hashed_password,
        "user_id": record['user_id'],
        "now": datetime.utcnow()
    })
    
    # Mark token as used
    await db.execute("""
        UPDATE password_reset_tokens 
        SET used_at = :now 
        WHERE token = :token
    """, {"token": token, "now": datetime.utcnow()})
    
    # Revoke all refresh tokens (force re-login on all devices)
    await revoke_all_user_tokens(record['user_id'])
    
    return {"message": "Password has been reset successfully"}
```

---

## 🛡️ Authorization & RBAC

### Role-Based Access Control

**Roles:**
1. **User** - Regular user (default)
2. **Premium** - Paid subscriber
3. **Chef** - Verified chef/contributor
4. **Moderator** - Content moderator
5. **Admin** - Full access

### Permissions Matrix

```python
PERMISSIONS = {
    "user": [
        "read:recipes",
        "read:ingredients",
        "read:categories",
        "write:own_recipes",
        "write:own_comments",
        "write:own_ratings",
        "read:chat",
        "write:chat",
        "read:own_profile",
        "write:own_profile"
    ],
    
    "premium": [
        # Includes all user permissions, plus:
        "read:premium_recipes",
        "read:advanced_features",
        "unlimited:ai_chat",
        "access:meal_planning",
        "export:recipes"
    ],
    
    "chef": [
        # Includes all user permissions, plus:
        "write:verified_recipes",
        "read:analytics",
        "access:chef_tools"
    ],
    
    "moderator": [
        # Includes all user permissions, plus:
        "read:all_content",
        "moderate:recipes",
        "moderate:comments",
        "moderate:users",
        "delete:inappropriate_content"
    ],
    
    "admin": [
        # Full access
        "read:*",
        "write:*",
        "delete:*",
        "manage:users",
        "manage:system"
    ]
}

def get_user_permissions(role: str) -> List[str]:
    """Get permissions for a role"""
    permissions = PERMISSIONS.get(role, PERMISSIONS["user"])
    
    # Premium inherits from user
    if role == "premium":
        permissions = PERMISSIONS["user"] + PERMISSIONS["premium"]
    
    # Chef inherits from user
    if role == "chef":
        permissions = PERMISSIONS["user"] + PERMISSIONS["chef"]
    
    # Moderator inherits from user
    if role == "moderator":
        permissions = PERMISSIONS["user"] + PERMISSIONS["moderator"]
    
    return list(set(permissions))  # Remove duplicates
```

### Permission Checking

```python
from functools import wraps
from fastapi import Depends, HTTPException, status

def require_permission(permission: str):
    """Decorator to check if user has required permission"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: Dict = Depends(get_current_user), **kwargs):
            user_permissions = get_user_permissions(current_user['role'])
            
            # Check for wildcard permission (admin)
            if f"{permission.split(':')[0]}:*" in user_permissions:
                return await func(*args, current_user=current_user, **kwargs)
            
            # Check for specific permission
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied: {permission} required"
                )
            
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Usage example
@router.delete("/recipes/{recipe_id}")
@require_permission("delete:recipes")
async def delete_recipe(recipe_id: str, current_user: Dict = Depends(get_current_user)):
    # Only users with delete:recipes permission can access
    pass
```

### Resource Ownership Check

```python
async def check_resource_ownership(
    user_id: str,
    resource_type: str,
    resource_id: str
) -> bool:
    """Check if user owns a resource"""
    query_map = {
        "recipe": "SELECT user_id FROM recipes WHERE id = :id",
        "comment": "SELECT user_id FROM comments WHERE id = :id",
        "recipe_list": "SELECT user_id FROM recipe_lists WHERE id = :id"
    }
    
    query = query_map.get(resource_type)
    if not query:
        return False
    
    result = await db.fetch_one(query, {"id": resource_id})
    return result and str(result['user_id']) == user_id

def require_ownership(resource_type: str):
    """Decorator to check if user owns the resource"""
    def decorator(func):
        @wraps(func)
        async def wrapper(
            *args,
            resource_id: str,
            current_user: Dict = Depends(get_current_user),
            **kwargs
        ):
            # Admins bypass ownership check
            if current_user['role'] == 'admin':
                return await func(*args, resource_id=resource_id, current_user=current_user, **kwargs)
            
            # Check ownership
            is_owner = await check_resource_ownership(
                current_user['id'],
                resource_type,
                resource_id
            )
            
            if not is_owner:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to modify this resource"
                )
            
            return await func(*args, resource_id=resource_id, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Usage example
@router.put("/recipes/{recipe_id}")
@require_ownership("recipe")
async def update_recipe(
    recipe_id: str,
    recipe_data: RecipeUpdate,
    current_user: Dict = Depends(get_current_user)
):
    # Only recipe owner or admin can update
    pass
```

---

## 🔐 API Security

### Authentication Middleware

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict:
    """Extract and verify user from JWT token"""
    token = credentials.credentials
    
    try:
        payload = verify_access_token(token)
        user_id = payload.get('sub')
        
        # Fetch fresh user data from database
        user = await db.fetch_one(
            "SELECT * FROM users WHERE id = :id AND is_active = true",
            {"id": user_id}
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        return dict(user)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

async def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Optional[Dict]:
    """Get user if authenticated, None otherwise (for public endpoints)"""
    try:
        return await get_current_user(credentials)
    except:
        return None
```

### Rate Limiting

```python
from fastapi import Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

# Apply different limits based on authentication
@router.post("/auth/login")
@limiter.limit("5/minute")  # Strict limit for login attempts
async def login(request: Request, credentials: LoginCredentials):
    pass

@router.post("/recipes")
@limiter.limit("10/minute")  # Limit for creating recipes
async def create_recipe(
    request: Request,
    recipe: RecipeCreate,
    current_user: Dict = Depends(get_current_user)
):
    pass

@router.get("/recipes")
@limiter.limit("100/minute")  # Higher limit for read operations
async def list_recipes(request: Request):
    pass
```

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://cooking-app.com",
        "https://www.cooking-app.com",
        "http://localhost:3000",  # Development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=3600
)
```

### Input Validation

```python
from pydantic import BaseModel, EmailStr, Field, validator

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=2, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        is_valid, errors = validate_password(v)
        if not is_valid:
            raise ValueError(', '.join(errors))
        return v
    
    @validator('full_name')
    def validate_name(cls, v):
        # Sanitize input
        v = v.strip()
        if not v:
            raise ValueError('Name cannot be empty')
        return v
```

---

## 📱 Session Management

### Multi-Device Support

```python
async def get_active_sessions(user_id: str) -> List[Dict]:
    """Get all active sessions for a user"""
    sessions = await db.fetch_all("""
        SELECT 
            token,
            device_id,
            device_name,
            ip_address,
            user_agent,
            created_at,
            last_used_at,
            expires_at
        FROM refresh_tokens
        WHERE user_id = :user_id 
        AND is_revoked = false
        AND expires_at > :now
        ORDER BY last_used_at DESC
    """, {"user_id": user_id, "now": datetime.utcnow()})
    
    return [dict(s) for s in sessions]

async def revoke_session(user_id: str, token: str):
    """Revoke a specific session"""
    result = await db.execute("""
        UPDATE refresh_tokens 
        SET is_revoked = true, revoked_at = :now
        WHERE user_id = :user_id AND token = :token
    """, {"user_id": user_id, "token": token, "now": datetime.utcnow()})
    
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

@router.get("/auth/sessions")
async def list_sessions(current_user: Dict = Depends(get_current_user)):
    """List all active sessions for current user"""
    sessions = await get_active_sessions(current_user['id'])
    return {"sessions": sessions}

@router.delete("/auth/sessions/{token}")
async def delete_session(
    token: str,
    current_user: Dict = Depends(get_current_user)
):
    """Revoke a specific session"""
    await revoke_session(current_user['id'], token)
    return {"message": "Session revoked successfully"}

@router.delete("/auth/sessions")
async def delete_all_sessions(
    current_token: str = None,
    current_user: Dict = Depends(get_current_user)
):
    """Revoke all sessions except current one"""
    await revoke_all_user_tokens(current_user['id'], except_token=current_token)
    return {"message": "All sessions revoked except current"}
```

### Session Activity Tracking

```python
async def track_session_activity(token: str, activity: str):
    """Update session last_used_at timestamp"""
    await db.execute("""
        UPDATE refresh_tokens 
        SET last_used_at = :now, last_activity = :activity
        WHERE token = :token
    """, {
        "token": token,
        "activity": activity,
        "now": datetime.utcnow()
    })
```

---

## 🔐 Security Best Practices

### 1. Environment Variables

```python
# .env file (NEVER commit to git)
SECRET_KEY=your-super-secret-key-min-32-characters-long
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret

APPLE_CLIENT_ID=your-apple-client-id
APPLE_TEAM_ID=your-apple-team-id
APPLE_KEY_ID=your-apple-key-id
APPLE_PRIVATE_KEY=your-apple-private-key

FRONTEND_URL=https://cooking-app.com
```

### 2. HTTPS Only

```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# Force HTTPS in production
if settings.ENVIRONMENT == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
```

### 3. Security Headers

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.sessions import SessionMiddleware

# Trusted hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["cooking-app.com", "*.cooking-app.com"]
)

# Security headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

### 4. SQL Injection Prevention

```python
# ✅ GOOD: Using parameterized queries
await db.execute(
    "SELECT * FROM users WHERE email = :email",
    {"email": user_email}
)

# ❌ BAD: String concatenation (SQL injection risk)
await db.execute(f"SELECT * FROM users WHERE email = '{user_email}'")
```

### 5. XSS Prevention

```python
import bleach

def sanitize_html(content: str) -> str:
    """Sanitize HTML content to prevent XSS"""
    allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'a']
    allowed_attrs = {'a': ['href', 'title']}
    
    return bleach.clean(
        content,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True
    )
```

### 6. CSRF Protection

```python
from fastapi_csrf_protect import CsrfProtect

@app.post("/auth/login")
async def login(
    credentials: LoginCredentials,
    csrf_protect: CsrfProtect = Depends()
):
    # CSRF token validation for web clients
    csrf_protect.validate_csrf(request)
    
    # ... login logic
```

---

## 💻 Implementation Details

### FastAPI Authentication Setup

```python
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import redis.asyncio as redis

# Initialize FastAPI app
app = FastAPI(title="Cooking Assistant API")

# Database setup
engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Redis setup
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

# Security
security = HTTPBearer()

# Dependency to get database session
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

# Protected route example
@app.get("/api/v1/me")
async def get_current_user_profile(
    current_user: Dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user profile (requires authentication)"""
    return {"user": current_user}

# Public route with optional authentication
@app.get("/api/v1/recipes")
async def list_recipes(
    current_user: Optional[Dict] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db)
):
    """List recipes (public, but personalized if authenticated)"""
    # Show personalized results if user is authenticated
    if current_user:
        # Personalized logic
        pass
    else:
        # Public logic
        pass
```

### Database Schema for Auth

```sql
-- Users table (already defined in schema)

-- Refresh tokens table
CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    device_id VARCHAR(255),
    device_name VARCHAR(255),
    ip_address INET,
    user_agent TEXT,
    is_revoked BOOLEAN DEFAULT false,
    last_used_at TIMESTAMP,
    last_activity VARCHAR(255),
    expires_at TIMESTAMP NOT NULL,
    revoked_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_refresh_tokens_user_id (user_id),
    INDEX idx_refresh_tokens_token (token),
    INDEX idx_refresh_tokens_expires (expires_at)
);

-- OAuth accounts table
CREATE TABLE oauth_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,  -- 'google', 'facebook', 'apple'
    provider_user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(provider, provider_user_id),
    INDEX idx_oauth_accounts_user_id (user_id)
);

-- Password reset tokens table
CREATE TABLE password_reset_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_password_reset_tokens_token (token)
);

-- Email verification tokens table
CREATE TABLE email_verification_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email_verification_tokens_token (token)
);
```

---

## 🎯 Summary

### Authentication Methods
- ✅ Email/Password with bcrypt (cost factor 12)
- ✅ OAuth 2.0 (Google, Facebook, Apple)
- ✅ JWT access tokens (1 hour expiry)
- ✅ Refresh tokens (30 days expiry)

### Authorization
- ✅ Role-based access control (5 roles)
- ✅ Permission-based authorization
- ✅ Resource ownership validation
- ✅ Granular permissions

### Security Features
- ✅ Token-based authentication
- ✅ Multi-device support
- ✅ Session management
- ✅ Rate limiting
- ✅ CORS configuration
- ✅ Security headers
- ✅ Input validation
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ CSRF protection

### Key Security Practices
- Strong password requirements
- Token expiration and rotation
- Secure password reset flow
- Email verification
- Audit logging
- HTTPS enforcement
- Environment variable protection

---

**Next Steps**:
- ✅ Authentication & Authorization completed
- ⏳ Caching Strategy (next)
- ⏳ Phase 4: Implementation
