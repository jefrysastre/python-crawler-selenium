# -*- coding: utf-8 -*-
import sys, os, codecs
import pickle
import jsonpickle
from copy import deepcopy

from config import Config
from crawler import Crawler

# Chamar o script com a linha abaixo.
# python3 scholar_main.py generate_data config/scholar.json out_scholar.json


def usage(script_filename):
    print("Usage: %s generate_data/process_data [parameters]\n"
          "       For 'generate_data', parameters = config_filename data_filename\n"
          "       For 'process_data', parameters = data_filename out_filename\n"
          % script_filename)

    exit(1)


def generate_crawler_data(config_filename, data_filename):
    config = Config.load(config_filename)

    crawler = Crawler(config, daemon_mode=False)

    previous_page = ''
    for data in crawler.run():
        save_data_to_file(data, data_filename)

        paper_pos_data = ''
        for i in range(1, 11):
            paper_pos_data = 'paper_pos%d_data' % (i)
            if paper_pos_data in data:
                break

        if previous_page != data[paper_pos_data]['next_page']:
            if previous_page != '':
                print("Continues in page:")
                print(previous_page)

            previous_page = data[paper_pos_data]['next_page']


def save_data_to_file(data, filename):
    jsonpickle.set_encoder_options('json', ensure_ascii=False)
    str_data = jsonpickle.encode(data, unpicklable=False)

    with codecs.open(filename, "a", encoding="utf-8") as file:
        file.write(str_data + "\n")


def process_crawler_data(data_filename, out_filename):
    pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage(sys.argv[0])

    if sys.argv[1] == "generate_data":
        config_filename = sys.argv[2]
        data_filename = sys.argv[3]

        generate_crawler_data(config_filename, data_filename)
    elif sys.argv[1] == "process_data":
        data_filename = sys.argv[2]
        out_filename = sys.argv[3]

        process_crawler_data(data_filename, out_filename)
    else:
        usage(sys.argv[0])
