# FinTrack feature update

## Safe database migration
Run the API once. `migrations/safe_migrate.py` creates new tables and adds nullable fields to existing users/transactions without dropping data. Categories/subcategories use soft-disable semantics, so historical transaction relationships remain intact.

## Admin
Existing users remain `user`. To grant admin access, set the user's `role` to `admin` in your existing database (for example with your DB client). Do not expose an admin role selector in public registration.

## Password reset
Configure SMTP in `.env`. The server stores only a SHA-256 hash of the reset token; raw tokens are sent by email, expire after `RESET_TOKEN_MINUTES`, and are single-use.

## Reports
CSV, Excel and PDF exports are client-side and export exactly the currently displayed/filtered transaction rows.
