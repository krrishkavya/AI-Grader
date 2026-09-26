# Task: Add Category Filtering to Product Search CLI

Our team uses a product search CLI located at `/workspace/product_search.py` backed by SQLite (`products.db`).

Currently, running:
```bash
python product_search.py search <query>
```
returns products whose names match the search query.

### Feature Request
We need to support an optional `--category <name>` flag to filter search results by category:
```bash
python product_search.py search <query> --category <category_name>
```

When provided, only active products matching both the search query AND the specified category should be returned.

### Requirements
1. Update `product_search.py` so the `search` subcommand accepts an optional `--category <name>` argument.
2. When `--category` is provided, filter the results so only products matching both the query and the exact category are returned.
3. When `--category` is omitted, the search should behave as before, matching across all categories.
4. Existing subcommands (`list` and `info`) must remain functional.
5. All existing tests in `tests/test_search.py` must pass.
