import os

from manage import ROOT_DIR


def read_text_file(text_file_path):
    with open(text_file_path, 'r') as txt_file:
        data = txt_file.readlines()
        data = [element.strip(r"\n").strip() for element in data]
    return data


if __name__ == '__main__':
    path = os.path.join(ROOT_DIR, 'config/credentials.txt')
    user_name, pw = read_text_file(path)
