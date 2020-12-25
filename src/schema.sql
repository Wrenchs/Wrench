CREATE TABLE
IF NOT EXISTS
reminders
(
    "created" TIMESTAMP,
    "expiers" TIMESTAMP,
    "reminder" VARCHAR,
    "where" BIGINT,
    "id" SERIAL,
    "author" BIGINT
)