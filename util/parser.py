# input
# ('merkle_root:', 'ef7554402d6f20135a58cd2ca0bf7b23811fef44c60c897c5d0ccb1076d87e18') tx list:['c4b77016d10094c81d08f67c7b5fe5a8d7016726ce5e2a278e01108377990303', '939935f8b5a461735e6858b2f26b75a2d59e947381c218e0a4d4ab9bf7d1ee5a', '51bf22b9ee9b01ef5ce0ddca4d9bfb0668fa5ba4dc83a74487a5a9673a0350d2', '7fbc98331fc6b398de218cfb0468db570b749a8245256ed1a76275b595673dcf', '9688f6c2fd199bad52bdf1709f246c274811dfa71c385b63c9ff8b2ad575b57a', '5372bd612a6cbd9305982146e5c7595ae9b3b4692a8276785a9be6d16c3de3ab', 'e91d4831d2e40c196eb49fa5e31c52ad9f692a5a1e1da3a31c3f31877a75f9bd', '0494df94f8a46df8ca4d853aaf0c6f6de03e28d603a34dd5715e1e99db85d4f8', '4f8792cd18a6cb782d39c8e1877d8d537dc0cbb98bb4984d52d3395490e8e16b', '913dcd7d9f2a019a56c2fc689cbb037c7e4f176a77e1e06f54d98bfcd130c823', 'd0a97351c5325cd21a61dca4a06ffab4ff0c572bbf704d647fe9d6b153fe2434', '0134cbb58304425939eabcf793aeb065e63903ecf2368ce345726527b8b207c3', 'bffd89cf1f0417be00bbe2520b31c901b6ce054f5260d9444f9df199e117c27f', 'c98aa01c5bba8149fe85139561095f99364ca58d9302baad69ae5a94675f7f3f', '????????????????????????????????????????????????????????????????', 'e749c4ba84fe23546aa7d404355e524ad6afaa3c61a785744c92dd39f9b20540', '6a38bc6f76f8cfeb8d35981ac1cdabcc0e60632f3d3f374bb8b23a150d470d7a', 'c5159bb3156df054d39a856232c5d0729534572fa3290883c4c9a3fb3fa7a9dd', 'bffc2e64128da8e0cbf23808ac9cb627f76ac7dff7709a4e4180250adc912dde']

# output type
# return mr, tx_list, index

# output for given input
# mr = ef7554402d6f20135a58cd2ca0bf7b23811fef44c60c897c5d0ccb1076d87e18
# tx_list = (list of 64 bytes tx_hash strings with mutable length)
# index = (index of the tx_hash string starts with "?") = 14


def parse_input(input_data: str) -> tuple[str, list, int]:
    # Extract the merkle root
    merkle_start_phrase = "('merkle_root:', '"
    merkle_root_start = input_data.find(merkle_start_phrase) + len(merkle_start_phrase)  # Find the first single quote
    merkle_root_end = input_data.find("') tx list", merkle_root_start)  # Find the second single quote
    mr = input_data[merkle_root_start:merkle_root_end]

    # Extract the transaction list
    tx_list_start = input_data.find("[") + 1  # Find the opening bracket
    tx_list_end = input_data.find("]", tx_list_start)  # Find the closing bracket
    tx_list_str = input_data[tx_list_start:tx_list_end]
    tx_list = tx_list_str.split(",")  # Split the string into a list
    tx_list = [tx.strip()[1:-1] for tx in tx_list]  # Remove leading and trailing spaces and quotes

    # Identify the index of the transaction hash that starts with "?"
    index = next((i for i, tx in enumerate(tx_list) if tx.startswith("?")), None)

    return mr, tx_list, index


def get_globals() -> tuple[str, list, int]:
    # read from txt file `input.txt`
    with open("./input.txt", "r") as file:
        input_data = file.read()
    mr, tx_list, index = parse_input(input_data)
    return mr, tx_list, index


# Test the function with the given input
if __name__ == '__main__':
    get_globals()
    pass
