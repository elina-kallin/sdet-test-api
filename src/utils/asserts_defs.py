def assert_status_code(response, expected_code):
    """
    сравнивает код ответа от сервера с ожидаемым
    :param response: полученный от сервера ответ
    :param expected_code: ожидаемый код ответа
    :raises AssertionError: если значения не совпали
    """
    assert expected_code == response.status_code, (
        response.add_compare_result(expected_code, response.status_code)
        .add_request_url()
        .add_response_info()
        .get_message()
    )


# def assert_left_in_right_json(response, exp_json, actual_json):
#     """
#     проверяет, что все значения полей exp_json равны значениям полей в actual_json
#     :param response: полученный ответ от сервера
#     :param exp_json: ожидаемый эталонный json
#     :param actual_json: полученый json
#     :raises AssertionError: если в exp_json есть поля со значениями, которые отличаются или которых нет в actual_json
#     """
#     root = "root:" if isinstance(actual_json, list) else ""
#     compare_res = compare_json_left_in_right(exp_json, actual_json, key=root, path=root)
#     assert not compare_res, (
#         response.add_compare_result(compare_res)
#         .add_request_url()
#         .add_response_info()
#         .get_message()
#     )
