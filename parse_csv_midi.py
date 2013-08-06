import math
import copy

def parse_file_init(filename):
    f = open(filename)
    r = f.readlines()
    for s in r:
        s = s.split(', ')
            
    return r

def get_key_sig(filename):
    r = parse_file_init(filename)
    print r[0:10]
    for s in r:
        s = s.split(', ')
        if s[2] == 'Key_signature':
            print 'boomtown'
            key_sig_compare_notes = [[(int(s[3])+12*i) for i in range(8)],s[4][1:6]]
            break 
    return key_sig_compare_notes

def parse_voice(filename,voicenum):
    r = parse_file_init(filename)
    first_voice = []
    for s in r:
        if s[0] == str(voicenum+1):
            first_voice.append(s)
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
        first_voice[i][0] = first_voice[i][0]
    return first_voice

def voice_w_scale_degs(voice_with_no_rests,filename):
    voice_copy = copy.deepcopy(voice_with_no_rests)
    key_list = get_key_sig(filename)
    for entry in voice_copy:
        index = voice_copy.index(entry)
        for i in range(len(key_list[0])-1,-1,-1):
            note_num = key_list[0][i]
            potensh = entry[1]%note_num
            if potensh < 12:
                entry.append(potensh)
                break
    #change pitch information to up or down
    for i in range(1,len(voice_copy)-1):
        # getting rid of rhythm info, for now, by assigning to 0th entry
        voice_copy[i][0] = []
        note_before = voice_copy[i-1][1]
        note = voice_copy[i][1]
        note_after = voice_copy[i+1][1]
        if note_before < note:
            voice_copy[i][0].append(1) #for below
        elif note_before == note:
            voice_copy[i][0].append(0)
        else:
            voice_copy[i][0].append(1) #for above
        if note_after > note:
            voice_copy[i][0].append(1) #for goin up
        elif voice_copy[i-1][1] == voice_copy[i][1]:
            voice_copy[i][0].append(0)
        else:
            voice_copy[i][0].append(-1) #for goin down
    for entry in voice_copy:
        entry.remove(entry[1])

        

    return voice_copy




def eliminate_rests_from_voice(voice):
    voice_copy = copy.deepcopy(voice)
    for i in range(len(voice_copy)-1,-1,-1):
        if voice_copy[i][1] == 1:
            voice_copy.remove(voice_copy[i])
    return voice_copy

def make_voice_into_grams(voice_with_no_rests):
    voice_copy = copy.deepcopy(voice_with_no_rests)
    for i in range(len(voice_copy)-1):
        voice_copy[i][0] = voice_copy[i+1][0] - voice_copy[i][0]
        voice_copy[i][1] = voice_copy[i+1][1] - voice_copy[i][1]   
    for i in range(len(voice_copy)-1):
        try:
            voice_copy[i][0] = round(math.log((voice_copy[i+1][0]/float(voice_copy[i][0])),2),2)
        except ValueError:
            print voice_copy[i+1][0],voice_copy[i][0]

    return voice_copy




def make_voices(filename):
    voices = []
    for i in range(1,8):
        new_voice = parse_voice(filename,i)
        if len(new_voice) > 0:
            voices.append(new_voice)
    return voices

def rest_intervals(voice):
    intervals = []
    for i in range(len(voice)-1):
        if voice[i][1] == 1:
            intervals.append([])
            intervals[-1].append(voice[i][0])
            intervals[-1].append(voice[i+1][0])
    return intervals

def how_many_voices(time,voices):
    result = 0
    for voice in voices:
        for i in range(len(voice)-1):
            if voice[i][0] < time < voice[i+1][0] and voice[i][1] != 1:
                result += 1

    return result

def find_prelude_end(voices):
    potential_times = []
    for time in range(5000,5000000,1000):
        if how_many_voices(time,voices) == 0 and how_many_voices(time+2000,voices) == 1:
            return time
    #     if how_many_voices(time,voices) == 1 and how_many_voices(time+2000,voices) == 1:
    #         potential_times.append(time)

    # return potential_times






def find_longest_rest(rest_intervals):
    rest_lengths = []
    for entry in rest_intervals:
        rest_lengths.append(entry[1]-entry[0])
    index = rest_lengths.index(max(rest_lengths))
    return rest_intervals[index][0],max(rest_lengths)


def find_break(filename):
    '''to find the fugue in a prelude and fugue, for instance. will look for places where
    multiple voices are resting'''
    voices = make_voices(filename)
    ls_of_rests = [rest_intervals(voice) for voice in voices]
    longest_rests = [find_longest_rest(rest_intervals) for rest_intervals in ls_of_rests]
    first_try = longest_rests[-1][0]
    num_voices_resting = 0
    # for i in range(len(longest_rests)-1):
    #     if longest_rests[i][0] == first_try:
    #         result += 1
    # if result > 

    # for i in range(len(longest_rests)-1,-1,-1):
    #     if longest_rests[i][1] < 5000:
    #         longest_rests.remove(longest_rests[i])

    # #rests has same len as voices
    # c = i.combinations(rests,3)
    # combos = [elem for elem in c]
    # print combos[1]
    # # print type(combos)
    # # print len(combos)
    # # for i in range(1000,1000000,1000):
    # #     for combo_of_rests in combos:
    # #         result = 0
    # #         for i in range(3):
    # #             for 










