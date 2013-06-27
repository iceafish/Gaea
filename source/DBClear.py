import pymongo


def main():
    db = pymongo.Connection('localhost',27017)
    print 'which db do you want to clear:'



if __name__ == '__main__':
    main()