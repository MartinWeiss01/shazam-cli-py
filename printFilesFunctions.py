import os


# Vypíše všechny soubory včetně těch v podsložách pomocí rekurze
def print_files_recursively(folder_path):

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isdir(file_path):
            print_files_recursively(file_path)
        else:
            print(filename) # Zmenit na file_path pokud chces celou cestu k souboru



# Vypíše všechny soubory včetně těch v podsložách
def print_files(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
           # file_path = os.path.join(root, filename)
            print(filename) # Zmenit na file_path pokud chces celou cestu k souboru + odkomentovat radek nad tim




# Vypíše všechny soubory, ale pouze ty, které se nachází v daném adresáři(neporchází podadresáře)
def print_files_in_folder(folder_path):

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):

            print(filename) # Zmenit na file_path pokud chces celou cestu k souboru