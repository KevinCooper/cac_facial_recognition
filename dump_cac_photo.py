"""
    This program dumps general information about a CAC card.
"""
import getpass
import logging
import optparse
from time import sleep


import llsmartcard.apdu as APDU
from llsmartcard.card import CAC
from PIL import Image


def dump_photo(connection, options):
    """
        Will dump all of the interesting information from a CAC card to standard
        out
        
        WARNING: The PIN verify command will be sent multiple times.  If the 
        PIN is wrong, it will lock your CAC card!
    """

    # Open card
    card = CAC(connection)

    # Set this to your PIN.  Please be very careful with this!
    t_pin = getpass.getpass("PIN: ")
    PIN = list(bytearray(t_pin,'ascii'))
    
    # Do we have a PIN to access authenticated information?
    if PIN is not None:
        print("Printing NIST PIV Objects... (PIN PROTECTED)")
        data = card.read_object(APDU.APPLET.NIST_PIV,
                          APDU.OBJ_NIST_PIV.FACE,
                          pin=PIN)
        picture = data[0][1]
        with open("user_face.jp2", "w") as f:
            import re
            container_string = "".join([chr(int(x)) for x in re.findall(r"\d+", str(picture))])
            #import pdb; pdb.set_trace()
            found = container_string.find("\xFF\x4F\xFF\x51")
            if(not found): raise Exception("No JPEG 2000 photo!")
            f.write(container_string[found:])
        image = Image.open("user_face.jp2")
        image.save("user_cac_image.jpeg", "JPEG")
        #import pdb; pdb.set_trace()
        print("Printing DoD CAC Objects... (PIN PROTECTED)")
        card.print_object(APDU.APPLET.DOD_CAC,
                          APDU.OBJ_DOD_CAC.CAC_PERSON,
                          pin=PIN)



if __name__ == "__main__":

    # Import our command line parser
    from llsmartcard import parser
    opts = optparse.OptionParser()

    # parse user arguments
    parser.command_line(opts, dump_photo)