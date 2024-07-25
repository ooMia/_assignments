from eth_hash.auto import (
    keccak,
)

# function 0x41424344() public payable {
#     v0 = sha256hash(0x77aeec0b38e07e77e0fceaee2742275c84ac2fc0026da95abfb692a7b934a280);
#     if (0 != v0) {
#         require(0x88f1eb6fc83d5b83b8d9443c4af8f72f8664c992b211610f47acd2e6f0767357 != MEM[0]);
#     }
#     return 1;
# }
#
# // Note: The function selector is not present in the original solidity code.
# // However, we display it for the sake of completeness.
#
# function function_selector( function_selector) public payable {
#     if (0x41424344 != function_selector >> 224) {
#         v1 = 0;
#         v0 = 255
#         v2 = sha256hash(0x7a9c571c22a679da5b82394f8ead31cf567a930e6827e9564c50bd722114afc7 ^ (0x333c86e14b3dbbb36563c1da6120387d418af2250faf48da26536a9111acc717 ^ (MEM[0x40] ^ (function_selector ^ keccak256(msg.sender)))));
#         if (0 != v2) {
#             if (0x88f1eb6fc83d5b83b8d9443c4af8f72f8664c992b211610f47acd2e6f0767357 == MEM[0]) {
#                 return 1;
#             }
#         }
#         revert();
#     } else {
#         0x41424344();
#     }
# }
from hashlib import sha256

a = ["0x77aeec0b38e07e77e0fceaee2742275c84ac2fc0026da95abfb692a7b934a280",
     "0x88f1eb6fc83d5b83b8d9443c4af8f72f8664c992b211610f47acd2e6f0767357"]
b = ["0x7a9c571c22a679da5b82394f8ead31cf567a930e6827e9564c50bd722114afc7",
     "0x333c86e14b3dbbb36563c1da6120387d418af2250faf48da26536a9111acc717",
     "0x0345b666897fc960d9bda0fab6a75830bb2dd4dda3f4804731ac4ff7722c7dcd"
     "0x88f1eb6fc83d5b83b8d9443c4af8f72f8664c992b211610f47acd2e6f0767357"] # this goes mem0

r = sha256(bytes.fromhex("77aeec0b38e07e77e0fceaee2742275c84ac2fc0026da95abfb692a7b934a280"))
print(r.hexdigest())

print(bytes.fromhex("be862ad9abfe6f22bcb087716c7d89a26051f74c"))
print(bytes.fromhex("20"))

s = b'\xbe\x86*\xd9\xab\xfeo"\xbc\xb0\x87ql}\x89\xa2`Q\xf7L\x20'
r = keccak(s)
print(r.hex())
