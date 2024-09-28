import argparse
import binascii
import os
import re
import shutil
from Crypto.Cipher import AES

def decrypt_file(file_path, key):
	with open(file_path, 'rb') as f:
		file_size = os.path.getsize(file_path)
		file_data = f.read()

	# encrypted data worked out by total file size minus 177 bytes (appended blocks 113 + 64)
	size_encrypted = file_size - 177

	# Ensure the remainder is a multiple of 16
	if size_encrypted % 16 != 0:
		raise ValueError('[!] The remainder is not a multiple of 16. Please check the appended bytes or encryption method.')

	encrypted_data = file_data[:size_encrypted]
	#print(encrypted_data.hex())

	# IV is first 16 bytes of an appended 64 byte block at the end of each file
	end_block = file_data[-64:]
	iv = end_block[:16]
	print(f'[*] IV: {iv.hex()}')
	
	# Create AES cipher in CBC mode
	cipher = AES.new(key, AES.MODE_CBC, iv=iv)

	# Decrypt the data
	decrypted_data = cipher.decrypt(encrypted_data)

	return decrypted_data

def process_files(input_file, key_hex, output_dir):
	# Convert hex key to bytes
	key = binascii.unhexlify(key_hex)

	# Ensure the output directory exists
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	if 'wrkman.log' in input_file:
		with open(input_file, 'r') as f:
			items = [line.strip() for line in f if 'Done' in line]
			
		file_paths = []
		for item in items:
			match = re.search(r"Done: (.+)", item)
			if match:
				file_paths.append(match.group(1))

	else:
		with open(input_file, 'r') as f:
			file_paths = [line.strip() for line in f]

	for file_path in file_paths:
		try:
			decrypted_data = decrypt_file(file_path, key)

			# Determine the output file path
			output_file_path = os.path.join(output_dir, os.path.basename(file_path) + '.decrypted')

			# Write the decrypted data to a new file
			with open(output_file_path, 'wb') as decrypted_file:
				decrypted_file.write(decrypted_data)

			print(f'[+] Decrypted {file_path} to {output_file_path}')
		except Exception as e:
			print(f'[!] Failed to decrypt {file_path}: {str(e)}')

def restore_files(input_file, output_dir):
	if 'wrkman.log' in input_file:
		with open(input_file, 'r') as f:
			items = [line.strip() for line in f if 'Done' in line]
			
		file_paths = []
		for item in items:
			match = re.search(r"Done: (.+)", item)
			if match:
				file_paths.append(match.group(1))

	else:
		with open(input_file, 'r') as f:
			file_paths = [line.strip() for line in f]

	for file_path in file_paths:
		decrypted_file = os.path.join(output_dir, os.path.basename(file_path) + '.decrypted')

		if os.path.exists(decrypted_file):
			try:
				# Move the decrypted file to the original location, overwriting the encrypted file
				shutil.move(decrypted_file, file_path)
				print(f'[+] Restored {file_path} from {decrypted_file}')
			except Exception as e:
				print(f'[!] Failed to restore {file_path}: {str(e)}')
		else:
			print(f'[!] No decrypted file found for {file_path}')

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Decrypt files encrypted by Dark Angels ransomware (2023/2024 Linux variant).')
	parser.add_argument('input_file', help='Path to the wrkman.log(.0) or input file containing the list of files to decrypt.')
	parser.add_argument('key_hex', help='64-character hex string representing the AES key.')
	parser.add_argument('output_dir', help='Directory to save the decrypted files.')
	parser.add_argument('--restore', action='store_true', help='Restore the .decrypted files back to the original files.')

	args = parser.parse_args()

	if args.restore:
		restore_files(args.input_file, args.output_dir)
	else:
		process_files(args.input_file, args.key_hex, args.output_dir)
