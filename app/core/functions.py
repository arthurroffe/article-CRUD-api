from rest_framework.response import Response



# 回傳訊息
class ApiRes():
    def __init__(self):
        self._err_code: int | None = None
        self._msg: str = ''

    def _gen_error_res_data(self):
        return {
            'error': {
                'code': self._err_code,
                'message': self._msg
            }
        }

    def _gen_success_res_data(self, return_data=None):
        return {
            "message": self._msg,
            "returnData": return_data
        }

    def generate(self, status_code: int, return_data=None):
        if self._err_code:
            res_data = self._gen_error_res_data()
        else:
            res_data = self._gen_success_res_data(return_data)

        return Response(status=status_code, data=res_data)

    def set_parameters_err(self):
        self._err_code = 4006
        self._msg = 'Missing or Error parameters'
        return self

    def set_already_exists_err(self):
        self._err_code = 4005
        self._msg = 'already exists'
        return self

    def set_does_not_exists_err(self):
        self._err_code = 4007
        self._msg = 'Does not exists'
        return self

    def set_token_err(self):
        self._err_code = 4004
        self._msg = 'The USer token is already expired or error.'
        return self

    def set_user_is_not_active_err(self):
        self._err_code = 4002
        self._msg = 'Login Error.'
        return self

    def set_user_is_not_exists_err(self):
        self._err_code = 4003
        self._msg = 'The UserID did not identify a User in the system.'
        return self

    def set_user_login_err(self):
        self._err_code = 4003
        self._msg = 'One or both of Username and Password are invalid.'
        return self

    def set_success_msg(self):
        self._msg = "ok"
        return self

    def set_connection_err(self):
        self._err_code = 500
        self._msg = "Connction Error"
        return self