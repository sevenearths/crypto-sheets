![Alt text](/header.jpeg?raw=true "Preview")

# crypto-sheets
**NOTE: This project is incomplete. It requires the proper implementation of BIP39 and BIP32 to work properly. If you know how to derive a BIP32 Extended Key from a BIP39 Passphrase please contact me!!!** *(play around with `test_mnemonic.py`)*

## Introduction

Unlike tradition forms such as finance *(bank account number)* and communication *(telephone number, email)*, crypto currencies unique identifiers *(addresses)* are; long, hard to type/communicate and easily forgettable. With the advent of QR codes and cheep adhesive labeling these addresses *(both public and private)* can be stored and displayed in a number of ways so that communities using digital wallets can conduct commerce un-hindered.
The adhesive label sheets for this project can be found [here](https://duckduckgo.com/?q=TANEX%20TW-2044)
A video of my presentation on this project can be found [here](https://youtu.be/1cg3dBUQQa8?t=319)

## Aim

This project was designed to help communities who have limited access to infrastructure and metropolitan areas.

### Considerations

 1. Cost must be kept to minimum
 2. The items required must be cheep
 3. Common technology should be used where ever possible
 4. The software should be simple to setup and use

### Achievements

 1. Labels are printable on standard laser jet printers
 2. The per address can be as low as $0.14
 3. A4 Test pages can be printed first to make sure alignment is correct
 4. Numbers and graphics are displayed as images to ensure consistence across different computers

### Features

 1. Modular design so coins can be added easily
 2. Currency logo in the center of public keys
 3. Unique four digit number on each row *(if someone is storing a number of partial private keys they can find one easily)*
 4. QR code for Apple and Android wallets
 5. Icons rather than text for suggested storage locations
 6. 4 x Partial private keys *(i.e two private keys)* for redundancy
 7. Private keys as keys or mnemonic

## Commands
Look at the `install.txt` file to get your virtual environment up and running.
```
# python test-page.py
# python generator.py --help
# ...
```
