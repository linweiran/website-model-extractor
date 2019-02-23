import random
import hpack

HUFFMAN_PATH = "/home/streddy2/huffman-fix/chars.txt"

# dictionary of Huffman padded extensions
EXT_PADS = {
    'gif':  'aaz.gif',
    'html': 'ab.html',
    'woff': 'aa.woff',
    'js':   'aabb.js',
    'css':  'bbz.css'
}

# list of 7-bit huffman characters
HUFFMAN_CHARS = []
with open(HUFFMAN_PATH) as f:
    for line in f:
        HUFFMAN_CHARS.append(line.split('\n')[0])

# dictionary of used filenames for each site
USED_NAMES = {}

# FOR TESTING ONLY
# dictionary of generated filenames
#GEN_NAMES = {}


# FOR TESTING ONLY
# helper function for getting Huffman length of string
#def getHuffLen(text):
    #length = sum(hpack.huffman_constants.REQUEST_CODES_LENGTH[ord(c)] for c in text)
    #return length


def gen_filename(type, sitecounter):
    filename = ''
    # generate unique 3-char name
    while True:
        filename = ''
        for i in range(3):
            filename += random.choice(HUFFMAN_CHARS)

        if filename not in USED_NAMES[sitecounter]:
            USED_NAMES[sitecounter].add(filename)
            break

    # append extension
    filename += EXT_PADS[type]
    return filename

    # FOR TESTING ONLY
    #print(getHuffLen(rename))
    #GEN_NAMES[sitecounter].append(rename)


def sitegenerate(sitecounter):
    USED_NAMES[sitecounter] = set()

    # FOR TESTING ONLY
    #GEN_NAMES[sitecounter] = []

    for i in range(10):
        gen_filename('gif', sitecounter)
        gen_filename('html', sitecounter)
        gen_filename('woff', sitecounter)
        gen_filename('js', sitecounter)
        gen_filename('css', sitecounter)

for x in range(20):
    sitegenerate(x)

