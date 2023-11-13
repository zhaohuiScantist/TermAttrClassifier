import argparse


def config(cli_lines=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_dir', type=str, required=True)
    parser.add_argument('--log_dir', type=str, required=True)
    parser.add_argument('--use_gpu', action="store_true", dest="use_gpu", default=True)
    parser.add_argument('--port', default=7780)
    args = parser.parse_args(args=cli_lines)

    print(args)
    return args
