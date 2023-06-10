import PyPDF2
import string
import itertools
import concurrent.futures

def make(min_length, max_length):
    character_set = string.ascii_letters + string.digits + string.punctuation
    for length in range(min_length, max_length + 1):
        combinations = itertools.product(character_set, repeat=length)
        for combination in combinations:
            password = ''.join(combination)
            yield password

def check(password):
    file_path = '/Users/lung/Documents/psychologicalevaluation.pdf'
    pdf_reader = PyPDF2.PdfReader(file_path)
    wrong = pdf_reader.decrypt("")
    if pdf_reader.is_encrypted:
        if wrong != pdf_reader.decrypt(password):
            print(f"Password found: {password}")
            raise KeyboardInterrupt

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(check, make(11, 20))
