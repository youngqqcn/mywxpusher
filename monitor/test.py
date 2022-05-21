import traceback
import requests


def main():
    for i in range(10):
        try:
            try:
                raise RuntimeError("hhhh")
            except Exception as e:
                raise requests.exceptions.ConnectTimeout(e, request=None)
        except Exception as e:
            print('{}'.format(e))
            traceback.print_exc(limit=requests.exceptions.ConnectTimeout)
    
    pass

if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            pass
    