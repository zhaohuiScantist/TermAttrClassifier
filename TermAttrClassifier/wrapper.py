import logging
from typing import List, Dict

import torch
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from transformers import pipeline

from .config import MODEL_PREDICT_RESULT_MAPPING


class BERTClassifierWrapper(object):
    def __init__(self,
                 model_dir,
                 log_dir,
                 flag_use_gpu: bool = True):
        self.model_input_text_template = "Term name:{name}, Term content:{text}"
        self.log_dir = log_dir
        self.model_dir = model_dir
        if flag_use_gpu and torch.cuda.is_available():
            logging.info("Enable CUDA support.")
            self.flag_use_gpu = True
        else:
            logging.info("No CUDA support.")
            self.flag_use_gpu = False
        # load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
        # load model
        model = AutoModelForSequenceClassification.from_pretrained(self.model_dir, num_labels=2)
        model.eval()
        if self.flag_use_gpu:
            model.cuda()

        self.classifier = pipeline("sentiment-analysis",
                                   model=model,
                                   tokenizer=self.tokenizer,
                                   device=0 if self.flag_use_gpu else -1)

    def predict(self, term_list: List[Dict], debug=False):
        """
        BERT预测接口
        term_text_list：输入文本列表，后续有需要的话会改为Batch模式
        返回：todo: doc for this
        """
        model_input_text_list = []
        for i in term_list:
            input_text = self.model_input_text_template.format(**i)
            model_input_text_list.append(input_text)
        result = self.classifier(model_input_text_list)
        for idx, i in enumerate(result):
            i["label"] = MODEL_PREDICT_RESULT_MAPPING[i["label"]]
            i.update(term_list[idx])
        return result
