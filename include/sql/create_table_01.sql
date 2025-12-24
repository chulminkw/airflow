-- Ensure the schema exists (optional)
CREATE SCHEMA IF NOT EXISTS doc;

-- Create the table
CREATE TABLE IF NOT EXISTS doc.possum (
    case_num    INTEGER,
    site        INTEGER,
    pop         TEXT,
    sex         TEXT,
    age         INTEGER,
    hdlngth     REAL,
    skullw      REAL,
    totlngth    REAL,
    taill       REAL,
    footlgth    REAL,
    earconch    REAL,
    eye         REAL,
    chest       REAL,
    belly       REAL
);