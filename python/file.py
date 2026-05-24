from zipfile import ZipFile
import time

def main():
    try:
        zipfile = input("Enter file location")
        with ZipFile(file = zipfile, mode='r', allowZip64=True) as file:
            textfile = file.open(name=file.namelist()[0], mode='r')
            print(textfile.read())
            textfile.close()
            Epath= str(input("Where do you want to Extract file? "))
            print("Extract files", end=" ")
            for i in range(3):
                print(".", end=" ")
                time.sleep(1)
            file.extractall(path=Epath)
            print("Done!\n File extracted in:", Epath)

    except:
        print("File Cannot be extracted...")

if __name__ == "__main__":
    main()