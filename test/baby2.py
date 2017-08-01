# -*- coding: utf-8 -*-
import sys, os, json, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import unicodedata

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
          "       For 'generate_data', parameters = config_filename data_filename\n" \
          "       For 'process_data', parameters = data_filename\n" \
          % script_filename)
    exit(1)


def generate_crawler_data(config_filename, data_filename):
    config = Config.load(config_filename)
     
    crawler = Crawler(config)
     
    data = crawler.run()
     
    data.dump(data_filename)


def process_crawler_data(data_filename):
    with open(data_filename, 'r') as data_file:
        data = json.load(data_file)
    
    query_list = data['children'][0]['data']
    for query in query_list.keys():
        query_data = query_list[query][0]['children'][0]['data']
        
        for page in query_data.keys():
            page_data = query_data[page][0]['data']
            
            for process_url in page_data.keys():
                process_root = page_data[process_url][0]
                
                personagem_list = process_root['children'][0]['children'][0]['data']['personagens']
                process_data = process_root['data']
                
                classe = process_data['classe'][0].encode('utf-8')
                integras_info = process_data['integras_info'][0]
                integras_links = process_data['integras_links']
                num_processo_field = process_data['num_processo'][0].encode('utf-8')
                orgao_julgador = process_data['orgao_julgador'][0].encode('utf-8')
                polo_ativo = process_data['polo_ativo'][0].encode('utf-8')
                polo_passivo = process_data['polo_passivo'][0].encode('utf-8')
                relator = process_data['relator'][0].encode('utf-8')
                
                integra_list = compose_integra_data(integras_info, integras_links)
                advogado_list = get_lawyers(personagem_list)
                num_processo = get_process_number(num_processo_field)
                
                right_integra = select_right_document(integra_list)
                integra_date = right_integra['date']
                pdf_result = process_pdf(right_integra['link'])
                
                print("Teste")


def get_process_number(process_number_field):
    mark_idx = process_number_field.find(':')
    
    assert mark_idx > -1
    
    process_number = process_number_field[mark_idx + 1:].strip()
    
    return process_number


def get_lawyers(character_list):
    lawyer_character = "ADVOGADO"
    lawyer_list = []
    
    for character_and_name in character_list:
        if len(character_and_name) != 2:
            continue
        
        character = character_and_name[0]
        name = character_and_name[1]
        
        if character.find(lawyer_character) > -1:
            lawyer_list.append(name)
    
    return lawyer_list


def compose_integra_data(integras_info, integras_links):
    integras_info_original = integras_info
    integra_data = []
    
    for integra_link in integras_links:
        for integra, integra_link in integra_link.items():
        
            integra_escaped = integra.replace('(', '\(').replace(')', '\)')
            pattern_integra = '\n%s.*?(\d\d/\d\d/\d\d\d\d)' % integra_escaped
            
            integra_date = re.findall(pattern_integra, integras_info)
            
            match_idx_list = [(m.start(0), m.end(0)) for m in re.finditer(pattern_integra, integras_info)]
            end_match_idx = match_idx_list[0][1]
            
            assert len(integra_date) > 0
            
            integra_data.append({'descr': integra,
                                  'link': integra_link,
                                  'date': integra_date[0]
                                 })
            
            integras_info = integras_info[end_match_idx:]
        
    return integra_data


# DOC_TYPES_SET = set()

agreement_name_list = ['inteiro teor n. 1 - acordao',
                       'acordao',
                       'inteiro teor n. 1 - acordao  com resolucao do merito',
                       'integra do(a) acordao'
                       ]

trial_name_list = ['julg. monocratico  com resolucao do merito',
                   'julgamento monocratico  com resolucao do merito',
                   'decisao monocratica',
                   ]


def select_right_document(docs):
    agreement_instance = None
    chosen_agreement_doc_type = ""
    chosen_agreement_doc_date = datetime.strptime('01/01/2020', '%d/%m/%Y')
    
    trial_instance = None
    chosen_trial_doc_type = ""
    chosen_trial_doc_date = datetime.strptime('01/01/2020', '%d/%m/%Y')
    
    for doc in docs:
#         global DOC_TYPES_SET
#         DOC_TYPES_SET.add(doc['descr'])
        
        doc_type = strip_accents(doc['descr']).lower()
        doc_date = datetime.strptime(doc['date'], '%d/%m/%Y')
        
        if doc_type in agreement_name_list and doc_date < chosen_agreement_doc_date:
            chosen_agreement_doc_type = doc_type
            chosen_agreement_doc_date = doc_date
             
            agreement_instance = doc
        
        if doc_type in trial_name_list and doc_date < chosen_trial_doc_date:
            chosen_trial_doc_type = doc_type
            chosen_trial_doc_date = doc_date
             
            trial_instance = doc
    
    selected_doc_instance = None
    
    if chosen_agreement_doc_type != "":
        selected_doc_instance = agreement_instance
    elif chosen_trial_doc_type != "":
        selected_doc_instance = trial_instance
    
    return selected_doc_instance


def process_pdf(url_pdf):
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage(sys.argv[0])
    
    if sys.argv[1] == "generate_data":
        config_filename = sys.argv[2]
        data_filename = sys.argv[3]
        
        generate_crawler_data(config_filename, data_filename)
    elif sys.argv[1] == "process_data":
        data_filename = sys.argv[2]
        
        process_crawler_data(data_filename)
    else:
        usage(sys.argv[0])
