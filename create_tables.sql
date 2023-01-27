-- Create first table
CREATE TABLE photoinfo(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    pathfile VARCHAR(1024) NOT NULL,
    photoname VARCHAR(50) NOT NULL
);

-- Create second table where photo information save
-- Second table unecessary, just to show relation between tables
-- Grayscale images 64*64 converted to string

-- NOTE - it is never recommended that you save the image IN the database
CREATE TABLE photos_grayscale_64(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    photos VARCHAR(16384)
);