from cltk.corpus.utils.importer import CorpusImporter
from cltk.stem.latin.declension import CollatinusDecliner
from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer
from cltk.stem.lemma import LemmaReplacer
from cltk.tag.pos import POSTag
from cltk.exceptions import UnknownLemma
import re
import numpy as np


PUNCTUATION_SIGNS = [".", ",", ";", ":", "!", "?"]


def get_additionals(lemma, tag):
    tag_info = tag[1]
    if tag_info is None:
        return None
    try:
        decliner = CollatinusDecliner()
        if tag_info[0] == "N":
            declination = decliner.decline(lemma)
            return declination[3][0] + " " + tag_info[6].lower()
        if tag_info[0] == "A":
            declination = decliner.decline(lemma)
            return declination[13][0] + " " + declination[26][0]
        if tag_info[0] == "V":
            declination = decliner.decline(lemma)
            return declination[67][0] + " " + declination[18][0]
    except UnknownLemma as e:
        print(e)
        return None


def sanitize(words, lemmata, tags):
    new_words = words.copy()
    lemmata_to_change = []
    if len(words) != len(tags):
        did_correct = 0, False
        for i, word in enumerate(words):
            if did_correct[1]:
                did_correct = did_correct[0], False
                continue
            tag = tags[i - did_correct[0]]
            if word != tag[0]:
                print(word, tag)
                if i < len(words)-1 and word + words[i+1] == tag[0]:
                    new_words[i] = word + words[i+1]
                elif i < len(words)-1 and words[i+1] + word == tag[0]:
                    new_words[i] = words[i+1] + word
                else:
                    raise AssertionError("tags and words differ")
                lemmata_to_change.append(i)
                del new_words[i+1]
                did_correct = did_correct[0]+1, True
        if len(lemmata_to_change) > 0:
            new_lemmata = LemmaReplacer("latin").lemmatize([new_words[index] for index in lemmata_to_change])
            for index, lemma in zip(lemmata_to_change, new_lemmata):
                lemmata[index] = lemma
    return new_words, lemmata, tags


if __name__ == '__main__':
    corpus_importer = CorpusImporter("latin")
    corpus_importer.import_corpus("latin_models_cltk")

    with open("./test_text.txt", "r") as f:
        test_text = f.read()
    sentence_tokenizer = TokenizeSentence('latin')

    sentences = sentence_tokenizer.tokenize(test_text)
    # test if sentence start with numbers
    number_re = re.compile("\d+")
    sentence_count = len(sentences)
    sentences_with_number = [number_re.match(sentence) is not None for sentence in sentences]
    sentences_with_number_count = np.sum(sentences_with_number)
    starts_with_numbers = sentences_with_number_count >= sentence_count / 3
    if starts_with_numbers and sentences_with_number_count < sentence_count:
        sentences = [sentence.strip() + " " + sentences[i+1].strip()
                     if i < len(sentences)-1 and not sentences_with_number[i+1]
                     else sentence.strip() for i, sentence in enumerate(sentences) if sentences_with_number[i]]

    word_tokenizer = WordTokenizer("latin")
    lemmatizer = LemmaReplacer("latin")
    pos_tagger = POSTag("latin")

    for i, sentence in enumerate(sentences):
        if not sentence.startswith(str(i+1)):
            print(f"sentence number incorrect should be {i+1}")
        words = [word for word in word_tokenizer.tokenize(sentence) if word not in PUNCTUATION_SIGNS
                 and not number_re.match(word)]
        lemmata = lemmatizer.lemmatize(words)
        tags = [tag for tag in pos_tagger.tag_ngram_123_backoff(sentence) if tag[0] not in PUNCTUATION_SIGNS
                and not number_re.match(tag[0])]
        words, lemmata, tags = sanitize(words, lemmata, tags)
        print(words)
        print(lemmata)
        print(tags)
        # for word, lemma, tag in zip(words, lemmata, tags):
        #     get_additionals(lemma, tag)
        print()
