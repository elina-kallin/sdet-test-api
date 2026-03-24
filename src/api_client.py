from typing import Any, Dict, Optional
import requests
import allure

from src.models.post import PostResponse
from src.models.comment import CommentResponse


class WordPressAPIClient:
    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        session: Optional[requests.Session] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.session = session or requests.Session()
        self.session.auth = requests.auth.HTTPBasicAuth(username, password)
        self.session.headers.update({"Content-Type": "application/json"})

    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    """API для постов"""

    @allure.step("Создать пост")
    def create_post(self, data: Dict[str, Any]) -> PostResponse:
        url = self._url("/wp/v2/posts")
        response = self.session.post(url, json=data)
        assert (
            response.status_code == 201
        ), f"Создание поста провалено: {response.status_code} {response.text}"
        return PostResponse.model_validate(response.json())

    @allure.step("Получить пост по ID {post_id}")
    def get_post(self, post_id: int) -> PostResponse:
        url = self._url(f"/wp/v2/posts/{post_id}")
        response = self.session.get(url)
        assert (
            response.status_code == 200
        ), f"Получение поста по ID провалено: {response.status_code} {response.text}"
        return PostResponse.model_validate(response.json())

    @allure.step("Обновить пост {post_id}")
    def update_post(self, post_id: int, data: Dict[str, Any]) -> PostResponse:
        url = self._url(f"/wp/v2/posts/{post_id}")
        response = self.session.post(url, json=data)
        assert (
            response.status_code == 200
        ), f"Обновление поста провалено: {response.status_code} {response.text}"
        return PostResponse.model_validate(response.json())

    @allure.step("Удалить пост {post_id}")
    def delete_post(self, post_id: int) -> Dict[str, Any]:
        url = self._url(f"/wp/v2/posts/{post_id}")
        params = {"force": True}
        response = self.session.delete(url, params=params)
        assert (
            response.status_code == 200
        ), f"Удаление поста провалено: {response.status_code} {response.text}"
        return response.json()

    @allure.step("Получить все посты")
    def get_all_posts(self, page: int = 1, per_page: int = 100):
        url = self._url("/wp/v2/posts")
        params = {"page": page, "per_page": per_page}
        response = self.session.get(url, params=params)
        assert (
            response.status_code == 200
        ), f"Получение всех постов провалено: {response.status_code} {response.text}"
        return [PostResponse.model_validate(post) for post in response.json()]

    """Далее API для комментариев"""

    @allure.step("Создать комментарий")
    def create_comment(self, data: Dict[str, Any]) -> CommentResponse:
        url = self._url("/wp/v2/comments")
        response = self.session.post(url, json=data)
        assert (
            response.status_code == 201
        ), f"Создание комментария провалено: {response.status_code} {response.text}"
        return CommentResponse.model_validate(response.json())

    @allure.step("Получить комментарий по ID {comment_id}")
    def get_comment(self, comment_id: int) -> CommentResponse:
        url = self._url(f"/wp/v2/comments/{comment_id}")
        response = self.session.get(url)
        assert (
            response.status_code == 200
        ), f"Получение комментария по ID провалено: {response.status_code} {response.text}"
        return CommentResponse.model_validate(response.json())

    @allure.step("Обновить комментарий {comment_id}")
    def update_comment(self, comment_id: int, data: Dict[str, Any]) -> CommentResponse:
        url = self._url(f"/wp/v2/comments/{comment_id}")
        response = self.session.post(url, json=data)
        assert (
            response.status_code == 200
        ), f"Обновление комментария провалено: {response.status_code} {response.text}"
        return CommentResponse.model_validate(response.json())

    @allure.step("Удалить комментарий {comment_id}")
    def delete_comment(self, comment_id: int) -> Dict[str, Any]:
        url = self._url(f"/wp/v2/comments/{comment_id}")
        params = {"force": True}
        response = self.session.delete(url, params=params)
        assert (
            response.status_code == 200
        ), f"Удаление комментария провалено: {response.status_code} {response.text}"
        return response.json()

    @allure.step("Получить комментарии поста {post_id}")
    def get_post_comments(self, post_id: int):
        url = self._url("/wp/v2/comments")
        params = {"post": post_id}
        response = self.session.get(url, params=params)
        assert (
            response.status_code == 200
        ), f"Получение комментариев поста провалено: {response.status_code} {response.text}"
        return [CommentResponse.model_validate(c) for c in response.json()]

    @allure.step("Получить текущего пользователя")
    def get_current_user(self) -> Dict[str, Any]:
        url = self._url("/wp/v2/users/me")
        response = self.session.get(url)
        assert (
            response.status_code == 200
        ), f"Получение текущего пользователя провалено: {response.status_code} {response.text}"
        return response.json()
