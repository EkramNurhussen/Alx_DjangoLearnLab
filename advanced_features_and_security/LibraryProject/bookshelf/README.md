# Advanced Features and Security Project

## Custom User Model
- Defined `CustomUser` extending `AbstractUser` with `date_of_birth` (DateField) and `profile_photo` (ImageField).
- Custom manager `CustomUserManager` with `create_user` and `create_superuser`.
- Updated `settings.py` with `AUTH_USER_MODEL = 'bookshelf.CustomUser'`.
- Admin integration in `admin.py` with `CustomUserAdmin`.

## Managing Permissions and Groups in Django
### Setup
- **Custom Permissions**: Added to `Book` model in `models.py`:
  - `can_view`: Allows viewing books.
  - `can_create`: Allows creating books.
  - `can_edit`: Allows editing books.
  - `can_delete`: Allows deleting books.
- **Groups**: Created via Django admin (`/admin/auth/group/`):
  - **Editors**: Assigned `can_create` and `can_edit`.
  - **Viewers**: Assigned `can_view`.
  - **Admins**: Assigned all (`can_view`, `can_create`, `can_edit`, `can_delete`).

### Enforcement in Views
- Views in `views.py` use `@permission_required` decorators:
  - `book_list`: Requires `bookshelf.can_view`.
  - `book_create`: Requires `bookshelf.can_create`.
  - `book_edit`: Requires `bookshelf.can_edit`.
  - `book_delete`: Requires `bookshelf.can_delete`.
- URLs in `urls.py` map to these views (e.g., `path('books/create/', views.book_create, name='book_create')`).

### Testing
- Create test users in Django admin (`/admin/`).
- Assign users to groups (e.g., user1 to Editors, user2 to Viewers).
- Log in as each user:
  - Viewers: Can access `/books/` (list), but not create/edit/delete.
  - Editors: Can create/edit, but not delete.
  - Admins: Full access.
- Verify: Unauthorized access raises `PermissionDenied` (403 error).

## Security Best Practices
- `settings.py`: `DEBUG=False`, `SECURE_BROWSER_XSS_FILTER=True`, `X_FRAME_OPTIONS='DENY'`, `SECURE_CONTENT_TYPE_NOSNIFF=True`, `CSRF_COOKIE_SECURE=True`, `SESSION_COOKIE_SECURE=True`.
- Templates: `{% csrf_token %}` in forms (e.g., `form_example.html`).
- Views: Use ORM (e.g., `Book.objects.all()`) and forms for validation to prevent SQL injection/XSS.
- CSP: Added `csp.middleware.CSPMiddleware` and policies (e.g., `CSP_DEFAULT_SRC = ("'self'",)`).

## HTTPS and Secure Redirects
- `settings.py`: `SECURE_SSL_REDIRECT=True`, `SECURE_HSTS_SECONDS=31536000`, `SECURE_HSTS_INCLUDE_SUBDOMAINS=True`, `SECURE_HSTS_PRELOAD=True`.
- Secure cookies/headers as above.
- Deployment: Nginx config in `deployment/nginx.conf` for SSL (redirect HTTP to HTTPS).

Run `python manage.py check --deploy` to verify security settings.
# Security Best Practices
- **Location**: `LibraryProject/LibraryProject/settings.py`, `bookshelf/templates/bookshelf/`, `bookshelf/views.py`
- **Settings**:
  - `DEBUG=False`: Prevents sensitive info exposure.
  - `SECURE_BROWSER_XSS_FILTER`, `X_FRAME_OPTIONS`, `SECURE_CONTENT_TYPE_NOSNIFF`: Browser-side protections.
  - `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`: HTTPS-only cookies.
  - `CSP`: Restricts content sources via `django-csp` middleware.
- **Templates**: Added `{% csrf_token %}` to `form_example.html`.
- **Views**: Use Django ORM for queries and `BookForm` for input validation.
- **Testing**:
  - Verify CSRF protection by submitting forms without tokens.
  - Test XSS by injecting `<script>alert('test')</script>` (should be escaped).
  - Run `python manage.py check --deploy` to validate settings.
  # HTTPS and Secure Redirects
- **Location**: `LibraryProject/LibraryProject/settings.py`, `deployment/nginx.conf`
- **Settings**:
  - `SECURE_SSL_REDIRECT`: Redirects HTTP to HTTPS.
  - `SECURE_HSTS_SECONDS`: Enforces HTTPS for 1 year.
  - `SECURE_HSTS_INCLUDE_SUBDOMAINS/PRELOAD`: Applies to subdomains and allows preloading.
  - `SESSION_COOKIE_SECURE/CSRF_COOKIE_SECURE`: HTTPS-only cookies.
- **Deployment**: Nginx configuration in `deployment/nginx.conf` for SSL/TLS.
- **Security Review**:
  - Verified HTTPS redirects using browser and `curl`.
  - Cookies confirmed as HTTPS-only via browser dev tools.
  - Headers (`X-Frame-Options`, etc.) verified.
  - **Improvements**: Add rate limiting and monitoring for production.