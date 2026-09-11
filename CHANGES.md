# FinTrack — Other Category/Subcategory Update

## What changed
- Transactions now support custom category names when `Other` is selected.
- Transactions now support custom subcategory names when `Other` is selected.
- Custom values are persisted in the existing `category` / `subcategory` fields.
- Predefined taxonomy still uses `category_id` / `subcategory_id` where applicable.
- Custom values are not rejected by backend taxonomy validation.
- Empty custom names are rejected; whitespace is trimmed.
- Existing category/subcategory relationships and IDs are preserved.
- Existing CSV, Excel, and PDF export code already reads transaction `category` and `subcategory`, so custom values are included automatically.
- Search/filtering already checks category and subcategory, so custom values remain searchable.

## Frontend
Replace the existing `src/App.jsx` with the updated file.

## Backend
Replace the existing `app/schemas.py` and `app/routers/transactions.py` with the updated files.

No database reset is required.
