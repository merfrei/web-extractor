"""Utils to be used for extractors.
Here will be included all the code to be shared for every extractor or that
does not specifically belong to any of them.
"""


def get_master_path(*paths, separator='/'):
    """ Find the common parts of the paths when the inputs have a "master path"
    The inputs must be of the same length
    >>> get_master_path(['/html/body/div/div[2]/div/div/div/div/div[2]/div[2]/div[2]/ul/li[1]/form/div/div[1]/span[1]',
                         '/html/body/div/div[2]/div/div/div/div/div[2]/div[2]/div[2]/ul/li[2]/form/div/div[1]/span[1]'])
    '/html/body/div/div[2]/div/div/div/div/div[2]/div[2]/div[2]/ul/li/form/div/div[1]/span[1]'
    """
    output = ''
    if len(paths) == 0:
        return output
    if len(paths) == 1:
        return paths[0]
    paths_parts = [p.split(separator) for p in paths]
    equal_lengths = [len(p) == len(paths_parts[0]) for p in paths_parts[1:]]
    if not all(equal_lengths):
        return output
    for i in range(len(paths[0])):
        lt = paths[0][i]
        try:
            equal_letters = [p[i] == lt for p in paths[1:]]
        except IndexError:
            return ''  # Incorrect length error
        if all(equal_letters):
            output += lt
    return output.replace('[]', '')
