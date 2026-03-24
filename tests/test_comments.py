import allure
import pytest

from test_data.test_data import (
    COMMENT_CREATE_DATA,
    COMMENT_UPDATE_DATA,
    POST_CREATE_DATA,
)
from src.utils.helpers import normalize_content


@allure.feature("Тестирование API для комментариев")
class TestComments:

    @allure.title("Создание комментария через API и проверка в БД")
    @allure.testcase("CREATE_COMMENT_001")
    @pytest.mark.comments
    def test_create_comment_and_check_in_db(self, api_client, db_client, config):

        post_data = POST_CREATE_DATA
        post_data["author"] = config["test_author_id"]
        created_post = api_client.create_post(post_data)
        post_id = created_post.id

        try:
            comment_data = COMMENT_CREATE_DATA.copy()
            comment_data["author"] = config["test_author_id"]
            comment_data["post"] = post_id
            created_comment = api_client.create_comment(comment_data)
            comment_id = created_comment.id

            try:
                with allure.step(
                    "Проверяем данные созданного комментария в ответе API"
                ):
                    assert (
                        created_comment.post == post_id
                    ), f"ID поста не совпадает: {created_comment.post} != {post_id}"
                    assert (
                        created_comment.author == config["test_author_id"]
                    ), f"ID автора не совпадает: {created_comment.author} != {config['test_author_id']}"
                    assert normalize_content(
                        created_comment.content.get("rendered")
                    ) == normalize_content(
                        comment_data["content"]
                    ), f"Содержимое не совпадает: {created_comment.content.get('rendered')} != {comment_data['content']}"

                with allure.step("Проверяем данные комментария в базе данных"):
                    comment_from_db = db_client.get_comment_by_id(comment_id)
                    assert (
                        comment_from_db is not None
                    ), "Комментарий не найден в базе данных"
                    assert (
                        comment_from_db["comment_post_ID"] == post_id
                    ), f"ID поста в БД не совпадает: {comment_from_db['comment_post_ID']} != {post_id}"
                    assert (
                        comment_from_db["user_id"] == config["test_author_id"]
                    ), f"ID автора в БД не совпадает: {comment_from_db['user_id']} != {config['test_author_id']}"
                    assert (
                        comment_from_db["comment_content"] == comment_data["content"]
                    ), f"Содержимое в БД не совпадает: {comment_from_db['comment_content']} != {comment_data['content']}"

            finally:
                with allure.step("Удаляем созданный комментарий"):
                    try:
                        api_client.delete_comment(comment_id)
                    except Exception:
                        pass
                    db_client.delete_comment_from_db(comment_id)

        finally:
            with allure.step("Удаляем пост после теста"):
                api_client.delete_post(post_id)
                db_client.delete_post_from_db(post_id)

    @allure.title("Обновление комментария через API и проверка в БД")
    @allure.testcase("UPDATE_COMMENT_001")
    @pytest.mark.comments
    def test_update_comment_and_check_in_db(self, api_client, db_client, config):

        post_data = POST_CREATE_DATA
        post_data["author"] = config["test_author_id"]

        created_post = api_client.create_post(post_data)
        post_id = created_post.id

        comment_data = COMMENT_CREATE_DATA.copy()
        comment_data["author"] = config["test_author_id"]
        comment_data["post"] = post_id
        created_comment = api_client.create_comment(comment_data)
        comment_id = created_comment.id

        try:
            update_data = COMMENT_UPDATE_DATA.copy()
            update_data["author"] = config["test_author_id"]
            update_data["post"] = post_id
            updated_comment = api_client.update_comment(comment_id, update_data)

            with allure.step("Проверяем данные обновленного комментария в ответе API"):
                assert normalize_content(
                    updated_comment.content.get("rendered")
                ) == normalize_content(
                    update_data["content"]
                ), f"Содержимое не обновилось: {updated_comment.content.get('rendered')} != {update_data['content']}"

            with allure.step(
                "Проверяем данные комментария в базе данных после обновления"
            ):
                comment_from_db = db_client.get_comment_by_id(comment_id)
                assert (
                    comment_from_db is not None
                ), "Комментарий не найден в базе данных после обновления"
                assert (
                    comment_from_db["comment_content"] == update_data["content"]
                ), f"Содержимое в БД не обновилось: {comment_from_db['comment_content']} != {update_data['content']}"

        finally:
            with allure.step("Удаляем комментарий и пост после теста"):
                try:
                    api_client.delete_comment(comment_id)
                except Exception:
                    pass
                db_client.delete_comment_from_db(comment_id)
                api_client.delete_post(post_id)
                db_client.delete_post_from_db(post_id)

    @allure.title("Удаление комментария через API и проверка в БД")
    @allure.testcase("DELETE_COMMENT_001")
    @pytest.mark.comments
    def test_delete_comment_and_check_in_db(self, api_client, db_client, config):

        post_data = POST_CREATE_DATA
        post_data["author"] = config["test_author_id"]

        created_post = api_client.create_post(post_data)
        post_id = created_post.id

        comment_data = COMMENT_CREATE_DATA.copy()
        comment_data["author"] = config["test_author_id"]
        comment_data["post"] = post_id
        created_comment = api_client.create_comment(comment_data)
        comment_id = created_comment.id

        delete_response = api_client.delete_comment(comment_id)

        with allure.step("Проверяем ответ API после удаления"):
            assert delete_response is not None, "Ответ API при удалении пуст"

        with allure.step("Проверяем, что комментарий удален из базы данных"):
            comment_from_db = db_client.get_comment_by_id(comment_id)
            assert (
                comment_from_db is None
            ), "Комментарий найден в базе данных после удаления"

        with allure.step("Удаляем пост после теста"):
            api_client.delete_post(post_id)
            db_client.delete_post_from_db(post_id)
