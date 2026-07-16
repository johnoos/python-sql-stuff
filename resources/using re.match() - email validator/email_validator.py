import email.utils
import re

def validusername(username):
    ## print(' ')                              ## debug
    print(username)                            ## debug
    if match := re.match(r'^[A-Za-z][A-Za-z0-9-._]+$', username):
        ## print('True')                       ## debug
        return True   
    
def validdomain(domain):
    ## print(domain)                           ## debug
    if match := re.match(r'^[A-Za-z]+$', domain):
        ## print('True')                       ## debug
        return True        
    
def validext(ext):
    ## print(ext)                              ## debug      
    if match := re.match(r'^[A-Za-z]+$', ext) and len(ext) <= 3:
        ## print('True')                       ## debug
        return True
    
def main():
    numemailaddresses = input()          
    for i in range (int(numemailaddresses)):
        line = input()
        name, emailaddress = email.utils.parseaddr(line)
        ## print(f'{name} {emailaddress}')
        bracketedemailaddress = f'<{emailaddress}>'
        if match := re.match(r'^<([^@]+)@([^.]+)\.(.+)>', bracketedemailaddress):
            ## print(f'Inside if-block')
            username, domain, ext = match.groups()
            ## print(f'About to call the functions with {username}, {domain}, and {ext}')
            if validusername(username) and validdomain(domain) and validext(ext):
                print(line)

if __name__ == "__main__":
    main()
