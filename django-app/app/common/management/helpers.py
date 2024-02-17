def get_file_contents(path):
    """
    Read file at path and return contents.
    Tries multiple encodings.
    """
    encodings = ['utf-8', 'windows-1250', 'windows-1252']  # add more
    file_reader = None
    file_contents = None
    for e in encodings:
        try:
            file_reader = open(path, 'r', encoding=e)
            file_contents = file_reader.read()
        except UnicodeDecodeError:
            print(f'got unicode error with {e}, trying different encoding')
        finally:
            if file_reader:
                file_reader.close()

    return file_contents


def write_file_contents(path, contents):
    """
    Write file contents at path.
    """
    f = open(path, 'w')
    f.write(contents)
    f.close()
