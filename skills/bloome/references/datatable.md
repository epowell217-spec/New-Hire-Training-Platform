# DataTable Operations

Structured data tables for tabular data, queryable by widgets and agents.

## Commands

```bash
table query <tableId>                              # Read all rows
table insert <tableId> --data '{"col":"val"}'      # Insert row
table update <tableId> <rowId> --data '{"col":"new"}'  # Update row
table delete <tableId> <rowId>                     # Delete row
```

## Notes

- Tables are conversation-scoped resources
- Each table has a defined column schema
- Row changes are broadcast in real-time to all viewers
- Use `/data-tables list` to discover accessible tables; use `/data-tables schema` to inspect available methods, permissions, risk, and examples
