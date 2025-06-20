import ctypes
import sys
from ctypes import wintypes

CRED_TYPE_GENERIC = 1
class CREDENTIALW(ctypes.Structure):
    _fields_ = [
        ("Flags", wintypes.DWORD),
        ("Type", wintypes.DWORD),
        ("TargetName", wintypes.LPWSTR),
        ("Comment", wintypes.LPWSTR),
        ("LastWritten", wintypes.FILETIME),
        ("CredentialBlobSize", wintypes.DWORD),
        ("CredentialBlob", wintypes.LPBYTE),
        ("Persist", wintypes.DWORD),
        ("AttributeCount", wintypes.DWORD),
        ("Attributes", ctypes.c_void_p),
        ("TargetAlias", wintypes.LPWSTR),
        ("UserName", wintypes.LPWSTR),
    ]

PCREDENTIALW = ctypes.POINTER(CREDENTIALW)
advapi32 = ctypes.windll.advapi32
CredReadW = advapi32.CredReadW
CredReadW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(PCREDENTIALW)]
CredReadW.restype = wintypes.BOOL
CredFree = advapi32.CredFree
CredFree.argtypes = [ctypes.c_void_p]
CredFree.restype = None

def main():
    service_name = input("enter service name : ")
    key = input("enter key value : ")
    query_string = f"{service_name}/{key}"

    pcred = PCREDENTIALW()
    flag = CredReadW(query_string, CRED_TYPE_GENERIC, 0, ctypes.byref(pcred))

    if not flag:
        print("Oooops there is no credential like that, give me another correct key plz")
        sys.exit(1)

    try:
        password_bytes = ctypes.string_at(pcred.contents.CredentialBlob, pcred.contents.CredentialBlobSize)
        password = password_bytes.decode('utf-8')

        username = pcred.contents.UserName
        print(f"requested password by key ID ('{username}')='{password}'")
    
    finally:
        CredFree(pcred)

if __name__ == "__main__":
    main()