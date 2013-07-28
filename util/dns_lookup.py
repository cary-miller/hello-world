import socket
import commands

# ############################################################ #
# ################## DNS/GEO Lookups ######################### #
# ############################################################ #


def example():
    my_name = socket.gethostname()
    my_num = socket.gethostbyname(my_name)


def dnslookup(s):
    return socket.gethostbyaddr(s)


def geolookup(ip):
    rob = requests.get("http://api.hostip.info/get_html.php?ip=%s" %ip)
    return rob.text.split('\n')[1].split(": ")[1]


def host(name):
    cmd = 'host %s' %name
    return_code, result = commands.getstatusoutput(cmd)
    if return_code == 0:
        return result.split()[-1]
    raise Exception(str(return_code) + str(result))



