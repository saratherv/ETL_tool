
CREATE TABLE IF NOT EXISTS bill_of_lading_bookmarks (
    ID SERIAL PRIMARY KEY,
    bill_of_landing_id  TEXT NOT NULL,
    bol_meta_data JSON,
    containers JSON
);

CREATE TABLE IF NOT EXISTS container_no_bookmarks (
    ID SERIAL PRIMARY KEY,
    container_id TEXT NOT NULL,
    meta_data JSON NOT NULL,
    tracking_data JSON 
);



