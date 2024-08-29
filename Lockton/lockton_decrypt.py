import argparse
import binascii
import os
import shutil
from Crypto.Cipher import AES

def decrypt_file(file_path, key):
	with open(file_path, 'rb') as f:
		file_data = f.read()

	# The first 16 bytes are the IV
	iv = file_data[:16]
	encrypted_data = file_data[16:]

	# Create AES cipher in OFB mode
	cipher = AES.new(key, AES.MODE_OFB, iv=iv)

	# Decrypt the data
	decrypted_data = cipher.decrypt(encrypted_data)

	return decrypted_data

def process_files(input_file, key_hex, output_dir):
	# Convert hex key to bytes
	key = binascii.unhexlify(key_hex)

	# Ensure the output directory exists
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

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

			print(f"Decrypted {file_path} to {output_file_path}")
		except Exception as e:
			print(f"Failed to decrypt {file_path}: {str(e)}")

def restore_files(input_file, output_dir):
	with open(input_file, 'r') as f:
		file_paths = [line.strip() for line in f]

	for file_path in file_paths:
		decrypted_file = os.path.join(output_dir, os.path.basename(file_path) + '.decrypted')

		if os.path.exists(decrypted_file):
			try:
				# Move the decrypted file to the original location, overwriting the encrypted file
				shutil.move(decrypted_file, file_path)
				print(f"Restored {file_path} from {decrypted_file}")
			except Exception as e:
				print(f"Failed to restore {file_path}: {str(e)}")
		else:
			print(f"No decrypted file found for {file_path}")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Decrypt files encrypted by Lockton ransomware.')
	parser.add_argument('input_file', help='Path to the input file containing the list of files to decrypt.')
	parser.add_argument('key_hex', help='64-character hex string representing the AES key.')
	parser.add_argument('output_dir', help='Directory to save the decrypted files.')
	parser.add_argument('--restore', action='store_true', help='Restore the .decrypted files back to the original files.')

	args = parser.parse_args()

	if args.restore:
		restore_files(args.input_file, args.output_dir)
	else:
		process_files(args.input_file, args.key_hex, args.output_dir)
