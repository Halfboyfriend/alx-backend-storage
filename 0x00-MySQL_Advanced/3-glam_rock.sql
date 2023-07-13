-- script that lists all bands with Glam rock as their main style, ranked by their longevity
-- Import this table dump: metal_bands.sql.zip
DELIMITER $$;
-- Create a stored procedure to calculate lifespan and retrieve the bands
CREATE PROCEDURE GetGlamRockBands()
BEGIN
    -- Create a temporary table to store the band names and lifespan
    CREATE TEMPORARY TABLE temp_bands (
        band_name VARCHAR(255),
        lifespan INT
    );

    -- Insert band names and lifespan into the temporary table
    INSERT INTO temp_bands (band_name, lifespan)
    SELECT
        band_name,
        IFNULL(
            YEAR(split) - YEAR(formed),
            YEAR('2022') - YEAR(formed)
        ) AS lifespan
    FROM
        metal_bands
    WHERE
        style LIKE '%Glam rock%';

    -- Retrieve the bands ranked by their longevity
    SELECT
        band_name,
        lifespan
    FROM
        temp_bands
    ORDER BY
        lifespan DESC;

    -- Drop the temporary table
    DROP TEMPORARY TABLE temp_bands;
END;$$
-- Reset the delimiter back to ;
DELIMITER ;

-- Call the stored procedure
CALL GetGlamRockBands();
