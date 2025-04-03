# Author: Pir00t
# Description: Decode Python scripts obfuscated by freecodingtools.orgs "Python Obfuscator. This was written to deobfuscate malware that has been encrypted for malicious intent and designed to assist Blue Teams in their analysis"

import argparse
import re
import zlib
from base64 import b64decode

def find_b64(data):
	# basic b64 match signature cater for initial strings and then byte strings received for processing
	if isinstance(data, str):
		b64_sig = re.compile(r'[A-Za-z0-9+/=]{30,}')
	elif isinstance(data, bytes):
		b64_sig = re.compile(rb'[A-Za-z0-9+/=]{30,}')
	
	match = re.search(b64_sig, data)
	if match:
		b64_string = match.group(0)

	return b64_string

def decode_data(data):
	decoded = b64decode(data[::-1])
	inflated_data = zlib.decompress(decoded)

	return inflated_data

def main():
	
	parser = argparse.ArgumentParser(description='Decode obfuscated Python from freecodingtools.org')
	parser.add_argument('-f', '--file', help='Path to the obfuscated Python script to be decoded')
	args = parser.parse_args()
	
	if not args.file:
		parser.print_help()
		return
	
	elif args.file:
		with open(args.file, 'r') as f:
			code = f.read()

		# testing shows that original script is encoded 50 times so loop 49 and final layer decode
		decoded = find_b64(code)
		for _ in range(49):
			result = decode_data(decoded)
			# extract b64 encoded data to be processed
			decoded = find_b64(result)

		final_layer = find_b64(result)
		orig_script = decode_data(final_layer)

		print(f'[+] Finished decoding\n\n{orig_script.decode()}\n')

		with open('decoded_script.txt', 'w') as f:
			f.write(orig_script.decode())

if __name__ == '__main__':
	main()