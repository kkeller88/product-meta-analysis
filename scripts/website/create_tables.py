from product_meta_analysis.database.database import Database
from product_meta_analysis.database.create import (create_website_annotation_table,
    create_website_content_table, create_website_url_table)

db = Database()
create_website_url_table(db)
create_website_content_table(db)
create_website_annotation_table(db)
db.close()
