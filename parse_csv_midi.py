

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
        if first_voice[i][-1] == 0:
            first_voice.remove(first_voice[i]) 



    return first_voice

