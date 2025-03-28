# IMAGE ENCRYPTION USING AES-256 CBC

# Import necessary libraries for encryption
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os  # Used to generate random keys and handle file operations

# Function to generate a secure random key for AES encryption
def generate_key():
    return os.urandom(32)  # Generates a 32-byte (256-bit) AES key

# Function to encrypt an image
def encrypt_image(image_path, key):
    # Generate a random 16-byte Initialization Vector (IV) for CBC mode
    iv = os.urandom(16)

    # Create AES cipher using the key and IV in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()  # Create an encryptor object

    with open(image_path, 'rb') as f:
        image_data = f.read()

    # Apply padding to make data length a multiple of 16 bytes (AES block size)
    padder = padding.PKCS7(128).padder()  # PKCS7 padding ensures proper encryption
    padded_data = padder.update(image_data) + padder.finalize()

    # Encrypt the padded data and overall data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Save the encrypted file with the original filename + ".bin" extension
    encrypted_path = image_path + ".bin"
    with open(encrypted_path, 'wb') as f:
        f.write(iv + encrypted_data)

    print(f"Image encrypted successfully: {encrypted_path}")

# Function to decrypt an encrypted image
def decrypt_image(encrypted_path, key, output_path):
    # Open the encrypted file and extract the IV and encrypted data
    with open(encrypted_path, 'rb') as f:
        iv = f.read(16)  # First 16 bytes are the IV
        encrypted_data = f.read()  # The rest is encrypted image data

    # Create AES cipher for decryption using the same key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()  # Create a decryptor object

    # Decrypt the encrypted data
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove padding to restore original image data
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    # Save the decrypted image with a new filename starting with "decrypted_"
    with open(output_path, 'wb') as f:
        f.write(decrypted_data)

    print(f"Image decrypted successfully: {output_path}")


if __name__ == "__main__":
    # Generate a secure AES-256 key
    key = generate_key()
    print("Generated Key (Save this!):", key.hex())

    # Ask the user to input the path of the image they want to encrypt
    image_path = input("Enter the path of the image to encrypt: ").strip()

    # Define the paths for encrypted and decrypted images
    encrypted_path = image_path + ".bin"  # Encrypted file will have ".bin" extension
    decrypted_path = "decrypted_" + image_path  # Decrypted file gets "decrypted_" prefix

    # Perform encryption and decryption
    encrypt_image(image_path, key)  # Encrypt the image
    decrypt_image(encrypted_path, key, decrypted_path)  # Decrypt the image
