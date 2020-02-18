import gzip


# unzip files
def unzip_files(file, output_path):
    fp = open(output_path, "wb")
    with gzip.open(file, "rb") as f:
        bind_data = f.read()
    fp.write(bind_data)
    fp.close()
