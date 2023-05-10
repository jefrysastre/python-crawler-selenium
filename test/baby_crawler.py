# -*- coding: utf-8 -*-
import sys, os, json, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import unicodedata
import jsonpickle
import codecs
from copy import deepcopy
import pickle
import csv

from config import Config
from crawler import Crawler


def strip_accents(text):
#     text = unicode(text, 'utf-8')
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


def usage(script_filename):
    print("Usage: %s generate_data/process_data [parameters]\n" \
          "       For 'generate_data', parameters = config_filename data_filename state_filename\n" \
          "       For 'process_data', parameters = data_filename out_filename\n" \
          % script_filename)
    exit(1)


def load_crawler_state(crawler, state_filename):
    if os.path.isfile(state_filename):
        with open(state_filename, "rb") as state_file:
            state = pickle.load(state_file)

        crawler.set_state(state)


def generate_crawler_data(config_filename, data_filename, state_filename):
    config = Config.load(config_filename)

    crawler = Crawler(config)

    # If state file exists, loads it in order to resume crawling
    load_crawler_state(crawler, state_filename)

    data_list = []
    data_saving_interval = 10
    has_finished = False
    last_saved_page = None

    while not has_finished:
        try:
            for i, data in enumerate(crawler.run()):
                if len(data_list) == data_saving_interval:
                    save_data_to_file(data_list, data_filename)

                    state = crawler.get_state()
                    with open(state_filename, "wb") as state_file:
                        pickle.dump(state, state_file)

                    data_list = []

                data_list.append(deepcopy(data))

            has_finished = True
        except Exception as e:
            print("Error crawling website. Error: \"%s\"" % (e))

            if data is not None:
                print(data)

            load_crawler_state(crawler, state_filename)
            data_list = []

    if len(data_list) > 0:
        save_data_to_file(data_list, data_filename)

    # Deletes the state file
    if os.path.isfile(state_filename):
        os.remove(state_filename)


def save_data_to_file(data, filename):
    jsonpickle.set_encoder_options('json', ensure_ascii=False)
    str_data = jsonpickle.encode(data, unpicklable=False)

    with codecs.open(filename, "a", encoding="utf-8") as file:
        file.write(str_data + "\n")


def write_lines_to_csv(filename, mode, my_list):
    with open(filename, mode) as file:
        writer = csv.writer(file, delimiter=";", lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        writer.writerows(my_list)


def process_crawler_data(data_filename, out_filename):
    header = [u'Classe', u'Número do processo', u'Órgão julgador', u'Relator',
              u'Polo ativo (1o parecer)', u'Polo passivo (2o parecer)', u'URL do processo']

    write_lines_to_csv(out_filename, 'w', [header])

    process_details_list = []
    csv_writing_interval = 10

    with open(data_filename, 'r') as data_file:
        for line in data_file:
            data_list = json.loads(line)

            for data in data_list:
                process_url = data['link_value']
                process_data = data['process_data']

                if len(process_data['classe']) > 0:
                    classe = process_data['classe'][0]
                else:
                    classe = ""

                num_processo_field = process_data['num_processo'][0]

                if len(process_data['orgao_julgador']) > 0:
                    orgao_julgador = process_data['orgao_julgador'][0]
                else:
                    orgao_julgador = ""

                if len(process_data['relator']) > 0:
                    relator = process_data['relator'][0]
                else:
                    relator = ""

                if len(process_data['polo_ativo']) > 0:
                    polo_ativo = process_data['polo_ativo'][0]
                else:
                    polo_ativo = ""

                if len(process_data['polo_passivo']) > 0:
                    polo_passivo = process_data['polo_passivo'][0]
                else:
                    polo_passivo = ""

                num_processo = get_process_number(num_processo_field)

                process_details_list.append([classe, num_processo, orgao_julgador, relator,
                                             polo_ativo, polo_passivo, process_url])

                if len(process_details_list) == csv_writing_interval:
                    write_lines_to_csv(out_filename, 'a', process_details_list)

                    process_details_list = []

            if len(process_details_list) > 0:
                write_lines_to_csv(out_filename, 'a', process_details_list)


def get_process_number(process_number_field):
    mark_idx = process_number_field.find(':')
    
    assert mark_idx > -1
    
    process_number = process_number_field[mark_idx + 1:].strip()
    
    return process_number




if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage(sys.argv[0])
    
    if sys.argv[1] == "generate_data":
        config_filename = sys.argv[2]
        data_filename = sys.argv[3]
        state_filename = sys.argv[4]

        generate_crawler_data(config_filename, data_filename, state_filename)
    elif sys.argv[1] == "process_data":
        data_filename = sys.argv[2]
        out_filename = sys.argv[3]

        process_crawler_data(data_filename, out_filename)
    else:
        usage(sys.argv[0])
