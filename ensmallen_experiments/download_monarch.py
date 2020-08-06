import re
import bs4 
import requests
from tqdm.auto import tqdm

def get_files_from_url(dir_url):
    """Given the url to a http folder, return the list of urls present in it.
    
    Arguments
    ---------
    dir_url: str,
        The url of the http folder
    """
    r = requests.get(dir_url)
    soup = bs4.BeautifulSoup(r.text)
    urls = []
    for link in soup.findAll('a'):
        file = link.get('href')
        if file.startswith(".") or not file.endswith(".nt"):
            continue
        url = dir_url + file
        urls.append(url)

def download_file(file_pointer, url: str):  
    """Read the content of the url and write it to the file pointer
    Since the files are  big, this function use streaming download.
    Arguments
    ---------
    file_pointer: _io.BufferedWriter,
        The file pointer obtained from a open() where the content will be written.
    url: str,
        The url of the file to download.
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=8192): 
            file_pointer.write(chunk)

def download_monarch(dir_url: str = """https://archive.monarchinitiative.org/202008/rdf/"""):
    """
    Download monarch into a single edge file.

    Arguments
    ---------
    dir_url: str,
        The url from where to retreive the files urls
    """
    urls = get_files_from_url(dir_url)
    with open(filename, "wb") as f:
        f.write("\t".join(["subject", "object", "weight"]))
        for url in tqdm(urls):
            download_file(f, url)