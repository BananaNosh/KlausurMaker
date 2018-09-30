from cltk.corpus.utils.importer import CorpusImporter
from cltk.stem.latin.declension import CollatinusDecliner
from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer
from cltk.stem.lemma import LemmaReplacer
from cltk.tag.pos import POSTag
from cltk.exceptions import UnknownLemma
import re
import string
import numpy as np
from collections import OrderedDict


PUNCTUATION_SIGNS = [".", ",", ";", ":", "!", "?"]


class VocabExtracter:
    def __init__(self):
        corpus_importer = CorpusImporter("latin")
        corpus_importer.import_corpus("latin_models_cltk")
        self.se_tokenizer = TokenizeSentence('latin')
        self.wo_tokenizer = WordTokenizer("latin")
        self.lemmatizer = LemmaReplacer("latin")
        self.pos_tagger = POSTag("latin")

    @staticmethod
    def get_additionals(lemma, tag):
        tag_info = tag[1]
        if tag_info is None:
            return None
        declination = None
        try:
            decliner = CollatinusDecliner()
            if tag_info[0] == "N":
                declination = decliner.decline(lemma)
                if declination[0][1][0] == "v":
                    return None
                return declination[3][0] + " " + tag_info[6].lower()
            if tag_info[0] == "A":
                declination = decliner.decline(lemma)
                if declination[0][1][0] == "v":
                    return None
                if len(declination) < 100:
                    print("strange decl", lemma, declination)
                    return declination[3][0]
                fem_form = declination[13][0]
                net_form = declination[26][0]
                if fem_form == net_form:
                    return declination[3][0]
                return fem_form + " " + net_form
            if tag_info[0] == "V":
                declination = decliner.decline(lemma)
                return declination[67][0] + " " + declination[18][0]
        except UnknownLemma as e:
            print(e)
        except KeyError as e:
            print(e)
        except IndexError as e:
            print(e, lemma, tag, declination if declination else None)
        return None

    @staticmethod
    def sanitize(words, lemmata, tags):
        new_words = words.copy()
        lemmata_to_change = []
        tags_to_change = []
        if len(words) != len(tags):
            did_correct = 0, False
            for i, word in enumerate(words):
                if did_correct[1]:
                    did_correct = did_correct[0], False
                    continue
                moved_index = i - did_correct[0]
                tag = tags[moved_index]
                if word != tag[0]:
                    if i < len(words) - 1 and word + words[i + 1] == tag[0]:
                        new_words[moved_index] = word + words[i + 1]
                    elif i < len(words) - 1 and words[i + 1] + word == tag[0]:
                        new_words[moved_index] = words[i + 1] + word
                    elif i < len(words) - 1 and word + words[i + 1][1:] == tag[0]:  # mortuos -que
                        new_words[moved_index + 1] = new_words[moved_index + 1][1:]
                        lemmata[moved_index + 1] = lemmata[moved_index + 1][1:]
                        tags_to_change.append(moved_index)
                        tags_to_change.append(moved_index + 1)
                        tags.insert(moved_index + 1, (new_words[moved_index + 1], None))
                        did_correct = did_correct[0], True
                        continue
                    else:
                        raise AssertionError("tags and words differ", word, tag)
                    lemmata_to_change.append(moved_index)
                    del new_words[moved_index + 1]
                    del lemmata[moved_index + 1]
                    did_correct = did_correct[0] + 1, True
            if len(lemmata_to_change) > 0:
                new_lemmata = LemmaReplacer("latin").lemmatize([new_words[index] for index in lemmata_to_change])
                for index, lemma in zip(lemmata_to_change, new_lemmata):
                    lemmata[index] = lemma
            words_needing_new_tag = [new_words[index] for index in tags_to_change]
            new_tags = POSTag("latin").tag_ngram_123_backoff(" ".join(words_needing_new_tag))
            for index, tag in zip(tags_to_change, new_tags):
                tags[index] = tag
        lemmata = [lemma.rstrip(string.digits) for lemma in lemmata]
        return new_words, lemmata, tags, (np.array(tags_to_change[::2]) - np.arange(len(tags_to_change) // 2))

    def extract_vocabs(self, text):
        sentences = self.se_tokenizer.tokenize(text)
        # test if sentence start with numbers
        number_re = re.compile("\d+")
        sentence_count = len(sentences)
        sentences_with_number = [number_re.match(sentence) is not None for sentence in sentences]
        sentences_with_number_count = np.sum(sentences_with_number)
        starts_with_numbers = sentences_with_number_count >= sentence_count / 3
        if starts_with_numbers and sentences_with_number_count < sentence_count:
            sentences = [sentence.strip() + " " + sentences[i + 1].strip()
                         if i < len(sentences) - 1 and not sentences_with_number[i + 1]
                         else sentence.strip() for i, sentence in enumerate(sentences) if sentences_with_number[i]]

        vocabs = []
        for i, sentence in enumerate(sentences):
            if starts_with_numbers and not sentence.startswith(str(i + 1)):
                print(f"sentence number incorrect should be {i+1}")
            words = [word for word in self.wo_tokenizer.tokenize(sentence) if word not in PUNCTUATION_SIGNS
                     and not number_re.match(word)]
            lemmata = self.lemmatizer.lemmatize(words)
            tags = [tag for tag in self.pos_tagger.tag_ngram_123_backoff(sentence) if tag[0] not in PUNCTUATION_SIGNS
                    and not number_re.match(tag[0])]
            words, lemmata, tags, splitted_indices = self.sanitize(words, lemmata, tags)
            print(words)
            print(lemmata)
            print(tags)
            print(splitted_indices)
            additionals = []
            for word, lemma, tag in zip(words, lemmata, tags):
                additionals.append(self.get_additionals(lemma, tag))
            print(additionals)
            original_indices = np.arange(len(words))
            for splitted_index in splitted_indices:
                original_indices -= np.where(original_indices > splitted_index, 1, 0)
            print(original_indices)
            vocabs.append(list(zip(words, lemmata, additionals, original_indices)))
            print()

        vocabs = self.make_unique(vocabs)
        return vocabs, starts_with_numbers, sentences

    @staticmethod
    def make_unique(vocabs):
        for i, sentence in enumerate(vocabs):
            new_vocabs = OrderedDict()
            for vocab in sentence:
                key = f"{vocab[1]}_{vocab[2]}"
                if key not in new_vocabs:
                    new_vocabs[key] = vocab
                else:
                    original_indices = new_vocabs[key][3]
                    if type(original_indices) is not list:
                        original_indices = [original_indices]
                    original_indices.append(vocab[3])
                    new_vocabs[key] = new_vocabs[key][0], new_vocabs[key][1], new_vocabs[key][2], original_indices
            vocabs[i] = list(new_vocabs.values())
        return vocabs


if __name__ == '__main__':
    with open("./test_text.txt", "r") as f:
        test_text = f.read()

    vocabs, starts_with_numbers, sentences = VocabExtracter().extract_vocabs(test_text)
    print(vocabs, starts_with_numbers, sentences)
