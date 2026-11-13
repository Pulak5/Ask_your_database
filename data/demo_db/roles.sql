-- Roles and permissions setup for Ask Your Database

-- Ensure the app_readonly role exists and has SELECT-only permissions
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_readonly') THEN
        CREATE ROLE app_readonly WITH LOGIN PASSWORD 'app_readonly_password';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE ask_your_db TO app_readonly;
GRANT USAGE ON SCHEMA public TO app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO app_readonly;

-- Revoke write permissions explicitly for security depth
REVOKE INSERT, UPDATE, DELETE, TRUNCATE, DROP, ALTER, CREATE ON ALL TABLES IN SCHEMA public FROM app_readonly;
