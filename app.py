import json
import logging
import time

from flask import Flask, request, make_response
from flask_cors import CORS
from werkzeug.serving import WSGIRequestHandler

from TermAttrClassifier import BERTClassifierWrapper
from config import config
from logger_config import configure_logger

app = Flask(__name__)
CORS(app)


def fix_werkzeug_logging():
    def address_string(self):
        return "[%s]-[%s]" % (self.headers.get('X-Forwarded-For', self.client_address[0]),
                              self.headers.get('X-Real-Ip', self.client_address[0]))

    WSGIRequestHandler.address_string = address_string


class StandardResponse(Exception):
    status_code = 200

    def __init__(
            self,
            is_success: bool = True,
            msg=None,
            status_code: int = 200,
            data=None,
            runtime: float = 0.0,
    ):
        Exception.__init__(self)
        if data is None:
            data = {}
        if status_code is not None:
            self.status_code = status_code
        fix_werkzeug_logging()
        self.msg = msg
        self.data = data
        self.is_success = is_success
        self.runtime = runtime

    def to_dict(self):
        rv = dict()
        rv["code"] = 0 if self.is_success else 1
        rv["data"] = self.data
        rv["msg"] = self.msg
        rv["runtime"] = self.runtime
        logger.info(rv)
        return rv


@app.errorhandler(StandardResponse)
def handle_standard_response(resp):
    resp_dict = resp.to_dict()
    result_json = json.dumps(resp_dict, ensure_ascii=False)
    response = make_response(result_json)
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    response.status_code = resp.status_code
    return response


def clean_text(text: str):
    return "".join(text.split())


@app.route("/nlp_term_attr_classifier", methods=["POST"])
def predict():
    """
    :return:
    """
    start_time = time.time()
    try:
        request_json_dict = request.json
        logger.info(request_json_dict)
    except Exception as ignore:
        if request.content_length < 1024:
            request_data_log = f"request body: {request.get_data(as_text=True)}"
        else:
            request_data_log = "request body 太大，不予输出"
        logger.error(f"/np [POST]接口错误。{request_data_log}", exc_info=True)
        raise StandardResponse(msg="不合法的json格式", status_code=400, is_success=False)
    try:
        term_list = request_json_dict.get("term_list")
        debug_flag = request_json_dict.get("sec_debug", 0)
        model_result = model.predict(term_list=term_list,
                                     debug=debug_flag == "enable")
        end_time = time.time()
        runtime = round((end_time - start_time), 2)
        return handle_standard_response(
            StandardResponse(
                data=model_result,
                runtime=runtime
            )
        )

    except Exception as e:
        if request.content_length < 1024:
            request_data_log = f"request body: {request.get_data(as_text=True)}"
        else:
            request_data_log = "request body 太大，不予输出"
        logger.error(f"/np [POST]接口错误。{request_data_log}", exc_info=True)
        end_time = time.time()
        runtime = round((end_time - start_time), 2)
        raise StandardResponse(
            msg=str(e), status_code=400, is_success=False, runtime=runtime
        )


def build_gunicorn(config_file):
    """
    gunicorn的启动入口
    也可以当做CLI的启动入口，可以从这里读取配置文件，初始化模型
    :param config_file: 配置文件，将CLI的入参按行拆分写在txt文件里
    :return:
    """
    global args
    global model
    global logger
    with open(config_file, 'r', encoding='utf-8') as fop:
        lines = [i.strip() for i in fop.readlines()]
        args = config(cli_lines=lines)
        logging.info(args)
    # gunicorn
    # 必须从build_gunicorn方法获取APP实例，用于读取配置文件
    gunicorn_logger = logging.getLogger('gunicorn.info')
    logger = configure_logger("info", "logs/prediction.log")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    logger.info(args)

    logger.info("load model")
    model = BERTClassifierWrapper(model_dir=args.model_dir,
                                  log_dir=args.log_dir,
                                  flag_use_gpu=args.use_gpu)
    logger.info("load model done.")
    return app


if __name__ == '__main__':
    # python CLI entrypoint
    build_gunicorn("config_for_gunicorn_start.ini")
    app.run(port=args.port, host="0.0.0.0", debug=False, threaded=False)
