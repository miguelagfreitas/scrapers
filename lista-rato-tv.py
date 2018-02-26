import urllib2, os, sys, re

def clear():
    if os.name == 'nt':
        os.system('cls')
    if os.name == 'posix':
        os.system('clear')


def main():
    clear()

    rato_url = "http://ratotv.fun/movies"
    req = urllib2.Request(rato_url, headers={'User-Agent' : "Magic Browser"})
    con = urllib2.urlopen(req)
    lines = con.readlines()
    list_file = open('list.txt', 'w+')

    last_page = 1
    for line in lines:
        if "..." in line and "/page/" in line:
            list_a = re.findall(r'\b\d+\b', line)
            last_page = list_a[len(list_a) -1]

    for page in range(1, int(last_page) + 1):
        page_url = "http://ratotv.fun/movies"
        if page > 1:
            page_url = page_url + "/page/" + str(page)
        req = urllib2.Request(page_url, headers={'User-Agent' : "Magic Browser"})
        con = urllib2.urlopen(req)
        lines = con.readlines()
        for line in lines:
            if '<a href="http://ratotv.fun/movies/' in line and 'alt="' in line:
                #re.search( r'(.*) are (.*?) .*', line, re.M|re.I)
                search = re.search(r'alt="(.*)', line)
                if search:
                    title = search.group()
                    title = title.replace("alt=\"", "")
                    title = title.replace("\" /></a>", "")
                    list_file.write(title + "\n")
                    print title.decode("utf-8")

    list_file.close()
if __name__ == '__main__':
    main()
