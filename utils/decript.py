from cryptography.fernet import Fernet

class Decript:
    def __init__(self):
        self.msg = None

    def dm(self):
        key = open(r"C:\martin\am.key", "rb").read()
        f = Fernet(key)
        decrypted_message = f.decrypt(open(r"C:\martin\am.cfg", "rb").read())

        return decrypted_message.decode()

if __name__ == "__main__":
    dc = Decript()
    print(dc.dm())
