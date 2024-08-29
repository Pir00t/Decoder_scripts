# Lockton
A script to decrypt files that have been encrypted by Lockton ransomware.

Blog post on the ransomware [here](https://ultimacybr.co.uk/2024-08-29-Lockton/)

_Note: this appears to be an early version of the ransomware given the hardcoded values but the script may be useful to some people either way_

## Python 3
Run the script as below:

Test decryption to a specified output directory:

`python .\lockton_decrypt.py <file containing list of enc files> <AES Key> <output_dir>`

If successful and you wish to overwrite the original files with the decrypted ones:

`python .\lockton_decrypt.py <file containing list of enc files> <AES Key> <output_dir> --restore`
