DROP TABLE IF EXISTS backup;

/*[1] Create a new table "backup" with the following columns and datatypes*/

CREATE TABLE backup(
    backup_id         INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    relation          VARCHAR(25),
    num_rows              INT,
    num_cols              INT,
    csv_length        INT,
    xml_length        INT,
    json_length       INT,
    csv_data          LONGTEXT,
    xml_data          LONGTEXT,
    json_data         JSON,
    dtm               DATETIME DEFAULT CURRENT_TIMESTAMP
);

/* [7] Create a view v_table_backups that has a list of backups without the actual csv_data, xml_data, and json_data */
CREATE OR REPLACE VIEW v_table_backups AS
       SELECT backup_id, relation as table_name, num_rows, num_cols as columns, csv_length, xml_length, json_length, dtm as date_saved
       FROM backup
       ORDER BY relation, dtm;

/* [7] Retrieve from view v_table_backups that has a list of backups without the actual csv_data, xml_data, and json_data */
SELECT * FROM v_table_backups;