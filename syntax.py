import re


class Syntax(object):
    def __init__(self):
        pass

    def pattern(self):
        return 'plain-text'

    def newline(self):
        return True


class UrbanSyntax(Syntax):
    def __init__(self):
        pass

    def pattern(self, text):
        content = text.get_text().strip()
        # content = text.get_text().encode('utf8').strip()

        if not content:
            return 'none'

        if content.isdigit():  # page number
            return 'none'

        if 130 < text.x0 and text.x1 < 460:
            if text.height > 11:
                return 'heading-1'
            if text.height < 12:
                return 'heading-2'

        if 17.9 < text.height < 18.1:
            return 'heading-3'

        if 15.9 < text.height < 16.0:
            return 'heading-2'

        if 20.0 < text.height < 20.1:
            return 'heading-1'

        mo = re.search(r'^(I|II|III|IV|V|VI|VII|VIII|IX|X).', content)
        if mo:
            return 'heading-4'

        mo = re.search(r'^(（|\()(I|II|III|IV|V|VI|VII|VIII|IX|X)(）|\))', content)
        if mo:
            return 'heading-5'

        mo = re.search(r'^\d+\.', content)
        if mo:
            return 'ordered-list-item'

        if text.x0 < 90.1:  # special case for neihu page 2
            return 'unordered-list-item'

        return 'plain-text'

    def newline(self, text):
        # content = text.get_text().encode('utf8').strip()
        content = text.get_text() #.strip()

        if text.x0 < 90.1:  # special case for neihu page 2
            return True

        mo = re.search('\n\n$', content)
        if mo:
            return True

        mo = re.search('\.$', content)
        if mo:
            return True

        if text.x1 > 505.0:  # reach the right margin
            return False

        return False

    def purify(self, text):
        # content = text.get_text().encode('utf8').strip()
        content = text.get_text().strip()

        mo = re.match(r'(I|II|III|IV|V|VI|VII|VIII|IX|X). (.*)', content)
        if mo:
            return mo.group(2)

        mo = re.match(r'(（|\()(I|II|III|IV|V|VI|VII|VIII|IX|X)(）|\))(.*)', content)
        if mo:
            return mo.group(4)

        mo = re.match(r'^\d+、(.*)', content)
        if mo:
            return mo.group(1)

        return content
