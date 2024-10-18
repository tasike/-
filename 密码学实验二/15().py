def valid_pkcs7_padding(data: bytes) -> bool:
    # Get the value of the last byte, which represents the padding length
    padding_length = data[-1]
    
    # Check if the padding length is valid
    if padding_length == 0 or padding_length > len(data):
        return False
    
    # Check if all padding bytes are the same and equal to the padding length
    padding = data[-padding_length:]
    return all(byte == padding_length for byte in padding)

def strip_pkcs7_padding(data: bytes) -> bytes:
    # Check if the data has valid PKCS#7 padding
    if not valid_pkcs7_padding(data):
        raise ValueError("Invalid PKCS#7 padding.")
    
    # Strip off the padding
    padding_length = data[-1]
    return data[:-padding_length]

# Example Usage
def main():
    try:
        valid_data = b"ICE ICE BABY\x04\x04\x04\x04"
        print("Stripped valid data:", strip_pkcs7_padding(valid_data).decode())

        invalid_data = b"ICE ICE BABY\x05\x05\x05\x05"
        print("Stripped invalid data:", strip_pkcs7_padding(invalid_data).decode())
    except ValueError as e:
        print(e)

    try:
        invalid_data2 = b"ICE ICE BABY\x01\x02\x03\x04"
        print("Stripped invalid data2:", strip_pkcs7_padding(invalid_data2).decode())
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
