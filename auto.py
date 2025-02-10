import base64
import json
import sys
import urllib.request


def modify_vmess_links(filename, new_remark):
    """
    Modifies the 'remark' field in all vmess:// links in a file.

    Args:
    filename (str): The path to the file containing the vmess links.
    new_remark (str): The new value for the 'remark' field.
    """
    try:
        with open(filename, "r+") as f:  # Open for reading and writing
            lines = f.readlines()
            f.seek(0)  # Rewind to the beginning of the file
            f.truncate()  # Clear the file

            for line in lines:
                line = line.strip()  # Remove leading/trailing whitespace
                if line.startswith("vmess://"):
                    try:
                        # Decode the Base64 string
                        base64_string = line[8:]  # Remove "vmess://" prefix
                        decoded_bytes = base64.b64decode(base64_string)
                        decoded_string = decoded_bytes.decode("utf-8")

                        # Parse the JSON object
                        config = json.loads(decoded_string)

                        # Modify the remark
                        config["ps"] = (
                            new_remark  # or config["remark"] depending on the key
                        )

                        # Encode back to Base64
                        modified_json_string = json.dumps(config, ensure_ascii=False)
                        modified_bytes = modified_json_string.encode("utf-8")
                        modified_base64_string = base64.b64encode(
                            modified_bytes
                        ).decode("utf-8")

                        # Write the modified vmess link back to the file
                        f.write("vmess://" + modified_base64_string + "\n")
                    except Exception as e:
                        print(f"Error processing line: {line}. Error: {e}")
                        # If there's an error, write the original line back
                        f.write(line + "\n")
                else:
                    # If the line is not a vmess link, write it back as is
                    f.write(line + "\n")
    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def download_file(url, filename):
    """Downloads a file from a URL."""
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"Downloaded file from {url} to {filename}")
    except Exception as e:
        print(f"Error downloading file from {url}: {e}")
        sys.exit(1)  # Exit if download fails


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python modify_vmess.py <url> <filename> <new_remark>")
        print("    <url>: URL to download the vmess links from")
        print("    <filename>: Local filename to save the downloaded links")
        print("    <new_remark>: The new remark to set")
        sys.exit(1)

    url = sys.argv[1]
    filename = sys.argv[2]
    new_remark = sys.argv[3]

    download_file(url, filename)
    modify_vmess_links(filename, new_remark)
    print("Finished processing the file.")
