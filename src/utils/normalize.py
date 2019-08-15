import re

def escape_unicode(comment):
    """Returns a tokenized comment where the un-escaped unicode characters have been escaped."""
    return [word.encode('utf-8').decode('unicode_escape') if re.findall('\\\\\w+', word) != [] else word for word in
            comment]


def test_escape_a_acute():
    assert escape_unicode(['\\xe1']) == ['á']


def test_escape_a_umlaut():
    assert escape_unicode(['\\xe4']) == ['ä']


def test_escape_inverted_question_mark():
    assert escape_unicode(['\\xbf']) == ['¿']


def test_escape_sentence():
    assert escape_unicode(['Iam\\xbf trying to \\xe4figure out \\xe1 unicode']) == [
        'Iam¿ trying to äfigure out á unicode']



def replace_spaces(comment):
    """Replaces the unicode characters for whitespaces ad new lines with spaces."""
    pattern = '(\\\\xa0)|(\\\\n)|(\\\\xc2)'
    return [re.sub(pattern, " ", word) if re.findall(pattern, word) != [] else word for word in comment]


def test_replace_whitespace():
    assert replace_spaces(['\\ntest']) == [' test']


def test_replace_beginning():
    assert replace_spaces(['\\xa0test test']) == [' test test']


def test_replace_middle():
    assert replace_spaces(['test\\xa0test']) == ['test test']


def test_replace_middle_twice():
    assert replace_spaces(['test\\xa0\\xa0test']) == ['test  test']


def test_replace_end():
    assert replace_spaces(['test\\xa0']) == ['test ']


def test_replace_space():
    assert replace_spaces(['test\\n test']) == ['test  test']


def test_replace_two_times():
    assert replace_spaces(['test\\n test\\n test']) == ['test  test  test']


def test_replace_different_unicode():
    assert replace_spaces(['test\\xc2\\xa0test\\ntest']) == ['test  test test']


def normalize(comment):
    """Returns the normalized comment.

    This is achieved by tokenizing and making the words lowercase, handling unicode issues and finally
    by stripping the remaining punctuation.

    Args:
        str: The original comment.

    Returns:
        list: A list of the normalized words in the comment.

    """
    tokenized = list(map(lambda word: word.lower(), comment.split(" ")))

    spaces_replaced = replace_spaces(tokenized)
    cleaned = escape_unicode(spaces_replaced)
    stripped = list(
        map(lambda word: word.translate(str.maketrans("", "", r"""[!"#$%&()*+,-./:;<=>?@[]^_`{|}~'\¿]""")),
            cleaned))

    return " ".join( word for word in remove_stopwords(stripped))


def test_normalize_simple():
    assert normalize("HELLO BOY") == "hello boy"


def test_normalize_newline():
    assert normalize("HELLO BOY! \\n") == "hello boy  "


def test_normalize_punctuation():
    assert normalize("HELLO BOY! &") == "hello boy "


def test_normalize_double_backslash():
    assert normalize("HELLO BOY\\") == "hello boy"

stopwords = ['i', 'like', 'me', 'my', 'im', 'myself', 'we', 'our', 'ours',
       'ourselves', 'you', "you're", 'youre', "you've", 'youve', "you'll",
       'youll', "you'd", 'youd', 'your', 'yours', 'yourself',
       'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's",
       'shes', 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself',
       'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
       'who', 'whom', 'this', 'that', "that'll", 'thatll', 'thats',
       'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
       'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
       'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because',
       'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
       'against', 'between', 'into', 'through', 'during', 'before',
       'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
       'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
       'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
       'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
       'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
       'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'dont',
       'should', "should've", 'shouldve', 'now', 'd', 'll', 'm', 'o',
       're', 've', 'y', 'ain', 'aren', "aren't", 'arent', 'couldn',
       "couldn't", 'couldnt', 'didn', "didn't", 'didnt', 'doesn',
       "doesn't", 'doesnt', 'hadn', "hadn't", 'hadnt', 'hasn', "hasn't",
       'hasnt', 'haven', "haven't", 'havent', 'isn', "isn't", 'isnt',
       'ma', 'mightn', "mightn't", 'mightnt', 'mustn', "mustn't",
       'mustnt', 'needn', "needn't", 'neednt', 'shan', "shan't", 'shant',
       'shouldn', "shouldn't", 'shouldnt', 'wasn', "wasn't", 'wasnt',
       'weren', "weren't", 'werent', 'won', "won't", 'wont', 'wouldn',
       'would', "wouldn't", 'wouldnt']


def remove_stopwords(comment):
    """Returns a list of words with stop words removed."""
    return [word for word in comment if word not in stopwords]


def test_remove_stopwords():
    assert remove_stopwords(["the", "cat", "is", "king"]) == ["cat", "king"]


def test_remove_basic_stopwords():
    assert remove_stopwords(["you", "i", "would", "it", "like"]) == []


def test_remove_stopwords_capitals():
    # This does not remove capital stopwords as this is handled elsewhere in the normalization step
    assert remove_stopwords(["The", "cat", "Is", "king", "like"]) == ["The", "cat", "Is", "king"]
