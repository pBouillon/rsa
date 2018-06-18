from utils import *

if __name__ == '__main__':
    msg = input('Please write your message:\n> ')
    print()

    p = get_rdm_prime_nb()
    q = get_rdm_prime_nb(to_ignore=[p])
    print(f'p = {p} ; q = {q}')
    print()

    pub_k, priv_k = gen_keys(p, q)

    print(f'public key: {pub_k}\nprivate key: {priv_k}')
    print()

    print(f'Original message:\n{msg}')
    print()

    ciphertext = encrypt(priv_k, msg)
    print('Encrypted message:')
    print(''.join(map(lambda x: str(x), ciphertext)))
    print()

    decrypted = decrypt(pub_k, ciphertext)
    print('Decrypted message:')
    print(''.join(map(lambda x: str(x), decrypted)))
