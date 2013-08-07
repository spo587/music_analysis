import math
import copy
import os

def parse_file_init(filename):
    f = open(filename)
    r = f.readlines()
    for s in r:
        s = s.split(', ')
            
    return r

def get_key_sig(filename):
    r = parse_file_init(filename)
    #print r[0:10]
    for s in r:
        s = s.split(', ')
        if s[2] == 'Key_signature':
            #print 'boomtown'
            key_sig_compare_notes = [[(int(s[3])+12*i) for i in range(8)],s[4][1:6]]
            break 
    return key_sig_compare_notes

def get_key_sig_manual(key,quality):
    '''key is the number of half-steps away from c. basically a repeat of function above
    but in case you want to just input key yourself!'''
    return [[(key+12*i) for i in range(8)],quality]


def parse_voice(filename,voicenum):
    r = parse_file_init(filename)
    first_voice = []
    for s in r:
        if s[0] == str(voicenum+1):
            first_voice.append(s)
    for i in range(len(first_voice)-1,-1,-1):
        first_voice[i] = first_voice[i].split(', ')
        if len(first_voice[i]) == 6:
            first_voice[i].remove(first_voice[i][5])
            first_voice[i].remove(first_voice[i][3])
            first_voice[i].remove(first_voice[i][0])





    for i in range(len(first_voice)-1,-1,-1):
        # if type(first_voice[i][1]) != str or first_voice[i][1][0] != 'N':
        #     first_voice.remove(first_voice[i])
        if first_voice[i][1][0:8] == 'Note_off' and int(first_voice[i+1][0])!= int(first_voice[i][0]):
            # change note offset entry to rest entry
            first_voice[i] = [int(first_voice[i][0]),1]
        elif first_voice[i][1][0:8] == 'Note_off':
            first_voice.remove(first_voice[i])

        # try:
        #     print first_voice[i][1][0]
        # except TypeError:
        #     print first_voice[i][1],first_voice[i]
        



    for i in range(len(first_voice)-1,-1,-1):
        for j in range(len(first_voice[i])-1,-1,-1):
            try:
                first_voice[i][j] = int(first_voice[i][j])
            except ValueError:
                first_voice[i].remove(first_voice[i][j])  

    for i in range(len(first_voice)-1,-1,-1):
        if first_voice[i][-1] == 0 or first_voice[i][0] < 100:
            first_voice.remove(first_voice[i])
    if len(first_voice) > 0 and first_voice[0][1] < 20:
        first_voice.remove(first_voice[0])

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

def how_many_voices(time,voices_w_rests):
    result = 0
    for voice in voices_w_rests:
        for i in range(len(voice)-1):
            if voice[i][0] <= time < voice[i+1][0] and voice[i][1] != 1:
                result += 1

    return result

def find_prelude_end(voices_w_rests):
    potential_times = []
    for time in range(5000,5000000,1000):
        if how_many_voices(time,voices_w_rests) == 0 and how_many_voices(time+2000,voices_w_rests) == 1:
            print 'prelude end ', time
            return time
    #     if how_many_voices(time,voices) == 1 and how_many_voices(time+2000,voices) == 1:
    #         potential_times.append(time)

    # return potential_times

def eliminate_prelude(voices_w_rests):
    voices_copy = copy.deepcopy(voices_w_rests)
    end = find_prelude_end(voices_w_rests)
    print 'prelude end ', end
    modified_voices = []
    for voice in voices_copy:
        voice_copy = copy.deepcopy(voice)
        for i in range(len(voice_copy)-1,-1,-1):
            if voice_copy[i][0] <= end:
                voice_copy.remove(voice[i])
        modified_voices.append(voice_copy)
    #find min time
    first_onsets = []
    for voice in modified_voices:
        first_onsets.append(voice[0][0])
    first_onset = min(first_onsets)
    for voice in modified_voices:
        for entry in voice:
            entry[0] = entry[0] - first_onset

    return modified_voices
    

def find_fugue_subject_end(fugue_only_voices):
    '''assume the file has already been pruned so only contains the fugue'''
    for time in range(256,50000,256):
        if how_many_voices(time,fugue_only_voices) > 1:
            return time


def get_fugue_subject(fugue_only_voices):
    end = find_fugue_subject_end(fugue_only_voices)
    voices_copy = copy.deepcopy(fugue_only_voices)
    #iterate through the 4 voices backward
    for i in range(len(voices_copy)-1,-1,-1):
        #iterate through the entries in the voice backward
        for j in range(len(voices_copy[i])-1,-1,-1):
            if voices_copy[i][j][0] >= end:
                voices_copy[i].remove(voices_copy[i][j])
    for voice in voices_copy:
        if len(voice) > 2:
            first_voice = voice
    return first_voice
    





if __name__ == '__main__':
    #files = ['wtc2032.mid.txt']
    
    files = os.listdir('.')
    wtc = []
    for filename in files:
        if filename[-8:] == '.mid.txt':
            wtc.append(filename)
    fugue_subjects = []
    print wtc
    for filename in wtc:
        voices = make_voices(filename)
        # voices_no_rests = []
        # for i in range(len(voices)):
        #     voices_no_rests.append(eliminate_rests_from_voice(voices[i]))
        #for i in range(3):
            #print 'voices with no rests beginnings ', voices[i][0:10]
        fugue_only_voices = eliminate_prelude(voices)
        # for i in range(3):
        #     print 'fugue only voices ', fugue_only_voices[i][0:10]
        fugue_subject = get_fugue_subject(fugue_only_voices)
        fugue_subjects.append(fugue_subject)
        print 'updated fugue subjects ', fugue_subjects
    print fugue_subjects






    













