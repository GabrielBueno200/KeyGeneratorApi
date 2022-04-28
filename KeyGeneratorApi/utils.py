from urllib.request import urlopen


def get_numbers_file(file_name: str) -> list[int]:
    sas_token = '?sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacupitfx&se=2022-04-28T22:58:11Z&st=2022-04-28T14:58:11Z&spr=https&sig=%2BBb6gnwuHNZjc4HgqE2Ysg5YkJaqEHd0WCItsdSkKkY%3D'
    file_path = f'https://keygenapi.file.core.windows.net/keygenapi/{file_name}' + sas_token
    return list(map(lambda n: int(n.decode()), list(urlopen(file_path))))
