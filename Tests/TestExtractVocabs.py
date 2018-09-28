import unittest
from cltk.tokenize.word import WordTokenizer
from cltk.stem.lemma import LemmaReplacer
from cltk.tag.pos import POSTag
import re
from extract_vocabs import PUNCTUATION_SIGNS, VocabExtracter


class ExtractVocabTest(unittest.TestCase):
    def setUp(self):
        self.extracter = VocabExtracter()

    def test_sanitize(self):
        number_re = re.compile("\d+")
        sentence = "tecum omnis tecum tecum rexque reginaque sub in dominusque at dominaque"
        words = [word for word in self.extracter.wo_tokenizer.tokenize(sentence) if word not in PUNCTUATION_SIGNS
                 and not number_re.match(word)]
        lemmata = self.extracter.lemmatizer.lemmatize(words)
        tags = [tag for tag in self.extracter.pos_tagger.tag_ngram_123_backoff(sentence)
                if tag[0] not in PUNCTUATION_SIGNS and not number_re.match(tag[0])]
        words, lemmata, tags, splitted_indices = self.extracter.sanitize(words, lemmata, tags)
        print(words)
        print(lemmata)
        print(tags)
        print(splitted_indices)

        for word, lemma, tag in zip(words, lemmata, tags):
            self.assertEqual(word, tag[0])

        expected = ['tu', 'omne', 'tu', 'tu', 'rex', 'que', 'regina', 'que', 'sub', 'in', 'dominus', 'que', 'at',
                    'domina', 'que']
        self.assertEqual(expected, lemmata)
        self.assertEqual([4, 5, 8, 10], list(splitted_indices))

    def test_extract(self):
        text = "tecum omnis tecum tecum rexque reginaque sub in dominusque at dominaque"
        vocabs = self.extracter.extract_vocabs(text)
