import os

def list_files(directory):
    files = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            files.append(filename)
    return files

def main():
    directory = r'I:\1_steam_account\noin_system_mafile'
    files = list_files(directory)
    for file in files:
        print(file)

if __name__ == "__main__":
    main()
