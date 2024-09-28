# Dark Angels
A POC script to decrypt files that have been encrypted by Dark Angels ransomware (Linux 2023-24 variant).

Blog post on the ransomware [here]()

_Note: this POC only works by grabbing the key from memory while debugging. The script has been developed to see if it was possible to decrypt the files and work ongoing to see if the key can be retrieved by other means._

## Prerequisites
Either:

- Run a find commmand and locate all **.crypted** files and append the absolute paths to a file
- Establish the path to wrkman.log / wrkman.log.0

## Python 3
Run the script as below:

Test decryption to a specified output directory:

`python ./da_decrypt.py <file containing list of enc files> <AES Key> <output_dir>`

If successful and you wish to overwrite the original files with the decrypted ones:

`python ./da_decrypt.py <file containing list of enc files> <AES Key> <output_dir> --restore`
