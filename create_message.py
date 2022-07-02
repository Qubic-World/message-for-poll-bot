import json
import logging

from algorithms.verify import *


def get_identity_list(seeds: list[str]) -> list[str]:
    if len(seeds) <= 0:
        return []

    identity_list = []
    for seed in seeds:
        result = get_subseed(seed)
        if result[0] == False:
            logging.error(f"Failed to get subseed from {seed}")
            continue

        identity_list.append(get_identity(
            get_public_key(get_private_key(result[1]))))

    return identity_list


def create_digest(username_id: str):
    kangaroo_twelve(username_id.encode('ascii'))


def create_json(seeds: list[str], username_id: str):
    digest = kangaroo_twelve(username_id.encode('ascii'))

    dict_list = []
    for seed in seeds:
        result = get_subseed(seed)
        if result[0] == False:
            logging.error(f"Failed to get subseed from {seed}")
            continue

        subseed = result[1]
        public_key = get_public_key(get_private_key(subseed))
        signatyre = pretty_signatyre(sign(subseed, public_key, digest))
        identity = get_identity(public_key)
        dict_list.append({"identity": identity, "username_id": username_id, "signature": signatyre})

    return json.loads(json.dumps(dict_list))


def main():
    try:
        seed_nums: int = int(input("Enter the number of seeds: "))
        if seed_nums <= 0:
            return
    except Exception as e:
        logging.error(e)
        return

    seed_len = 55
    seeds = []
    while len(seeds) < seed_nums:
        seed: str = str(input(f"Enter the seed number {len(seeds) +1}: "))
        seed_alpha = ''.join([s for s in seed if s.isalpha()])
        print(seed_alpha)
        if len(seed_alpha) != seed_len:
            logging.warning("Invalid seed")
            continue

        seeds.append(seed_alpha)

    # Delete duplicates
    seeds = list(set(seeds))
    print(f"Your seeds: {seeds}")

    username_id = input("Enter your ID from discord: ")
    if len(username_id) <= 0:
        logging.error("Your ID is empty")
        return

    print(json.dumps(create_json(seeds, username_id), indent=4))


if __name__ == "__main__":
    main()
