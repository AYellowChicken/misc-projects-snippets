def header_generic(url):
    header = {
        "Host": url,
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "close",
    }
    return header