# -*- coding: utf-8 -*-
import sys, os, json, re, codecs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import jsonpickle
from copy import deepcopy
import csv

from config import Config
from crawler import Crawler

#python3 scholar_main.py generate_data config/scholar.json out_scholar.json

def usage(script_filename):
    print("Usage: %s generate_data/process_data [parameters]\n" \
          "       For 'generate_data', parameters = config_filename data_filename\n" \
          "       For 'process_data', parameters = data_filename out_filename\n" \
          % script_filename)
    
    # Codigo de saida de erro
    exit(1)


def generate_crawler_data(config_filename, data_filename):
    config = Config.load(config_filename)
    
    crawler = Crawler(config, daemon_mode=False)
    
    data_list = []
    for data in crawler.run():
        print(data)
        data_list.append(deepcopy(data))
    
    if len(data_list) > 0:
        save_data_to_file(data_list, data_filename)


def save_data_to_file(data, filename):
    # Especifica as opcoes para salvar o arquivo JSON
    jsonpickle.set_encoder_options('json', ensure_ascii=False)
    str_data = jsonpickle.encode(data, unpicklable=False)
    
    file = codecs.open(filename, "a", encoding="utf-8")
    file.write(str_data + "\n")
    file.close()


def write_lines_to_csv(filename, mode, my_list):
    file = open(filename, mode)
    writer = csv.writer(file, delimiter=";", lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    writer.writerows(my_list)
    file.close()


def process_crawler_data(data_filename, out_filename):
    header = ["Número do processo", "URL da íntegra"]
    write_lines_to_csv(out_filename, 'w', [header])
    
    process_details_list = []
    csv_writing_interval = 10
    
    data_file = open(data_filename, 'r')
    for line in data_file:
        data_list = json.loads(line)
        
        for data in data_list:
            process_data = data['process_data']
            num_processo = process_data['num_processo'][0]
            integra_list = process_data['integras_link']
            
            num_processo_processed = num_processo.strip('Processo No: ')
            if len(integra_list) > 0:
                integra_mais_recente_dict = integra_list[0]
            else:
                integra_mais_recente_dict = {}
            
            for integra_detalhe, integra_url in integra_mais_recente_dict.items():
                fields = [num_processo_processed, integra_url]
                process_details_list.append(fields)
            
                if len(process_details_list) == csv_writing_interval:
                    write_lines_to_csv(out_filename, 'a', process_details_list)
                
                    process_details_list = []
    
    if len(process_details_list) > 0:
        write_lines_to_csv(out_filename, 'a', process_details_list)

    data_file.close()


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
