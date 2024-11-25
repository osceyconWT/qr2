from PIL import Image

def encode_data_to_image(data, output_file, image_size=(100, 100)):
    binary_data = ''.join(format(ord(c), '08b') for c in data)
    img = Image.new('RGBA', image_size, (0, 0, 0, 0))  
    pixels = img.load()
    data_index = 0

    for y in range(img.height):
        for x in range(img.width):
            if data_index + 5 < len(binary_data):  
                r = int(binary_data[data_index:data_index+2], 2) * 85  
                g = int(binary_data[data_index+2:data_index+4], 2) * 85
                b = int(binary_data[data_index+4:data_index+6], 2) * 85
                pixels[x, y] = (r, g, b)
                data_index += 6  
            else:
                pixels[x, y] = (0, 0, 0, 0)
    
    img.save(output_file)

def decode_data_from_image(image_path):
    img = Image.open(image_path).convert("RGBA")  
    pixels = img.load()
    binary_data = ''
    
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]  
            if a == 0:
                continue
            
            binary_data += format(r // 85, '02b')  
            binary_data += format(g // 85, '02b')
            binary_data += format(b // 85, '02b')
    
    decoded_data = ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))
    return decoded_data

print("welcome to QR2!")
print("i made this as a little test to see if i could exceed the data storage capabilities of QR, and i sure did accomplish that.")
print("QR can, at it's maximum (version 40) hold 3KB. my QR2 holds 7.5KB AT DEFAULT SIZE! this is around 7,500 characters of plaintext.")
print("obviously, this cannot be implemented like QR codes are implemented today, as many phone cameras would struggle to see each individual pixel as different color values. however it's good in other environments, like just general data storage.")
encodeordecode = input("would you like to encode text to image or decode image to text? ")

if encodeordecode.lower() == "encode":
    imgsize = input("image size? ")
    datatoencode = input("data to encode? ")
    filename = input("filename? ")
    encode_data_to_image(data=datatoencode, output_file=filename)
    input("saved as " + filename)
elif encodeordecode.lower() == "decode":
    filename = input("whats the image called? it has to be in this directory. ")
    output = input("what should the text file be called that we save it to? ")
    decoded_data = decode_data_from_image(filename)
    print("data found in " + filename + " is: " + decoded_data)
    with open(output, 'w') as outputfile:
        outputfile.write(decoded_data)
    print("saved to text file: " + output)