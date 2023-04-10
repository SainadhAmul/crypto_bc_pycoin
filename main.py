from pycoin import Blockchain, Transaction

def main():
    blockchain = Blockchain()

    while True:
        print("\nMenu:")
        print("1. Add a new transaction")
        print("2. Mine a new block")
        print("3. Display the blockchain")
        print("4. Check blockchain validity")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            sender = input("Enter the sender's address: ")
            recipient = input("Enter the recipient's address: ")
            amount = float(input("Enter the transaction amount: "))
            transaction = Transaction(sender, recipient, amount)
            print('Created Transaction')
            blockchain.add_block(transaction)
            print('transaction added to blockchain')
            continue

        elif choice == "2":
            blockchain.add_block(blockchain.pending_transactions)
            print("New block mined and added to the blockchain!")
            continue

        elif choice == "3":
            for block in blockchain.chain:
                print("\nBlock Index:", block.index)
                print("Previous Hash:", block.previous_hash)
                print("Timestamp:", block.timestamp)
                print("Transactions:", block.data)
                print("Nonce:", block.nonce)
                print("Hash:", block.hash)

            continue

        elif choice == "4":
            if blockchain.is_chain_valid():
                print("The blockchain is valid.")
            else:
                print("The blockchain is not valid.")

            continue

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")


main()


if __name__ == "__main__":
    main()
