import time
import sys
import os
def prints(strin):
    print
    for i in strin:
        if i == ' ' or i == '\n':
            time.sleep(0.06)
            sys.stdout.write(i)
        else:
            time.sleep(0.03)
            sys.stdout.write(i)
def stream_size(num):
    n=num
    bl=0
    while n > 0:
        n=n/0xff
        bl+=1
    return bl
def stream_split(num,bits=8):
    n=num
    for  i in range(stream_size(num)):
        yield (n >> bits*i) & (2**bits-1)
def shift_add(num1,num2,bits):
    return (num1 << bits) + num2
def lzw(strin,DictSize,WordSize,BufferSize,ByteSize,fp):
    i=0
    lvalue=0xff
    byte_stack_buffer=[]
    byte_stak=[]
    Dict={}
    while i <= len(strin)-2:
        if strin[i]+strin[i+1] in Dict.keys() and i <= len(strin)-3:
            strin[i+1]=strin[i]+strin[i+1]
            i+=1
            continue
         
        if len(Dict) <= DictSize-0xff and len(strin[i]+strin[i+1]) <= WordSize and i <= len(strin)-3:
            lvalue+=1
            Dict[strin[i]+strin[i+1]]=lvalue
        if len(strin[i])//2>0:
            n=Dict[strin[i]]
        else:
            n=ord(strin[i])
        byte_stack_buffer.append(n)
        if 0>1:
            streamToFile(fp,bufferToStream(byte_stack_buffer,ByteSize))
            Dict={}
            fp.write('\255\255\255')
            fp.flush()
            byte_stack_buffer=[]
            
        i+=1
    byte_stack_buffer.append(ord(strin[-1]))
    streamToFile(fp,bufferToStream(byte_stack_buffer,ByteSize))
    fp.write('\255\255\255')
    fp.flush()
def unlzw(en_chr,ByteSize,BufferSize):
    Dict={}
    de_ord=[]
    flag=0
    init=0
    dict_count=1
    en_ord=[ord(i) for i in en_chr]
    long_stream=bufferToStream(en_ord,8)
    en_stream=[i for i in stream_split(long_stream,ByteSize)]
    en_stream.reverse()
    for i in range(0,len(en_stream)):
        if en_stream[i]!= 0L:
            en_stream=en_stream[i:]
            break
    for next_tokn in en_stream:
        kkk=1
        
        if flag == 0:
            flag+=1
            curr_tokn=next_tokn
            continue
        elif next_tokn <= 255:             
            if curr_tokn>255:

                curr_tokn=Dict[curr_tokn]
                Dict[0xff+dict_count]=curr_tokn+(next_tokn,)
                de_ord+=list(curr_tokn)
                curr_tokn=next_tokn
                kkk+=1
            else:
                Dict[0xff+dict_count]=(curr_tokn,next_tokn)
                de_ord.append(curr_tokn)
                curr_tokn=next_tokn
                kkk+=1
        elif next_tokn > 255:
            if curr_tokn>255:
                try:
                    Dict[0xff+dict_count]=tuple(Dict[curr_tokn]+(Dict[next_tokn][0],))
                except KeyError:
                    Dict[0xff+dict_count]=tuple(Dict[curr_tokn]+(Dict[curr_tokn][0],))
                kkk+=1
                de_ord+=list(Dict[curr_tokn])
                curr_tokn=next_tokn
            else:
                try:
                    Dict[0xff+dict_count]=(curr_tokn,Dict[next_tokn][0])
                except KeyError:
                    if curr_tokn>255:
                        Dict[0xff+dict_count]=tuple(Dict[curr_tokn]+(Dict[curr_tokn][0],))
                    else:
                        Dict[0xff+dict_count]=(curr_tokn,curr_tokn)
                de_ord.append(curr_tokn)
                curr_tokn=next_tokn
                kkk+=1
        dict_count+=1
    de_ord.append(curr_tokn)
    for i in de_ord:
        yield chr(i)

def ltos(l):
    st=""
    for i in l:                            
        st+=str(i).strip()
        st+=' '
    return st
def bufferToStream(Buffer,ByteSize):
    if len(Buffer) == 0:
        return 0
    n1=Buffer[0]
    for i in range(1,len(Buffer)):
        n1=shift_add(n1,Buffer[i],ByteSize)
    return n1
def streamToFile(File,stream):
    l=[i for i in stream_split(stream)]
    l.reverse()
    s=''
    for i in l:
        s+=chr(i)
    File.write(s)
def getFileSize(fp):
    pos=fp.tell()
    f.seek(0,2)
    size = f.tell()
    f.seek(pos)
    return pos

