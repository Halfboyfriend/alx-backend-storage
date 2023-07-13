-- script that lists all bands with Glam rock as their main style, ranked by their longevity
-- Import this table dump: metal_bands.sql.zip
DELIMITER $$

-- Create a stored procedure to calculate band longevity
CREATE PROCEDURE calculate_band_longevity()
BEGIN
    -- Create a temporary table to store the results
    CREATE TEMPORARY TABLE IF NOT EXISTS band_longevity (
        band_name VARCHAR(100),
        lifespan INT
    );

    -- Insert data into the temporary table
    INSERT INTO band_longevity (band_name, lifespan)
    SELECT band_name, (YEAR('2022-01-01') - split + 1) AS lifespan
    FROM (
        SELECT band_name, SUBSTRING_INDEX(lifespan, ' - ', 1) AS formed,
               SUBSTRING_INDEX(lifespan, ' - ', -1) AS split
        FROM metal_bands
        WHERE style LIKE '%Glam rock%'
    ) AS subquery;

    -- Select bands ranked by longevity
    SELECT band_name, lifespan
    FROM band_longevity
    ORDER BY lifespan DESC;
END$$

-- Call the stored procedure
CALL calculate_band_longevity();

-- Reset the delimiter back to the semicolon
DELIMITER ;
