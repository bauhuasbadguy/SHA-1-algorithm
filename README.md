# SHA-1 #

In this repo I have attempted to recreate SHA-1 in python in order to better understand how SHA-1 works.

The basic idea of the SHA-1 algorithm is to take in an arbitary number and then return a hash of that value 160 bits long.

The first step is to pad the input in order to generate the keys W<sub>t</sub>. This is done by first converting the message to binary. Then a 1 is appended to the message followed by a series of zeros until the length of the message satisfies

len(m) % 512 = 448 --- (1)

Now the final padding step is to add the original length of the message expressed in binary to the end of the message resulting in a padded message which can be broken down into 32 bit parts which will be used to generate a series of 80 32 bit keys.

The first keys are the 32 bit padding values we just generated, the rest of the keys are generated using the logic shown below:

k<sub>i</sub> = XOR(XOR(XOR(<sub>ki-3</sub>, k<sub>i-8</sub>), k<sub>i-14</sub>), k<sub>i-16</sub>)

this is then rotated left by one position and stored as the new key until 80 keys are generated in total. These keys are then used as the values of W<sub>t</sub> in the compression function shown below.

<p align="center">
<image src='./SHA-1-diagram.png'></image>
</p>

This function shows one round of the compression function which will be run for 80 rounds resulting in the 160 bit output. 

When the compression function starts the values of A-E are set to:

A - 0x67452301
B - 0xEFCDAB89
C - 0x98BADCFE
D - 0x10325476
E - 0xC3D2E1F0

each of which is 32 bits long. The values k<sub>t</sub> changes every 20 rounds as does the behaviour of the function F. The value of W<sub>t</sub> is different in each round since it is set by the keys we generated before starting the compression function. The behavour of F is as follows:

F<sub>0-19</sub> = 

### Sources ###

* https://en.wikipedia.org/wiki/SHA-1
* http://quadibloc.com/crypto/mi060501.htm
* https://medium.com/bugbountywriteup/breaking-down-sha-1-algorithm-c152ed353de2
* https://cse.unl.edu/~ssamal/crypto/genhash.php

