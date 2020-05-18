#SHA-1
#My attempt to enact SHA-1
#Please note that SHA-1 is well and truly broken at this point
#Sources:-
#https://en.wikipedia.org/wiki/SHA-1

def text2bin(message):

    output = ''
    for i in message:
        output += bin(ord(i))[2:].zfill(8)

    return output

#bitwise rotation of a number rotdist bits to
#the left inside the field defined by bit_length
def ROL(number, rotdist, bit_length):

    
    #make it a x bit binary number
    a = number.zfill(bit_length)
    #a

    #loop over the number of rotations needed
    for i in range(rotdist):

        #perform one rotation at a time
        b = ''
        #do the loop first. If it were not
        #for the looping we could use pythons
        #internal bitwise shift tools
        
        #move all the other elements in the string
        for l in range(bit_length - 1):

            b = b + a[l+1]
            
        b = b + a[0]
        #alter a to ensure perminance over
        #all the shifts in the code
        a = b

    #print a
    return a

#bitwise rotation of a number rotdist bits to
#the right inside the field defined by bit_length
def ROR(number, rotdist, bit_length):

    
    #make it a x bit binary number
    a = number.zfill(bit_length)
    #print a
    
    #loop over the number of rotations needed
    for i in range(rotdist):

        #perform one rotation at a time
        b = ''
        #do the loop first. If it were not
        #for the looping we could use pythons
        #internal bitwise shift tools
        b = b + a[bit_length - 1]
        #move all the other elements in the string
        for l in range(bit_length - 1):

            b = b + a[l]
            
        
        #alter a to ensure perminance over
        #all the shifts in the code
        a = b

    #print a
    return a


def logical_XOR(A, B):

    C = ''
    for i, b in enumerate(B):

        if A[i] != B[i]:
            C += '1'
        else: C+= '0'
    return C

def logical_AND(A, B):

    C = ''
    for i, b in enumerate(B):
        if A[i] == '1' and  B[i] == '1':
            C += '1'
        else: C += '0'
    return C

def logical_OR(A, B):

    C = ''
    for i, a in enumerate(A):
        if A[i] == '1' or B[i] == '1':
            C += '1'
        else: C += '0'
    return C

def logical_NOT(A):
    C = ''
    for i, a in enumerate(A):
        if a == '1':
            C += '0'
        else: C += '1'

    return C
'''
=================================================
====Now we start the SHA-1 specific functions====
=================================================
'''


def padding_function(message):
    
    #first convert the message to a string
    binary_message = text2bin(message)


    #record the initial message length for later
    message_length = len(binary_message)

    #add a one to the end of the message string. Now were in the
    #padding stage
    p = binary_message + '1'

    #extend the length of p until len(p)%512 = 448
    while len(p)%512 != 448:
        p += '0'

    #the final padding step, add the length of the starting message

    p += bin(message_length)[2:].zfill(64)

    block_no = int(len(p)/512)

    #splits the padded message into blocks
    blocks = []
    for i in range(block_no):

        blocks.append(p[i * 512: (i * 512) + 512])

    return blocks


def gen_keys(p):

    #Now enter the key generation step
    

    #count the number of keys we already have
    no_pad_keys = int(len(p)/32)

    #convert the string into a series of 32 bit words
    keys = []
    for i in range(no_pad_keys):
        keys.append(p[(i * 32):((i * 32) + 32)])

    #there is a mistake here. I only start at 16 because I am testing with such small messages. In reality
    #this step is simply run until 80 keys have been generated. This must be fixed
    for i in range(no_pad_keys, 80):

        #XOR the previously found keys together to get the new key
        new_key = logical_XOR(keys[i-3], keys[i-8])

        new_key = logical_XOR(new_key, keys[i-14])
        
        new_key = logical_XOR(new_key, keys[i-16])

        
        #Rotate the new key left by one position
        new_key = ROL(new_key, 1, 32)


        #save the new key
        keys.append(new_key)


    return keys

