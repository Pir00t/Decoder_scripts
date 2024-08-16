# FCTDecode
Methods for deobfuscating malware using Free Coding Tools 'Python Obfuscator'

## Python 3
Run the script as below:

`python FCTdecode.py -f <obfuscated_file.py>`

## CyberChef
- Use this [recipe](https://gchq.github.io/CyberChef/#recipe=Regular_expression('User%20defined','%5BA-Za-z0-9%2B/%3D%5D%7B30,%7D',true,true,false,false,false,false,'List%20matches')Label('top')Reverse('Character')From_Base64('A-Za-z0-9%2B/%3D',true,false)Zlib_Inflate(0,0,'Adaptive',false,false)Regular_expression('User%20defined','%5BA-Za-z0-9%2B/%3D%5D%7B30,%7D',true,true,false,false,false,false,'List%20matches')Jump('top',48)Reverse('Character')From_Base64('A-Za-z0-9%2B/%3D',true,false)Zlib_Inflate(0,0,'Adaptive',false,false)&oenc=65001)
- Copy and paste or open the obfuscated script
- Voila (hopefully!)
