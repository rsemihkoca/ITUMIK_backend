from fastapi.responses import JSONResponse


class CustomError(Exception):

    def __init__(self, code, message, status_code=400, parameters=None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.parameters = parameters
        super().__init__(self.message)

def SUCCESS_RESPONSE_DATA(result, status_code=200):
    return JSONResponse(result, status_code=status_code)