import sys

if len(sys.argv) != 2:
    print("lsb.py [file.png]")
message = input("Input your super secret message: ")
message = ''.join(format(ord(i), 'b') for i in message)

png_array = [0]*4
pixel_data = []
message_iterator = 0

with open(sys.argv[1], "r+b") as f:
    flag = 0
    alpha_check = 0
    message_bool = 0
    #Read file byte by byte
    while True:
        current_byte = int.from_bytes(f.read(1), 'big')

        #Unique  IDAT specifier; will only alter pixel data
        if png_array[-4:] == [120,94,236,189]:
            flag = 1

        #Exit once the IEND sequence is found
        if png_array[-4:] == [174,66,96,130]:
            break

        #Alter LSB as long as there is a message
        if flag == 1 and message_iterator < len(message) and alpha_check%4 != 3:
            if message[message_iterator] == "1":
                message_bool = 1
            else:
                message_bool = 0
            png_array.append((current_byte >> 1 << 1) + message_bool)
            message_iterator += 1
            
        #Otherwise just copy the bytes over
        else:
            png_array.append(current_byte)
        alpha_check += 1
        

png_array = png_array[4:]
f.close()

newfile = open("encoded_" + sys.argv[1], "w+b")
newfile.write(bytearray(png_array))
newfile.close()
print("File created: encoded_" + sys.argv[1])
