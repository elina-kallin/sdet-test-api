from sqlalchemy import create_engine, text
from typing import Optional, List, Dict, Any


class WordPressDataBaseClient:
    """Клиент для работы с базой данных WordPress"""

    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        self.connection_string = (
            f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        )
        self.engine = create_engine(self.connection_string)

    # ==================== посты ====================

    def get_posts(self):
        query = text("select * from wp_posts where post_type = 'post'")
        with self.engine.connect() as connect:
            result = connect.execute(query)
            return [dict(row._mapping) for row in result]

    def get_post_by_id(self, post_id: int):
        query = text(
            "select * from wp_posts where id = :post_id and post_type = 'post'"
        )
        with self.engine.connect() as connect:
            result = connect.execute(query, {"post_id": post_id})
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None

    def create_post_in_db(
        self,
        title: str,
        content: str,
        status: str,
        author: int,
        comment_status: str = "open",
    ):
        query = text(
            """
            insert into wp_posts
            (post_title, post_content, post_status, post_author, post_type, comment_status, post_date, post_date_gmt)
            values
            (:title, :content, :status, :author, 'post', :comment_status, now(), utc_timestamp())
        """
        )
        with self.engine.connect() as connect:
            result = connect.execute(
                query,
                {
                    "title": title,
                    "content": content,
                    "status": status,
                    "author": author,
                    "comment_status": comment_status,
                },
            )
            connect.commit()
            return result.inserted_primary_key[0]

    def update_post_in_db(self, post_id: int, data: Dict[str, Any]):
        set_clauses = []
        for key, value in data.items():
            set_clauses.append(f"{key} = :{key}")

        query = text(
            f"""
            update wp_posts
            set {', '.join(set_clauses)}
            where id = :post_id and post_type = 'post'
        """
        )
        data["post_id"] = post_id

        with self.engine.connect() as connect:
            result = connect.execute(query, data)
            connect.commit()
            return result.rowcount > 0

    def delete_post_from_db(self, post_id: int):
        query = text("delete from wp_posts where id = :post_id and post_type = 'post'")
        with self.engine.connect() as connect:
            result = connect.execute(query, {"post_id": post_id})
            connect.commit()
            return result.rowcount > 0

    # ==================== комментарии ====================

    def get_comments(self):
        query = text("select * from wp_comments")
        with self.engine.connect() as connect:
            result = connect.execute(query)
            return [dict(row._mapping) for row in result]

    def get_comment_by_id(self, comment_id: int):
        query = text("select * from wp_comments where comment_id = :comment_id")
        with self.engine.connect() as connect:
            result = connect.execute(query, {"comment_id": comment_id})
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None

    def get_comments_by_post_id(self, post_id: int):
        query = text("select * from wp_comments where comment_post_id = :post_id")
        with self.engine.connect() as connect:
            result = connect.execute(query, {"post_id": post_id})
            return [dict(row._mapping) for row in result]

    def create_comment_in_db(
        self,
        post_id: int,
        author: int,
        content: str,
        comment_author: str = "Test User",
        status: str = "approved",
    ) -> int:
        query = text(
            """
            insert into wp_comments
            (comment_post_id, user_id, comment_author, comment_content, comment_date, comment_date_gmt, comment_approved)
            values
            (:post_id, :author, :comment_author, :content, now(), utc_timestamp(), :status)
        """
        )
        with self.engine.connect() as connect:
            result = connect.execute(
                query,
                {
                    "post_id": post_id,
                    "author": author,
                    "comment_author": comment_author,
                    "content": content,
                    "status": status,
                },
            )
            connect.commit()
            return result.inserted_primary_key[0]

    def update_comment_in_db(self, comment_id: int, data: Dict[str, Any]):
        field_mapping = {
            "content": "comment_content",
            "author": "user_id",
            "post": "comment_post_id",
            "status": "comment_approved",
        }

        db_data = {}
        for key, value in data.items():
            if key in field_mapping:
                db_data[field_mapping[key]] = value
            else:
                db_data[key] = value

        set_clauses = []
        for key, value in db_data.items():
            set_clauses.append(f"{key} = :{key}")

        query = text(
            f"""
            update wp_comments
            set {', '.join(set_clauses)}
            where comment_id = :comment_id
        """
        )
        db_data["comment_id"] = comment_id

        with self.engine.connect() as connect:
            result = connect.execute(query, db_data)
            connect.commit()
            return result.rowcount > 0

    def delete_comment_from_db(self, comment_id: int):
        query = text("delete from wp_comments where comment_id = :comment_id")
        with self.engine.connect() as connect:
            result = connect.execute(query, {"comment_id": comment_id})
            connect.commit()
            return result.rowcount > 0
