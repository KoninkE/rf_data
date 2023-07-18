# rf_data

Email 1: koninket@mail.uc.edu
Email 2: elliottkoninkdonner@outlook.com

My generated RF data set that uses a variety of digital modulation schemes at various carrier frequencies. The scripts used to generate the data set are also available as well.

This data set uses 301 words- such as 'watts' or 'bpsk'- that are encoded into RF signals as bits. The "rand_words.txt" file holds the words used to generate the data set in a shuffled order. The "rand_bits.txt" file holds these byte-encoded words, where each letter is a byte, and the encodings correspond to the same lines as the words text file. If you want to generate your own encoded words the "generate bitstrings.py" file will take a .txt file with newline delimination.

List of used modulation types: OOK, 2-ASK, 4-ASK, BPSK, QPSK, 16-PSK, 16-QAM, 2-FSK, 4-FSK

List of carrier frequencies: 5MHz, 10MHz, 50MHz, 75MHz, 100MHz, 200MHz, 500MHz, 750MHz, 900MHz

Sample Rate: 13.5GHz (Oversampled above Nyquist Rate)

FSK Carrier Offset: 100KHz

Symbol Rate: 250MHz

Total Number of Signals: 2025 (25 Signals Per Carrier x 9 Carrier Frequencies x 9 Modulation Types)

To generate the data set use the "Generate Radio Data Set.py" file and make sure to set the right file paths. This file generates all of the listed modulation types but the user provides a list of carrier frequencies to generate the data as well as the sample rate. The file's primary dependencies are "APSK.py", "FSK.py", and "radio_aid.py". The data provided should be byte arrays in the form of a bitstream.

Feel free to reach out to me if you have any questions or concerns at the emails listed at the top.
