from bip_utils import Bip44Coins, Bip44, Bip44Changes
from mnemonic import Mnemonic

mnemonic_phrase = "bus unfold gym admit know climb immune relax bridge sudden unhappy witness"
mnemonic = Mnemonic("english")

entropy = mnemonic.to_entropy(mnemonic_phrase)
print(entropy.hex())

seed = mnemonic.to_seed(mnemonic_phrase)
print(seed.hex())

generated_contract_address = "0x927C084Dc00884c21Cb7f11122B046E358588Cde"

# 3. 시드를 사용하여 BIP44 경로의 지갑 파생
bip44_mst = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)

# 4. 특정 주소의 개인 키 찾기
account = 0
change = Bip44Changes.CHAIN_EXT  # 0 for external chain (receiving addresses)
address_index = 0

for address_index in range(2 ** 32):
    bip44_acc = bip44_mst.Purpose().Coin().Account(account)
    bip44_change = bip44_acc.Change(change)
    bip44_addr = bip44_change.AddressIndex(address_index)

    address = bip44_addr.PublicKey().ToAddress()
    if address == generated_contract_address:
        private_key = bip44_addr.PrivateKey().Raw().ToHex()
        public_key = bip44_addr.PublicKey().RawCompressed().ToHex()
        print(f"{address_index}")
        print("Derived Address:", address)
        print("Public Key:", public_key)
        print("Private Key:", private_key)
        break
