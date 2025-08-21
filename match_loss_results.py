import re
import os

def extract_filename_from_path(path):
    """Extract the filename from a file path, preserving original extension"""
    return os.path.basename(path)

def main():
    # Read the mapping file
    mapping_dict = {}
    with open('results/hf_dataset_mapping.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if ':' in line:
                hash_key, path = line.split(':', 1)
                hash_key = hash_key.strip()
                path = path.strip()
                
                # Extract original filename from path (could be .mp3 or .wav)
                original_filename = extract_filename_from_path(path)
                if original_filename:
                    mapping_dict[hash_key] = {
                        'path': path,
                        'original_filename': original_filename
                    }
    
    # Read the loss results
    loss_dict = {}
    with open('results/loss_large.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if ':' in line and '.wav:' in line:
                # Split on ': ' to separate filename and loss value
                parts = line.split(': ', 1)
                if len(parts) == 2:
                    wav_file, loss_value = parts
                    wav_file = wav_file.strip()
                    loss_value = loss_value.strip()
                    
                    # Extract hash from wav filename (remove .wav extension)
                    if wav_file.endswith('.wav'):
                        hash_key = wav_file[:-4]  # Remove .wav extension
                        loss_dict[hash_key] = loss_value
    
    # Match and write results
    matched_results = []
    unmatched_hashes = []
    
    for hash_key in mapping_dict:
        if hash_key in loss_dict:
            original_filename = mapping_dict[hash_key]['original_filename']
            path = mapping_dict[hash_key]['path']
            loss_value = loss_dict[hash_key]
            
            matched_results.append({
                'hash': hash_key,
                'original_filename': original_filename,
                'path': path,
                'loss': loss_value
            })
        else:
            unmatched_hashes.append(hash_key)
    
    # Write matched results to output file - 只输出原始文件名和损失值
    with open('loss_large_match.txt', 'w', encoding='utf-8') as f:
        f.write("# Matched files with loss results\n")
        f.write("# Format: original_filename: loss_value\n\n")
        
        for result in matched_results:
            f.write(f"{result['original_filename']}: {result['loss']}\n")
        
        if unmatched_hashes:
            f.write("\n# Unmatched hashes (no loss data found):\n")
            for hash_key in unmatched_hashes:
                original_filename = mapping_dict[hash_key]['original_filename']
                f.write(f"# {original_filename}\n")
    
    print(f"Matching completed!")
    print(f"Total mappings found: {len(mapping_dict)}")
    print(f"Total loss results: {len(loss_dict)}")
    print(f"Successfully matched: {len(matched_results)}")
    print(f"Unmatched hashes: {len(unmatched_hashes)}")
    print(f"Results written to: loss_large_match.txt")

if __name__ == "__main__":
    main()