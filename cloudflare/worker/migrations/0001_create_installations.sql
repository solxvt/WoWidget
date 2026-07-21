CREATE TABLE IF NOT EXISTS installations (
    discord_application_id TEXT PRIMARY KEY,
    token_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    last_upload_at TEXT,
    is_enabled INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_installations_enabled
ON installations(is_enabled);