import hashlib
import os
def calculate_md5(data):
    hash_md5 = hashlib.md5()
    
    # Check if the input is a file path or direct string data
    if isinstance(data, str) and os.path.isfile(data):
        # Treat as file path, read file contents
        with open(data, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    else:
        # Treat as string data
        hash_md5.update(data.encode('utf-8'))
    
    return hash_md5.hexdigest()


input_type = input("Do you want to input a file path (F) or a string (S)? ").strip().upper()

if input_type == 'F':
    input1 = input("Enter first file path: ")
    input2 = input("Enter second file path: ")
elif input_type == 'S':
    input1 = input("Enter first string: ")
    input2 = input("Enter second string: ")
else:
    print("Invalid input type selected!")
    exit()

output1 = calculate_md5(input1)
output2 = calculate_md5(input2)


print(f"MD5 of first input: {output1}")
print(f"MD5 of second input: {output2}")


if output1 == output2:
    print("File is not tampered")
else:
    print("FILE HAS BEEN TAMPERED!!")
