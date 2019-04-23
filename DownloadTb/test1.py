import requests

def download_file(url, path):
    with closing(requests.get(url, stream=True)) as r:
        chunk_size = 1024
        content_size = int(r.headers['content-length'])
        print ('下载开始')
        with open(path, "wb") as f:
            n = 1
            for chunk in r.iter_content(chunk_size=chunk_size):
                loaded = n*1024.0/content_size
                f.write(chunk)
                print ('已下载{0:%}'.format(loaded))
                n += 1



if __name__ == '__main__':
    download_file('https://cloud.video.taobao.com/play/u/1091756444/p/1/e/6/t/1/50096924877.mp4','D:\\taobao_img')
