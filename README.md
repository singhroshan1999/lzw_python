# lzw_python
python implementation of Lempel Ziv Welch algorithm for file compression. 
lzw(): function to compress string and give output to file.
parameters:
lzw(input string,dictionary size, wordsize of dictonary,buffer size after that dictionary is flushed,
byte size of lzw,output file handle)

unlzw(): function to uncompress string and yield output character. (generator function)
parameters:
unlzw(encoded character, byte size (same as lzw()),buffersize (same as lzw())).

ROSHAN SINGH
NIT RAIPUR
singhroshan1999@gmail.com
