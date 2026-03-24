import allure
import pytest

from test_data.test_data import POST_CREATE_DATA, POST_UPDATE_DATA
from src.utils.helpers import normalize_content


@allure.feature("Тестирование API для постов")
class TestPosts:

    @allure.title("Создание поста через API и проверка в БД")
    @allure.testcase("CREATE_POST_001")
    @pytest.mark.posts
    def test_create_post_and_check_in_db(self, api_client, db_client, config):

        post_data = POST_CREATE_DATA.copy()
        post_data["author"] = config["test_author_id"]

        created_post = api_client.create_post(post_data)
        post_id = created_post.id

        try:
            with allure.step("Проверяем данные созданного поста в ответе API"):
                assert (
                    created_post.title.get("rendered") == post_data["title"]
                ), f"Заголовок не совпадает: {created_post.title.get('rendered')} != {post_data['title']}"
                assert normalize_content(
                    created_post.content.get("rendered")
                ) == normalize_content(
                    post_data["content"]
                ), f"Содержимое не совпадает: {created_post.content.get('rendered')} != {post_data['content']}"
                assert (
                    created_post.status == post_data["status"]
                ), f"Статус не совпадает: {created_post.status} != {post_data['status']}"
                assert (
                    created_post.author == post_data["author"]
                ), f"Автор не совпадает: {created_post.author} != {post_data['author']}"

            with allure.step("Проверяем данные поста в базе данных"):
                post_from_db = db_client.get_post_by_id(post_id)
                assert post_from_db is not None, "Пост не найден в базе данных"
                assert (
                    post_from_db["post_title"] == post_data["title"]
                ), f"Заголовок в БД не совпадает: {post_from_db['post_title']} != {post_data['title']}"
                assert (
                    post_from_db["post_content"] == post_data["content"]
                ), f"Содержимое в БД не совпадает: {post_from_db['post_content']} != {post_data['content']}"
                assert (
                    post_from_db["post_status"] == post_data["status"]
                ), f"Статус в БД не совпадает: {post_from_db['post_status']} != {post_data['status']}"
                assert (
                    post_from_db["post_author"] == post_data["author"]
                ), f"Автор в БД не совпадает: {post_from_db['post_author']} != {post_data['author']}"

        finally:
            with allure.step("Удаляем созданный пост для очистки данных"):
                api_client.delete_post(post_id)
                db_client.delete_post_from_db(post_id)

    @allure.title("Обновление поста через API и проверка в БД")
    @allure.testcase("UPDATE_POST_001")
    @pytest.mark.posts
    def test_update_post_and_check_in_db(self, api_client, db_client, config):

        post_data = POST_CREATE_DATA.copy()
        post_data["author"] = config["test_author_id"]
        created_post = api_client.create_post(post_data)
        post_id = created_post.id

        try:
            update_data = POST_UPDATE_DATA.copy()
            update_data["author"] = config["test_author_id"]
            updated_post = api_client.update_post(post_id, update_data)

            with allure.step("Проверяем данные обновленного поста в ответе API"):
                assert (
                    updated_post.title.get("rendered") == update_data["title"]
                ), f"Заголовок не обновился: {updated_post.title.get('rendered')} != {update_data['title']}"
                assert normalize_content(
                    updated_post.content.get("rendered")
                ) == normalize_content(
                    update_data["content"]
                ), f"Содержимое не обновилось: {updated_post.content.get('rendered')} != {update_data['content']}"

            with allure.step("Проверяем данные поста в базе данных после обновления"):
                post_from_db = db_client.get_post_by_id(post_id)
                assert (
                    post_from_db is not None
                ), "Пост не найден в базе данных после обновления"
                assert (
                    post_from_db["post_title"] == update_data["title"]
                ), f"Заголовок в БД не обновился: {post_from_db['post_title']} != {update_data['title']}"
                assert (
                    post_from_db["post_content"] == update_data["content"]
                ), f"Содержимое в БД не обновилось: {post_from_db['post_content']} != {update_data['content']}"

        finally:
            with allure.step("Удаляем пост, чтобы не засорять данные"):
                api_client.delete_post(post_id)
                db_client.delete_post_from_db(post_id)

    @allure.title("Удаление поста через API и проверка в БД")
    @allure.testcase("DELETE_POST_001")
    @pytest.mark.posts
    def test_delete_post_and_check_in_db(self, api_client, db_client, config):

        post_data = POST_CREATE_DATA.copy()
        post_data["author"] = config["test_author_id"]
        created_post = api_client.create_post(post_data)
        post_id = created_post.id

        delete_response = api_client.delete_post(post_id)

        with allure.step("Проверяем ответ API после удаления"):
            assert delete_response is not None, "Ответ API при удалении пуст"

        with allure.step("Проверяем, что пост удален из базы данных"):
            post_from_db = db_client.get_post_by_id(post_id)
            assert post_from_db is None, "Пост найден в базе данных после удаления"

        with allure.step("Очищаем базу данных"):
            db_client.delete_post_from_db(post_id)
