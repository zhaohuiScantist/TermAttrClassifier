import json

import gradio as gr
import requests


def ner_api(text, api_url="http://127.0.0.1:7647/nlp_license_term_extract"):
    """
    :param api_url:
    :param text:
    :return:
    """
    payload = {
        "doc_text": text
    }
    req = requests.post(api_url, json=payload)
    result = req.json()
    return result


def infer(text):
    result = ner_api(text)
    data = result["data"]
    # 高亮NER输出
    # high_light_result = {
    #     "text": "this is a text",
    #     "entities": [
    #         {
    #             "entity": "tag",
    #             # "word": "this",
    #             "start": 0,
    #             "end": 3
    #         }
    #     ]
    # }
    # 对极性判断结果输出表格
    high_light_result = data["gradio_highlight_result"]
    return json.dumps(result, ensure_ascii=False, indent=4), high_light_result


with gr.Blocks() as demo:
    gr.Markdown("# License extractor with NER, and term attitude parse by standford NLP tool.")
    input_text = gr.Textbox(label="License text", placeholder="Input licence text", lines=10)
    btn = gr.Button("Infer")

    origin_output = gr.JSON()
    ner_output = gr.HighlightedText()
    term_parse_result = gr.Tabs()

    btn.click(fn=infer, inputs=[input_text, ], outputs=[origin_output, ner_output])

demo.launch()
