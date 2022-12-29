import shutil
import json
import sys
import os
import logging

__home__ = os.path.dirname(__file__)
__client_home__ = os.path.dirname(__home__) + "/client-side"
sys.path.append(os.path.dirname(__home__))

from mytoolkit.txttag import TextTag as tag
import mytoolkit.core.brain as brain

inbound_dir = f'{__home__}/inbound'
outbound_dir = f'{__home__}/outbound'

p_logger = logging.getLogger("Process logger")
p_logger.propagate = False
p_logger.setLevel(logging.INFO)
if not p_logger.handlers:
    fh = logging.FileHandler(filename='phistory.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    fh.setFormatter(formatter)
    p_logger.addHandler(fh)


try:
    clients = os.listdir(inbound_dir)

    for client in os.listdir(inbound_dir):
        print(f'\r\n{tag.info.b()}[*]{tag.info} Accessing directory {tag.id}{client}{tag.close}')
        p_logger.info("Directory accessed.")

        os.makedirs(f'{outbound_dir}/{client}', exist_ok=True)

        # alg_contract_file = open(f'{inbound_dir}/{client}/algorithm contract.json', 'r')
        alg_contract_file = open(f'{__client_home__}/outbound/algorithm contract.json', 'r')
        source_file = f'{inbound_dir}/{client}/container.zip.encrypted'
        # target_file = f'{outbound_dir}/{client}/container.zip'
        target_file = source_file.replace(inbound_dir, outbound_dir).replace('.encrypted', '')
        compromised = False

        try:
            thinker = brain.fileThinker(sourceFile=source_file, targetFile=target_file, createKey=False, keyAddress=f'{__client_home__}/metadata', name='server')
            contract = json.load(alg_contract_file)

            if thinker.unthink(contract=contract):
                print(f'\r\n{tag.info.b()}File verified{tag.close}')
                p_logger.info("File verification successful.")
            else:
                print(f'\r\n{tag.error.b()}File compromised{tag.close}')
                p_logger.info("File compromised.")
                compromised = True

            thinker.close()

        except Exception as e:
            print(f"\r\n{tag.error.b()}[-] ERROR:{tag.error} Encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}")
            logging.error("Encountered exception.")
            raise e

        alg_contract_file.close()

        if not compromised:
            try:
                target = shutil.unpack_archive(target_file, os.path.dirname(target_file), format='zip')
                print(f'\r\n{tag.info}Unarchived {tag.id}{target_file}{tag.close}')
                p_logger.info("File unarchived.")
            except ValueError as e:
                print(f'\r\n{tag.error.b()}ERR:{tag.error}Can not idenity zip format/The file is not an archive{tag.close}\r\n{e}')
                p_logger.error("File is not an archive.")
            os.remove(target_file)

            try:
                os.removedirs(f'{inbound_dir}/{client}')

            except OSError as e:
                folder = f'{inbound_dir}/{client}'

                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)

                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)

                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)

                    except Exception as e:
                        print(f'{tag.error.b()}ERROR:{tag.error} Failed to delete {tag.id}{file_path}{tag.close}\r\n{e}')
                        p_logger.error("File not deleted.")
                
                os.removedirs(folder)

except FileNotFoundError as e:
    print(f'{tag.info}No files to process{tag.close}')
    p_logger.error("No file to process.")