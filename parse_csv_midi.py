

def parse_file(filename,voicenum):
    f = open(filename)
    r = f.readlines()
    first_voice = []
    for s in r:
        if s[0] == str(voicenum+1):
            first_voice.append(s)
    print first_voice[0:10]
    indices_to_remove = []
    for i in range(len(first_voice)):
        first_voice[i] = first_voice[i].split(', ')
        if len(first_voice[i]) == 6:
            first_voice[i].remove(first_voice[i][5])
            first_voice[i].remove(first_voice[i][3])
            first_voice[i].remove(first_voice[i][0])
    print first_voice[0:10]

    for i in range(len(first_voice)-1,-1,-1):
        if first_voice[i][1][0:8] == 'Note_off' and int(first_voice[i+1][0])!= int(first_voice[i][0]):
            # change note offset entry to rest entry
            first_voice[i] = [int(first_voice[i][0]),1]
        elif first_voice[i][1][0:8] == 'Note_off':
            first_voice.remove(first_voice[i])


    for i in range(len(first_voice)-1,-1,-1):
        for j in range(len(first_voice[i])-1,-1,-1):
            try:
                first_voice[i][j] = int(first_voice[i][j])
            except ValueError:
                first_voice[i].remove(first_voice[i][j])  

    for i in range(len(first_voice)-1,-1,-1):
        if first_voice[i][-1] == 0 or first_voice[i][0] < 100:
            first_voice.remove(first_voice[i])

    for i in range(len(first_voice)):
        first_voice[i][0] = first_voice[i][0]/256.0
    return first_voice


def make_voice_into_grams(voice):
    for i in range(len(voice)+1):
        voice[i][0] = voice[i+1][0] - voice[i][0]
        voice[i][1] = voice[i+1][1] - voice[i][1]

def make_voices(filename):
    voices = []
    for i in range(1,8):
        new_voice = parse_file(filename,i)
        if len(new_voice) > 0:
            voices.append(new_voice)
    return voices

def find_break(filename):
    '''to find the fugue in a prelude and fugue'''
    voices = make_voices(filename)




