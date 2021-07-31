from product_meta_analysis.database.database import Database
from product_meta_analysis.database.create import create_comment_annotation_table, create_comment_table 

db = Database()
create_comment_annotation_table(db)
create_comment_table(db)
db.close()
