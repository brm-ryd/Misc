#!/usr/bin/python
"""
email harvesting - will crawl the site and find all related email address &
store into txt file
"""
import sys, urllib

to_search_list = []
searched_list = []
email_list = []

def download(max_iterations):
    iteration = 1
    while iteration <= int(max_iterations):
        print iteration

        if len(to_search_list) == 0:
            print "dead url end"
            break

        first_url = to_search_list[0]
        to_search_list.remove(first_url)
        searched_list.append(first_url)


        def download_url(url):
            return urllib.urlopen(url)


        try:
            content = download_url(first_url)
        except:
            try:
                content = download_url(first_url)
            except:
                iteration += 1
                continue

        for line in content:
            import re

            url_expression = r"http://+[\w\d:#@%/;$()~_?\+-=\\\.&]*"
            regex = re.compile(url_expression)

            results = regex.findall(line)

            if results:
                for result in results:
                    if result not in searched_list:
                        to_search_list.append(result)


            email_expression = r"\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6}"
            eregex= re.compile(email_expression)

            e_results = eregex.findall(line)

            if e_results:
                for e_result in e_results:
                    if e_result not in email_list:
                        email_list.append(e_result)

        iteration += 1


def output_results():
    print "number sites to search: %s" % len(to_search_list)
    print "number sites searched: %s" % len(searched_list)
    print "number emails collected: %s" % len(email_list)


def write_results():
    info_file_name = "info.txt"
    i = open("info.txt", "w")
    i.write("number sites to search: %s \n" % len(to_search_list))
    i.write("number sites searched: %s \n" % len(searched_list))
    i.write("number emails collected: %s \n" % len(email_list))
    i.close()


    file_name = "email_addresses.txt"
    n = open(file_name, "w")

    for email in email_list:
        entry = email + "\n"
        n.write(entry)
    n.close()

def get_input():
    try:
        start_url = sys.argv[1]
        iterations = sys.argv[2]

    except:
        raise Exception("\n\nInvalid input, <site_url> <num iterations> \n")
    return start_url, iterations

def main():
    start_url, iterations = get_input()
    to_search_list.append(start_url)

    download(iterations)
    output_results()
    write_results()

if __name__ == "__main__":
    main()
