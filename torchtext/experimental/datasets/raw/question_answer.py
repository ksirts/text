from torchtext.utils import download_from_url
import json
from torchtext.experimental.datasets.raw.common import RawTextIterableDataset
from torchtext.experimental.datasets.raw.common import wrap_split_argument
from torchtext.experimental.datasets.raw.common import add_docstring_header

URLS = {
    'SQuAD1':
        {'train': 'https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json',
         'dev': 'https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json'},
    'SQuAD2':
        {'train': 'https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json',
         'dev': 'https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v2.0.json'}
}


def _create_data_from_json(data_path):
    with open(data_path) as json_file:
        raw_json_data = json.load(json_file)['data']
        for layer1 in raw_json_data:
            for layer2 in layer1['paragraphs']:
                for layer3 in layer2['qas']:
                    _context, _question = layer2['context'], layer3['question']
                    _answers = [item['text'] for item in layer3['answers']]
                    _answer_start = [item['answer_start'] for item in layer3['answers']]
                    if len(_answers) == 0:
                        _answers = [""]
                        _answer_start = [-1]
                    # yield the raw data in the order of context, question, answers, answer_start
                    yield (_context, _question, _answers, _answer_start)


def _setup_datasets(dataset_name, root, split, offset):
    extracted_files = {key: download_from_url(URLS[dataset_name][key], root=root,
                                              hash_value=MD5[dataset_name][key], hash_type='md5') for key in split}
    return [RawTextIterableDataset(dataset_name, NUM_LINES[dataset_name][item],
                                   _create_data_from_json(extracted_files[item]), offset=offset) for item in split]


@wrap_split_argument
@add_docstring_header
def SQuAD1(root='.data', split=('train', 'dev'), offset=0):
    """
    Examples:
        >>> train_dataset, dev_dataset = torchtext.experimental.datasets.raw.SQuAD1()
        >>> for idx, (context, question, answer, ans_pos) in enumerate(train_dataset):
        >>>     print(idx, (context, question, answer, ans_pos))

    The iterator yields a tuple of (raw context, raw question, a list of raw answer,
    a list of answer positions in the raw context).
    For example, ('Architecturally, the school has a Catholic character. Atop the ...',
                  'To whom did the Virgin Mary allegedly appear in 1858 in Lourdes France?',
                  ['Saint Bernadette Soubirous'],
                  [515])
    """

    return _setup_datasets("SQuAD1", root, split, offset)


@wrap_split_argument
@add_docstring_header
def SQuAD2(root='.data', split=('train', 'dev'), offset=0):
    """
    Examples:
        >>> train_dataset, dev_dataset = torchtext.experimental.datasets.raw.SQuAD2()
        >>> for idx, (context, question, answer, ans_pos) in enumerate(train_dataset):
        >>>     print(idx, (context, question, answer, ans_pos))

    The iterator yields a tuple of (raw context, raw question, a list of raw answer,
    a list of answer positions in the raw context).
    For example, ('Beyoncé Giselle Knowles-Carter (/biːˈjɒnseɪ/ bee-YON-say) (born September 4, 1981) is an ...',
                  'When did Beyonce start becoming popular?',
                  ['in the late 1990s'],
                  [269])
    """

    return _setup_datasets("SQuAD2", root, split, offset)


DATASETS = {
    'SQuAD1': SQuAD1,
    'SQuAD2': SQuAD2
}

NUM_LINES = {
    'SQuAD1': {'train': 87599, 'dev': 10570},
    'SQuAD2': {'train': 130319, 'dev': 11873}
}

MD5 = {
    'SQuAD1': {'train': '981b29407e0affa3b1b156f72073b945', 'dev': '3e85deb501d4e538b6bc56f786231552'},
    'SQuAD2': {'train': '62108c273c268d70893182d5cf8df740', 'dev': '246adae8b7002f8679c027697b0b7cf8'}
}
