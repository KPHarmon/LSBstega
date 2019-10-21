import sys

def color_chooser(color_type):
    switch = {
        0: "Greyscale",
        2: "Truecolor",
        3: "Indexed-Color",
        4: "Greyscale with Alpha",
        6: "Truecolor with Alpha"
    }
    return switch.get(color_type, "Error")

def decrypt():
    f = open(sys.argv[1], "r+b")
    print("---------")
    
    #24 Bytes is the size of the complete PNG Header
    print("PNG Signature: ", end="")
    for i in range(8):
        print(str(int.from_bytes(f.read(1), 'big')), end =" ")
    print("\n\nIHDR Header Data:")
    
    #Read IDHR chunk
    f.read(8)
    width = int.from_bytes(f.read(4), 'big')
    height = int.from_bytes(f.read(4), 'big')
    bit_depth = int.from_bytes(f.read(1), 'big')
    image_type = color_chooser(int.from_bytes(f.read(1), 'big'))
    compression_method = int.from_bytes(f.read(1), 'big')
    print("\tWidth: " + str(width))
    print("\tHeight: " + str(height))
    print("\tBits Per Sample: " + str(bit_depth))
    print("\tImage Type: " + image_type)
    print("\tCompression Method: " + str(compression_method))
    

    #Search and Read Ancillary Chunks
    temp_array = [0]*3
    data = ""

    print("\nAncillary Chunks")
    #Search through file
    while True:
        data = ""
        #Read bytes 1 by 1
        temp_array.append(int.from_bytes(f.read(1), 'big'))
        
        #Check for special byte values
        check = temp_array[-4:]
        if check == [116,69,88,116]:
            data_size = temp_array[-5]

            #Read in data byte by byte (ignoring Null byte)
            for i in range(data_size):
                temp = f.read(1)
                if temp == b'\x00':
                    temp = b'\x2a'    
                data += str(temp)

                #strip garbage
                data = data.replace("b'", "")
                data = data.replace("'", "")
                data = data.replace("*", ": ")

            print("\t" + data)
        
        #Check for IEND
        if check == [73,69,78,68]:
            break
    
    f.close()
    print("---------")

def main():
    if len(sys.argv) != 2:
        print("Encryption: crypto.py [file.png]")
        return
    decrypt()

main()
