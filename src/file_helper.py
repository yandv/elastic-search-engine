import json
import xml.etree.ElementTree as ET

import os
import time

current_dir = os.path.dirname(__file__)

documents = []

print("Carregando documentos, aguarde...")
start_time = time.time()

with open(f'{current_dir}/../resources/papers.json', 'r') as f:
    for idx, document in enumerate(json.load(f)):
        # abra o xml do document
        
        file_name_without_extension = document['filename'].split('.')[0]
        file_name_xml = f'{file_name_without_extension}.xml'
        
        with open(f'{current_dir}/../resources/{document['type']}/{file_name_xml}', 'r') as xml_file:
            xml_content = xml_file.read()
            
            try:
                root = ET.fromstring(xml_content)
                feature_element = root.find('.//feature[@title]')
                
                if feature_element is not None:
                    document['title'] = feature_element.get('title')
            except Exception as e:
                print(f'Error parsing XML: {file_name_xml} {e}')
        
        with open(f'{current_dir}/../resources/{document["type"]}/{document["filename"]}', 'r') as txt_file:
            document['content'] = txt_file.read()
        
        document['path'] = current_dir + '/../resources/' + document['type'] + '/' + document['filename']
        document['id'] = f'{file_name_without_extension}-{idx}'
        documents.append(document)

print(f"Documentos carregados com sucesso ({time.time() - start_time:.4f}s)")

def get_documents():
    return documents

def get_suspicious_documents():
    for document in documents:
        if document['type'] == 'suspicious-document':
            yield document

def get_source_documents():
    for document in documents:
        if document['type'] == 'source-document':
            yield document

def get_document_by_file_name(file_name: str):
    for document in documents:
        if document['filename'] == file_name:
            return document

def get_source_documents_from_suspicious():
    source_documents = set()
    
    for document in get_suspicious_documents():
        for source_document in document['src_file']:
            source_documents.add(source_document)
        
    return source_documents

def calculate_found_percentage(suspicious_document_file_name: str, source_documents_found: int):
    suspicious_document = get_document_by_file_name(suspicious_document_file_name)
    source_documents = suspicious_document['src_file']
    return source_documents_found / len(source_documents)