def compressFile(fp,fpout,DictSize=510,WordSize=50,BufferSize=500,ByteSize=9):
    fpout.write(str(BufferSize)+'|'+str(ByteSize)+'#')
    fp.seek(0,2)
    size = fp.tell()
    fp.seek(0)
    t=time.time()
    for i in range((size//BufferSize)+1):
        lzw(list(fp.read(BufferSize)),DictSize,WordSize,BufferSize,ByteSize,fpout)
    t=time.time()-t
    print t

def uncompressFile(fp,fpout):
    ByteSize=''
    header_len=0
    while '#' not in ByteSize:
        ByteSize+=fp.read(1)
        if '|' in ByteSize:
            BufferSize=ByteSize
            ByteSize=''
            header_len+=1
    curr_pos=fp.tell()
    fp.seek(0,2)
    en_size = fp.tell()-header_len
    fp.seek(curr_pos)
    BufferSize=int(BufferSize[:-1])    
    ByteSize=int(ByteSize[:-1])
    en_chr=fp.read()
    en_block=en_chr.split('\255\255\255')
    t=time.time()
    for j in range(len(en_block)-1):
        for i in unlzw(en_block[j],ByteSize,BufferSize):
            fpout.write(i)
        fpout.flush()
#        print 'test'
    print time.time() - t

def compress(inName,outName,default=1,conf=[]):
    try:
        fpin=open(inName,'rb')
    except IOError:
        return 1
    fout=open(outName,'wb+')
    if default == 1:
        compressFile(fpin,fout)
    else:
        if len(conf) == 4:
            compressFile(fpin,fout,conf[0],conf[1],conf[2],conf[3])
            return 0
        else:
            print len(conf),'PLEASE CLECK CONFIGURATION: `compress()` ERR'
            return 1
    fpin.close()
    fout.close()
def uncompress(inName,outName):
    try:
        fpin=open(inName,'rb')
    except IOError:
        return 1
    fout=open(outName,'wb+')
    uncompressFile(fpin,fout)
    fpin.close()
    fout.close()
def lzw_feedback(strin,fp,slowmo=0,DictSize=510,WordSize=100,BufferSize=5000,ByteSize=9):
    i=0
    lvalue=0xff
    byte_stack_buffer=[]
    byte_stak=[]
    Dict={}
    flag1=0
    inlen=len(strin)
    prints('Welcome to LZW feedback,I will explain you how a bunch of bytes are going to compress with Lempel-Ziv-Welch (LZW) algorithm.\nIt actually expands ASCII dictionary from 255 to 256,256 and more.So here is your string\n')
    print ltos(strin)
    prints('So here I\'m gonna expand dictionary or simply create my own dictonary with its max size '+str(2**ByteSize)+' ,ASCII byte is of 8 bits but byte size of my byte is  '+str(ByteSize)+',wonder how?.')
    print '\n|current character|next character|output|dictonary|'
    while i <= len(strin)-2:
        if strin[i]+strin[i+1] in Dict.keys() and i <= len(strin)-3:
            strin[i+1]=strin[i]+strin[i+1]
            prints('Hey! `'+strin[i+1]+'` is already in the dictonary\n')  
            i+=1
            continue
         
        if len(Dict) <= DictSize-0xff and len(strin[i]+strin[i+1]) <= WordSize and i <= len(strin)-3:
            lvalue+=1
            
            Dict[strin[i]+strin[i+1]]=lvalue
        if len(strin[i])//2>0:
            n=Dict[strin[i]]
        else:
            n=ord(strin[i])
        print '| '+strin[i]+' | '+strin[i+1]+' | '+strin[i]+' | '+strin[i]+strin[i+1]+'('+str(lvalue)+')'+'|'
        if flag1 == 0:
            prints('here character `'+strin[i]+'` and `'+strin[i+1]+'` combine to give a new word in LZW dictionary i.e `'+strin[i]+strin[i+1]+'`. But order of `'+strin[i]+'` in ASCII is `'+str(ord(strin[i]))+'` and that of `'+strin[i+1]+'` is `'+str(ord(strin[i+1]))+'`. So what will be order of `'+strin[i]+strin[i+1]+'`?\nWait! I have expanded my byte size so I can expand my dictonary limit beyond 256. This is the tricky part. Order of `'+strin[i]+strin[i+1]+'` is my dictonary will be 256.\nThis way i will continue')
            flag1=1
        byte_stack_buffer.append(n)
        raw_input('\nPress ENTER to continue.....')
        if 0>1:
            streamToFile(fp,bufferToStream(byte_stack_buffer,ByteSize))
            Dict={}
            fp.write('\255\255\255')
            fp.flush()
            byte_stack_buffer=[]
            
        i+=1
    byte_stack_buffer.append(ord(strin[-1]))
    prints('So, finally I have completed my word. But before you go to my sibling unlzw() le us see what I have done.')
    if len(byte_stack_buffer) < inlen:
        prints('Hey! I have reduced your string by '+str(inlen-len(byte_stack_buffer))+' character,isn\'t fun compressing? is it?\n')
    else:
        prints('Hey! I think that string didn\'t gone well.I don\'t think i have reduced its size. Have fun\n')
    streamToFile(fp,bufferToStream(byte_stack_buffer,ByteSize))
    fp.write('\255\255\255')
    fp.flush()
def unlzw_feedback(en_chr,ByteSize=9,BufferSize=5000):
    Dict={}
    de_ord=[]
    flag=0
    init=0
    dict_count=1
    prints('Welcome to LZW Uncompression,this part is more tricky than compression.Because my sibling has generated a set of crappy string which human can hardly understand.\nIt look like this.\n')
    print en_chr
    prints('So, first i will convert this crappy code into its equivalent '+str(ByteSize)+' byte character list,here it is,\n')
    en_ord=[ord(i) for i in en_chr]
    long_stream=bufferToStream(en_ord,8)
    en_stream=[i for i in stream_split(long_stream,ByteSize)]
    en_stream.reverse()

    for i in range(0,len(en_stream)):
        if en_stream[i]!= 0L:
            en_stream=en_stream[i:]
            break
    print en_stream
    prints('Now I will continue generating a new dictonary')
    for next_tokn in en_stream:
        kkk=1
        
        if flag == 0:
            flag+=1
            curr_tokn=next_tokn
            continue
        elif next_tokn <= 255:             
            if curr_tokn>255:

                curr_tokn=Dict[curr_tokn]
                Dict[0xff+dict_count]=curr_tokn+(next_tokn,)
                de_ord+=list(curr_tokn)
                curr_tokn=next_tokn
                kkk+=1
            else:
                Dict[0xff+dict_count]=(curr_tokn,next_tokn)
                de_ord.append(curr_tokn)
                curr_tokn=next_tokn
                kkk+=1
        elif next_tokn > 255:
            if curr_tokn>255:
                try:
                    Dict[0xff+dict_count]=tuple(Dict[curr_tokn]+(Dict[next_tokn][0],))
                except KeyError:
                    Dict[0xff+dict_count]=tuple(Dict[curr_tokn]+(Dict[curr_tokn][0],))
                kkk+=1
                de_ord+=list(Dict[curr_tokn])
                curr_tokn=next_tokn
            else:
                try:
                    Dict[0xff+dict_count]=(curr_tokn,Dict[next_tokn][0])
                except KeyError:
                    if curr_tokn>255:
                        Dict[0xff+dict_count]=tuple(Dict[curr_tokn]+(Dict[curr_tokn][0],))
                    else:
                        Dict[0xff+dict_count]=(curr_tokn,curr_tokn)
                de_ord.append(curr_tokn)
                curr_tokn=next_tokn
                kkk+=1
        dict_count+=1
    de_ord.append(curr_tokn)
    prints('So,here is new dictonary,\n')
    print Dict
    for i in de_ord:
        yield chr(i)
   
def compressString(strin):
    if len(strin) == 0:
        print '\nNo string given'
        return
    lzw(list(strin),510,10**3,1000,9,sys.stdout)
def uncompressString(strin):
    if len(strin) == 0:
        print '\nNo string given'
        return
    for i in unlzw(strin,9,10**3):
        sys.stdout.write(i)
#main
def_conf=[510,50,500,9]
conf=[510,50,500,9]
i=None
while i != 0:
    print '\n'*50
    try:
        i=input('\n1. Compress file\n2. Uncompress file\n3. Compress String\t\n4. Uncompress String\n5. Compress String \t*with feedback\n6. Uncompress String \t*with feedback\n7. Configure LZW\n8. Restore default\n0.Quit\n>>>')
        if i==1:
            for i in os.listdir('.'):
                print i
            if compress(raw_input('\nEnter file name to compress>>>'),raw_input('\nEnter output file>>>'),0,conf):
                        print '\nOops! I can\'t find your file'
        elif i==2:
            for i in os.listdir('.'):
                print i
            if uncompress(raw_input('\nEnter file name to uncompress>>>'),raw_input('\nEnter output file>>>')):
                        print '\nOops! I can\'t find your file'
        elif i==3:
            compressString(raw_input('\nEnter String to compress>>>'))
        elif i==4:
            uncompressString(raw_input('\nEnter String to uncompress>>>'))
        elif i==5:
            lzw_feedback(list(raw_input('\nEnter String to compress>>>')),sys.stdout)
        elif i==6:
            for i in unlzw_feedback(raw_input('\nEnter String to uncompress>>>')):
                sys.stdout.write(i)
        elif i==7:
            l=[None for i in range(0,4)]
            l[3]=input('\nEnter Byte size(>8);DEFAULT:9>>>')
            l[0]=input('\nEnter Dictonary size(<= 2**(byte size) -2);DEFAULT:510>>>')
            l[1]=input('\nEnter Word size;DEFAULT:50>>>')
            l[2]=input('\nEnter Buffer size;DEFAULT:500>>>')
            conf=list(l)
            del l
        elif i==8:
            conf=list(def_conf)
            print'\n Restored default settings'
        elif i==0:
            break
        else:
            continue
        raw_input('\nEnter to continue......')
    except SyntaxError:
        pass
