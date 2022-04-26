from main import tokopedia_scrape

if __name__ == "__main__":
    katakunci = input('Masukkan kata kunci : ')
    print('mencari semua product dengan kata kunci ' + katakunci)
    tokopedia_scrape(katakunci)