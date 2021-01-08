#!/usr/bin/python3
#   Einführung in die Kryptographie 1
#   Projekt: AES T-Tables
#
#   Gruppe         :
# 
#   Name           :
#   Matrikelnummer :
# 
#   Name           :
#   Matrikelnummer :

######################################
# static and global variables

mixColumn_tabelle = [[0x02, 0x01, 0x01, 0x03],
                     [0x03, 0x02, 0x01, 0x01],
                     [0x01, 0x03, 0x02, 0x01],
                     [0x01, 0x01, 0x03, 0x02]]

# !!! KEINE ÄNDERUNGEN IN DIESEM ABSCHNITT !!!
    
# AES S-Box
sbox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]

# AES Rundenkonstanten
rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

######################################
# code


def multiply_pol(hex1, hex2):
    s1 = [int(x) for x in bin(hex1)[2:]]
    s2 = [int(x) for x in bin(hex2)[2:]]

    res = [0] * (len(s1) + len(s2) - 1)
    for o1, i1 in enumerate(s1):
        for o2, i2 in enumerate(s2):
            res[o1 + o2] += i1 * i2
            if res[o1 + o2] >= 2:
                res[o1 + o2] %= 2

    return res


def division_pol(dividend):
    # dividend and divisor are both polynomials, which are here simply lists of coefficients. Eg: x^2 + 3x + 5 will be represented as [1, 3, 5]
    divisor = [1,0,0,0,1,1,0,1,1]
    out = list(dividend)  # Copy the dividend
    normalizer = divisor[0]

    for i in range(len(dividend) - (len(divisor) - 1)):
        out[i] /= normalizer  # for general polynomial division (when polynomials are non-monic),
        # we need to normalize by dividing the coefficient with the divisor's first coefficient
        coef = out[i]
        if coef != 0:  # useless to multiply if coef is 0
            for j in range(1, len(
                    divisor)):  # in synthetic division, we always skip the first coefficient of the divisor,
                # because it's only used to normalize the dividend coefficients
                out[i + j] += -divisor[j] * coef
                if out[i + j] >= 2:
                    out[i + j] %= 2


    # The resulting out contains both the quotient and the remainder, the remainder being the size of the divisor (the remainder
    # has necessarily the same degree as the divisor since it's what we couldn't divide from the dividend), so we compute the index
    # where this separation is, and return the quotient and remainder.
    separator = -(len(divisor) - 1)
    result = ''.join([str(int(abs(x))) for x in out[separator:]])
    if len(result) - 8 < 0:
        for i in range(8 - len(result)):
            result = '0' + result

    return result # return quotient, remainder.


# In dieser Funktion sollen die T-Tables berechnet und anschließend über 
# "t_tables" zurückgegeben werden. Das Ergebnis muss also in "t_tables" geschrieben
# werden, wobei "t_tables[i]" alle 256 Werte von T_i enthält.
# 
# t_tables[4][256] - Array zum Speichern der T-Tables T_0 bis T_3.
def precompute_t_tables(t_tables):
    # TODO Implementiere diese Funktion
    for index, value in enumerate(t_tables):
        value.clear()
        for init_value in range(256):
            column_values_list = [str(division_pol(multiply_pol(s, sbox[init_value]))) for s in mixColumn_tabelle[index]]
            column_values_to_int = int(''.join(column_values_list), 2)
            value.append(column_values_to_int)

    return 0  # TODO mit "return 0;" ersetzen, um die Testbench zu aktivieren
    

# In dieser Funktion soll ein gegebener Rundenschlüssel "roundkey" auf den 
# aktuellen Zustand "state" des AES addiert werden.
# Das Ergebnis der Berechnungen muss wieder in "state" geschrieben werden.
# 
# state[16] - Aktueller Zustand des AES.
# roundkey[16] - Aktueller Rundenschlüssel.
def add_roundkey(state, roundkey):
    # TODO Implementiere diese Funktion
    state_out = [int(bin(x ^ y), 2) for x, y in zip(state, roundkey)]
    state.clear()
    state += state_out
    return 1 # TODO mit "return 0;" ersetzen, um die Testbench zu aktivieren

print(1)
# In dieser Funktion soll eine Runde der AES-Verschlüsselung ausgeführt werden.
# Dabei darf die normale AES S-Box nicht verwendet werden, stattdessen sollen 
# bei der Berechnung die T-Tables verwendet werden.
# Das Ergebnis der Berechnungen soll wieder in "state" geschrieben werden.
# 
# t_tables[4][256] - Array zum Speichern der T-Tables T_0 bis T_3.
# state[16] - Aktueller Zustand des AES.
# roundkey[16] - Aktueller Rundenschlüssel.
def enc_round(t_tables, state, roundkey):
    # TODO Implementiere diese Funktion

    return 1 # TODO mit "return 0;" ersetzen, um die Testbench zu aktivieren


# Aufgrund der Besonderheiten der letzten Runde können die T-Tables
# nicht ohne weiteres angewendet werden, daher soll diese Runde
# "klassisch" (also ohne T-Tables) implementiert werden.
# Das Ergebnis der Berechnungen muss in "ciphertext" geschrieben werden.
# 
# state[16] - Aktueller Zustand des AES.
# roundkey[16] - Aktueller Rundenschlüssel.
# ciphertext[16] - Das AES Chiffrat.
def final_enc_round(state, roundkey, ciphertext):
    # TODO Implementiere diese Funktion

    return 1 # TODO mit "return 0;" ersetzen, um die Testbench zu aktivieren


# Mithilfe der Methoden add_roundkey, enc_round ud final_enc_round
# soll eine AES-Verschlüsselung eines Klartextes durchgeführt werden.
# Der Klartext ist zu Beginn in "plaintext" gespeichert, das Ergebnis muss
# in "ciphertext" geschrieben werden.
# 
# t_tables[4][256] - Array zum Speichern der T-Tables T_0 bis T_3.
# plaintext[16] - Der Klartext.
# roundkeys[13][16] - Die 13 Rundenschlüssel für AES-192.
# ciphertext[16] - Das AES Chiffrat.
def encrypt(t_tables, plaintext, roundkeys, ciphertext):
    # TODO Implementiere diese Funktion

    return 1 # TODO mit "return 0;" ersetzen, um die Testbench zu aktivieren


# In dieser Funktion soll der 192-Bit Schlüsselfahplan implementiert werden.
# Der 192-Bit AES-Schlüssel ist im Array "key" gegeben.
# Die erzeugten Rundenschlüssel sollen in "roundkeys" gespeichert werden.
# 
# roundkeys[13][16] - Die 13 Rundenschlüssel für AES-192.
# key[24] Der 192-Bit AES-Schlüssel.
def key_schedule_192(roundkeys, key):
    # TODO Implementiere diese Funktion

    return 1 # TODO mit "return 0;" ersetzen, um die Testbench zu aktivieren
