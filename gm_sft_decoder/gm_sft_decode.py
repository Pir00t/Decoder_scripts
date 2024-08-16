from base64 import b64decode

def get_mapping(encoded_str):
	decoded_str = b64decode(encoded_str[::-1])

	# result is mapping in reverse and also string, we need a dict
	mapping = eval(decoded_str[::-1])

	# also need to reverse the mapping in dict for decoding to work (discovered through testing)
	reversed_mapping = {v: k for k, v in mapping.items()}

	return reversed_mapping

def decode_string(encoded_str, chr_map):
	decoded_str = b64decode(encoded_str).decode()

	return ''.join(chr_map.get(char, char) for char in decoded_str)

def main():
	orig_string = 'KSxKbzskfndPIzh2TVRRM15qUTFealFgXmotYDxTOVRAKTwxKG0ldlRHOXVAM0J2Jkc+UShtIHxZIX4gUSE8NSZtTXZNX34gKDN+LTspMXdeM34sWSlAbWEpTXZAbT52O3xfLCV8Xyw7bV8sWW1GKkBTOCNeQ0p8JiVKcEB8PnZZKX50Oyk+YGElPnAmbl80XyRKaEBtQHBZfH52O3w1LiZ8RmsoLEo7.==weionI6IiKiwiIkJiOisjIsIiMiojI8JCLiIlI6IifiwiIiJiOiYiIsICSiojIkICLiolI6ICQiwiIOJiOiwjIsICWiojIhICLikmI6IyIiwiIXJiOikiIsICTiojIeJCLiknI6ICLiwiIzJiOi4iIsIiViojIfJCLignI6IiPiwiIwIiOiAmIsISRiojItICLiMmI6ICKiwiIsJiOiAiIsISViojIlISf'
	
	split_strings = orig_string.split('.')
	# Using cyberchef determined second half is key mapping in reverse
	mapping = get_mapping(split_strings[1])
	
	# now perform decode via substitution
	result = decode_string(split_strings[0], mapping)
	
	#result is b64 encoded so decode for reveal
	print(b64decode(result).decode())

if __name__ == '__main__':
	main()