def gen_letters(keys, h0, h1, h2, h3, h4):

    #iniciate the first set of temporary values
    A = h0
    B = h1
    C = h2
    D = h3
    E = h4
    
    #work through all 80 rounds of the algorithm
    for i in range(80):
        #change up the way the function f works depending on the round
        #number
        if i <= 19:
            
            #f = (B & C) OR (!B & D)
            f = logical_OR(logical_AND(B, C), (logical_AND(logical_NOT(B), D)))
            k = bin(0x5A827999)[2:]

        elif 20 <= i <= 39:
            
            #f = B ^ C ^ D
            f = logical_XOR(logical_XOR(B, C), D)
            k = bin(0x6ED9EBA1)[2:]

        elif 40 <= i <= 59:

            #f = (B & C) OR (B & D) OR (C & D) 
            f = logical_OR(logical_OR(logical_AND(B, C), logical_AND(B, D)), logical_AND(C, D))
            k = bin(0x8F1BBCDC)[2:]


        elif 60 <= i <= 79:

            #f = B ^ C ^ D
            f = logical_XOR(logical_XOR(B, C), D)
            k = bin(0xCA62C1D6)[2:]


        #this is the meat of the round. Changing the values
        #of A, B, C, D and E
        temp = (int(ROL(A, 5, 32), 2) + int(f, 2) + int(E, 2) + int(k, 2) + int(keys[i], 2)) % pow(2,32)
        E = bin(int(D, 2))[2:]
        D = bin(int(C, 2))[2:]
        C = bin(int(ROL(B, 30, 32), 2))[2:]
        B = bin(int(A, 2))[2:]
        A = bin(temp)[2:]
        

        #pad back up to 32 bits
        A = A.zfill(32)
        B = B.zfill(32)
        C = C.zfill(32)
        D = D.zfill(32)
        E = E.zfill(32)

    return [A, B, C, D, E]

def collect_block_results(h0, h1, h2, h3, h4, A, B, C, D, E):

    #save the results from this block
    h0 = bin((int(h0, 2) + int(A, 2)) % pow(2,32))[2:].zfill(32)
    h1 = bin((int(h1, 2) + int(B, 2)) % pow(2,32))[2:].zfill(32)
    h2 = bin((int(h2, 2) + int(C, 2)) % pow(2,32))[2:].zfill(32)
    h3 = bin((int(h3, 2) + int(D, 2)) % pow(2,32))[2:].zfill(32)
    h4 = bin((int(h4, 2) + int(E, 2)) % pow(2,32))[2:].zfill(32)

    return [h0, h1, h2, h3, h4]



def SHA_1(message):

    #set up the initial values of the hash words
    h0 = '01100111010001010010001100000001'
    h1 = '11101111110011011010101110001001'
    h2 = '10011000101110101101110011111110'
    h3 = '00010000001100100101010001110110'
    h4 = '11000011110100101110000111110000'


    blocks = padding_function(message)

    #Split the thing to be hashed into blocks
    for block in blocks:

        #Generate 80x 32 bit words as the keys
        keys = gen_keys(block)
        

        #generate the ABCDE temperary variables that represent
        #the result from the round structure
        [A, B, C, D, E] = gen_letters(keys, h0, h1, h2, h3, h4)

        #collect the results from this block to be saved up for the next block
        [h0, h1, h2, h3, h4] = collect_block_results(h0, h1, h2, h3, h4, A, B, C, D, E)


    #This is the final hash. It should be 160 bits long
    result = h0 + h1 + h2 + h3 + h4

    #convert the final hash to hex
    result = hex(int(result,2))

    return result

'''
====================================================================
===== End of functions and begining of the code that uses them =====
====================================================================
'''


message = 'A Test'

#This function returns a hash of the input string in hex
result = SHA_1(message)

print(result)


    
