import io
import sys

def check_header(header_data):

    #Validates the header input parameters.
    validation_result = {"valid": True, "error": None}

    # Check if header contains exactly three numbers
    if len(header_data) != 3:
        validation_result["valid"] = False
        validation_result["error"] = "Error: Chybna hlavicka souboru!"
        return validation_result

    # Check maximum value
    if header_data[0] <= 0:
        validation_result["valid"] = False
        validation_result["error"] = "Error: Maximum neni kladne!"
        return validation_result

    # Verify sort type
    valid_sort_types = {0, 1, 2}
    if header_data[1] not in valid_sort_types:
        validation_result["valid"] = False
        validation_result["error"] = "Error: Neznamy typ razeni posloupnosti!"
        return validation_result

    # Check virus flag
    if header_data[2] not in [0, 1]:
        validation_result["valid"] = False
        validation_result["error"] = "Error: Nelze urcit, zda posloupnost napadl virus!"
        return validation_result

    return validation_result

def validate_element(value, max_limit):

    # Ensures the number is within valid range.
    return 0 < value <= max_limit

def check_order(element, position, elements, order_type):

    #Validates if the element follows the specified sorting order.
    if position == 0:
        return True

    previous = elements[position - 1]
    if order_type == 1 and element < previous:
        return False
    if order_type == 2 and element > previous:
        return False
    return True

def validate_sequence_length(data):
    
    #Checks if the sequence length is within allowed bounds.
    result = {"valid": True, "error": None}
    length = len(data)

    if length < 1000:
        result["valid"] = False
        result["error"] = "Error: Posloupnost ma mene nez 1000 prvku!"
    elif length > 2000000:
        result["valid"] = False
        result["error"] = "Error: Posloupnost ma vic nez 2000000 prvku!"
    
    return result

def perform_counting_sort(data, max_value):

    #Implements counting sort for small ranges.
    counts = [0] * (max_value + 1)
    
    # Count occurrences
    for item in data:
        counts[item] += 1
    
    # Construct the output sequence
    sorted_data = []
    for idx, count in enumerate(counts):
        sorted_data.extend([idx] * count)
    
    return sorted_data

def apply_insertion_sort(items):
    #Performs insertion sort for small sequences or virus case.

    sorted_items = items.copy()
    for idx in range(1, len(sorted_items)):
        current = sorted_items[idx]
        pos = idx - 1
        while pos >= 0 and sorted_items[pos] > current:
            sorted_items[pos + 1] = sorted_items[pos]
            pos -= 1
        sorted_items[pos + 1] = current
    return sorted_items

def execute_merge_sort(data):
    #Implements merge sort with insertion sort optimization for small sequences.

    if len(data) <= 1:
        return data
    if len(data) <= 10:
        return apply_insertion_sort(data)

    mid_point = len(data) // 2
    left_part = execute_merge_sort(data[:mid_point])
    right_part = execute_merge_sort(data[mid_point:])

    return merge_parts(left_part, right_part)

def merge_parts(left, right):
    # Combines two ordered sequences

    merged = []
    left_idx, right_idx = 0, 0

    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] <= right[right_idx]:
            merged.append(left[left_idx])
            left_idx += 1
        else:
            merged.append(right[right_idx])
            right_idx += 1

    merged.extend(left[left_idx:])
    merged.extend(right[right_idx:])
    return merged

def select_sorting_method(data, max_value):

    #Chooses the appropriate sorting algorithm based on maximum value.
    return perform_counting_sort(data, max_value) if max_value <= 10000 else execute_merge_sort(data)

# Input processing
input_buffer = io.BytesIO()
chunk_size = 4096

while True:
    data_chunk = sys.stdin.buffer.read(chunk_size)
    if not data_chunk:
        break
    input_buffer.write(data_chunk)

input_content = input_buffer.getvalue().decode().splitlines()
header_info = [int(x) for x in input_content[0].split() if x.strip()]
sequence_data = [int(line) for line in input_content[1:] if line.strip()]

# Input validation
header_check = check_header(header_info)
if not header_check["valid"]:
    sys.stderr.write(f"{header_check['error']}\n")
    sys.exit(1)

for idx, value in enumerate(sequence_data):
    if not validate_element(value, header_info[0]):
        sys.stderr.write("Error: Prvek posloupnosti je mimo rozsah!\n")
        sys.exit(1)
    
    if header_info[2] != 1 and header_info[1] != 0:
        if not check_order(value, idx, sequence_data, header_info[1]):
            sys.stderr.write("Error: Posloupnost neni usporadana!\n")
            sys.exit(1)

sequence_check = validate_sequence_length(sequence_data)
if not sequence_check["valid"]:
    sys.stderr.write(f"{sequence_check['error']}\n")
    sys.exit(1)

# Sorting logic
output_data = []
if header_info[1] == 0:
    output_data = select_sorting_method(sequence_data, header_info[0])
else:
    processed_data = sequence_data[::-1] if header_info[1] == 2 else sequence_data
    output_data = apply_insertion_sort(processed_data) if header_info[2] == 1 else processed_data

# Output results
output_buffer = io.BufferedWriter(io.BytesIO())
for i in range(0, len(output_data), chunk_size):
    block = "\n".join(map(str, output_data[i:i + chunk_size])).encode() + b"\n"
    output_buffer.write(block)
    output_buffer.flush()

sys.stdout.buffer.write(output_buffer.raw.getbuffer())
sys.stdout.flush()